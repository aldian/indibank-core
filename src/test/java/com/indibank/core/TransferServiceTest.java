package com.indibank.core;

import com.indibank.core.domain.model.Account;
import com.indibank.core.domain.model.AccountStatus;
import com.indibank.core.domain.model.AccountType;
import com.indibank.core.domain.model.JournalEntry;
import com.indibank.core.domain.model.Transfer;
import com.indibank.core.domain.repository.AccountRepository;
import com.indibank.core.domain.repository.JournalEntryRepository;
import com.indibank.core.domain.repository.TransferRepository;
import com.indibank.core.dto.TransferRequestDto;
import com.indibank.core.dto.TransferResponseDto;
import com.indibank.core.event.TransferEventProducer;
import com.indibank.core.service.AccountBalanceCacheService;
import com.indibank.core.service.DistributedLockService;
import com.indibank.core.service.IdempotencyService;
import com.indibank.core.service.IdempotencyService.IdempotencyResult;
import com.indibank.core.service.IdempotencyService.IdempotencyStatus;
import com.indibank.core.service.TransferService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class TransferServiceTest {

    @Mock
    private AccountRepository accountRepository;

    @Mock
    private TransferRepository transferRepository;

    @Mock
    private JournalEntryRepository journalEntryRepository;

    @Mock
    private IdempotencyService idempotencyService;

    @Mock
    private DistributedLockService lockService;

    @Mock
    private AccountBalanceCacheService cacheService;

    @Mock
    private TransferEventProducer eventProducer;

    @InjectMocks
    private TransferService transferService;

    private Account sourceAccount;
    private Account destAccount;

    @BeforeEach
    void setUp() {
        sourceAccount = Account.builder()
                .id(1L)
                .accountNumber("1001002001")
                .accountHolderName("Budi Santoso")
                .accountType(AccountType.CHECKING)
                .balance(new BigDecimal("10000000.00"))
                .status(AccountStatus.ACTIVE)
                .currency("IDR")
                .build();

        destAccount = Account.builder()
                .id(2L)
                .accountNumber("1001002002")
                .accountHolderName("Siti Rahma")
                .accountType(AccountType.SAVINGS)
                .balance(new BigDecimal("5000000.00"))
                .status(AccountStatus.ACTIVE)
                .currency("IDR")
                .build();
    }

    @Test
    @DisplayName("Should successfully settle transfer and update double-entry balances")
    void shouldSettleTransferSuccessfully() {
        String idempKey = "test-uuid-001";
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("2000000.00"))
                .currency("IDR")
                .description("Test Transfer")
                .build();

        when(idempotencyService.checkAndLock(eq(idempKey), any()))
                .thenReturn(new IdempotencyResult(IdempotencyStatus.ACQUIRED, null));
        when(lockService.acquireLock(eq("1001002001"), any())).thenReturn("lock-token-123");
        when(accountRepository.findByAccountNumber("1001002001")).thenReturn(Optional.of(sourceAccount));
        when(accountRepository.findByAccountNumber("1001002002")).thenReturn(Optional.of(destAccount));
        when(transferRepository.save(any(Transfer.class))).thenAnswer(inv -> {
            Transfer t = inv.getArgument(0);
            t.setId(101L);
            return t;
        });
        when(journalEntryRepository.save(any(JournalEntry.class))).thenAnswer(inv -> {
            com.indibank.core.domain.model.JournalEntry j = inv.getArgument(0);
            j.setId(1001L);
            return j;
        });

        TransferResponseDto response = transferService.processTransfer(idempKey, request);

        assertNotNull(response);
        assertEquals("1001002001", response.getSourceAccountNumber());
        assertEquals("1001002002", response.getDestinationAccountNumber());
        assertEquals(new BigDecimal("2000000.00"), response.getAmount());

        // Verify balance updates
        assertEquals(new BigDecimal("8000000.00"), sourceAccount.getBalance());
        assertEquals(new BigDecimal("7000000.00"), destAccount.getBalance());

        // Verify lock release and idempotency completion
        verify(lockService).releaseLock(eq("1001002001"), eq("lock-token-123"));
        verify(idempotencyService).markCompleted(eq(idempKey), any(), any());
        verify(eventProducer).publishTransferSettled(any());
    }

    @Test
    @DisplayName("Should return cached response on idempotent duplicate replay")
    void shouldReturnCachedResponseOnIdempotentReplay() {
        String idempKey = "replay-uuid";
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("1000000.00"))
                .build();

        TransferResponseDto cached = TransferResponseDto.builder()
                .referenceNumber("TRX-CACHED-001")
                .idempotencyKey(idempKey)
                .amount(new BigDecimal("1000000.00"))
                .build();

        when(idempotencyService.checkAndLock(eq(idempKey), any()))
                .thenReturn(new IdempotencyResult(IdempotencyStatus.COMPLETED, cached));

        TransferResponseDto result = transferService.processTransfer(idempKey, request);

        assertEquals("TRX-CACHED-001", result.getReferenceNumber());
        verifyNoInteractions(accountRepository);
        verifyNoInteractions(transferRepository);
    }

    @Test
    @DisplayName("Should reject transfer when balance is insufficient")
    void shouldRejectWhenBalanceInsufficient() {
        String idempKey = "insufficient-funds-key";
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("999999999.00")) // Exceeds balance
                .currency("IDR")
                .build();

        when(idempotencyService.checkAndLock(eq(idempKey), any()))
                .thenReturn(new IdempotencyResult(IdempotencyStatus.ACQUIRED, null));
        when(lockService.acquireLock(eq("1001002001"), any())).thenReturn("lock-token-abc");
        when(accountRepository.findByAccountNumber("1001002001")).thenReturn(Optional.of(sourceAccount));
        when(accountRepository.findByAccountNumber("1001002002")).thenReturn(Optional.of(destAccount));

        assertThrows(IllegalArgumentException.class, () -> transferService.processTransfer(idempKey, request));

        verify(lockService).releaseLock(eq("1001002001"), eq("lock-token-abc"));
        verify(idempotencyService).releaseKey(eq(idempKey));
    }

    @Test
    @DisplayName("Should reject when concurrent transfer request is in-progress")
    void shouldRejectWhenConcurrentRequestInProgress() {
        String idempKey = "in-progress-key";
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("1000.00"))
                .build();

        when(idempotencyService.checkAndLock(eq(idempKey), any()))
                .thenReturn(new IdempotencyResult(IdempotencyStatus.IN_PROGRESS, null));

        assertThrows(IllegalStateException.class, () -> transferService.processTransfer(idempKey, request));
    }

    @Test
    @DisplayName("Should reject when source and destination accounts are identical")
    void shouldRejectWhenSameAccount() {
        String idempKey = "same-acc-key";
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002001")
                .amount(new BigDecimal("1000.00"))
                .build();

        when(idempotencyService.checkAndLock(eq(idempKey), any()))
                .thenReturn(new IdempotencyResult(IdempotencyStatus.ACQUIRED, null));

        assertThrows(IllegalArgumentException.class, () -> transferService.processTransfer(idempKey, request));
        verify(idempotencyService).releaseKey(eq(idempKey));
    }

    @Test
    @DisplayName("Should reject when distributed lock acquisition fails")
    void shouldRejectWhenLockAcquisitionFails() {
        String idempKey = "lock-fail-key";
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("1000.00"))
                .build();

        when(idempotencyService.checkAndLock(eq(idempKey), any()))
                .thenReturn(new IdempotencyResult(IdempotencyStatus.ACQUIRED, null));
        when(lockService.acquireLock(eq("1001002001"), any())).thenReturn(null);

        assertThrows(IllegalStateException.class, () -> transferService.processTransfer(idempKey, request));
        verify(idempotencyService).releaseKey(eq(idempKey));
    }

    @Test
    @DisplayName("Should reject when source account is not found")
    void shouldRejectWhenSourceAccountNotFound() {
        String idempKey = "src-not-found-key";
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("1000.00"))
                .build();

        when(idempotencyService.checkAndLock(eq(idempKey), any()))
                .thenReturn(new IdempotencyResult(IdempotencyStatus.ACQUIRED, null));
        when(lockService.acquireLock(eq("1001002001"), any())).thenReturn("lock-1");
        when(accountRepository.findByAccountNumber("1001002001")).thenReturn(Optional.empty());

        assertThrows(java.util.NoSuchElementException.class, () -> transferService.processTransfer(idempKey, request));
        verify(lockService).releaseLock(eq("1001002001"), eq("lock-1"));
        verify(idempotencyService).releaseKey(eq(idempKey));
    }

    @Test
    @DisplayName("Should reject when destination account is not found")
    void shouldRejectWhenDestAccountNotFound() {
        String idempKey = "dst-not-found-key";
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("1000.00"))
                .build();

        when(idempotencyService.checkAndLock(eq(idempKey), any()))
                .thenReturn(new IdempotencyResult(IdempotencyStatus.ACQUIRED, null));
        when(lockService.acquireLock(eq("1001002001"), any())).thenReturn("lock-1");
        when(accountRepository.findByAccountNumber("1001002001")).thenReturn(Optional.of(sourceAccount));
        when(accountRepository.findByAccountNumber("1001002002")).thenReturn(Optional.empty());

        assertThrows(java.util.NoSuchElementException.class, () -> transferService.processTransfer(idempKey, request));
        verify(lockService).releaseLock(eq("1001002001"), eq("lock-1"));
        verify(idempotencyService).releaseKey(eq(idempKey));
    }

    @Test
    @DisplayName("Should reject when source account is not active")
    void shouldRejectWhenSourceAccountInactive() {
        String idempKey = "src-inactive-key";
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("1000.00"))
                .build();

        sourceAccount.setStatus(AccountStatus.FROZEN);
        when(idempotencyService.checkAndLock(eq(idempKey), any()))
                .thenReturn(new IdempotencyResult(IdempotencyStatus.ACQUIRED, null));
        when(lockService.acquireLock(eq("1001002001"), any())).thenReturn("lock-1");
        when(accountRepository.findByAccountNumber("1001002001")).thenReturn(Optional.of(sourceAccount));
        when(accountRepository.findByAccountNumber("1001002002")).thenReturn(Optional.of(destAccount));

        assertThrows(IllegalStateException.class, () -> transferService.processTransfer(idempKey, request));
    }

    @Test
    @DisplayName("Should reject when destination account is not active")
    void shouldRejectWhenDestAccountInactive() {
        String idempKey = "dst-inactive-key";
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("1000.00"))
                .build();

        destAccount.setStatus(AccountStatus.DORMANT);
        when(idempotencyService.checkAndLock(eq(idempKey), any()))
                .thenReturn(new IdempotencyResult(IdempotencyStatus.ACQUIRED, null));
        when(lockService.acquireLock(eq("1001002001"), any())).thenReturn("lock-1");
        when(accountRepository.findByAccountNumber("1001002001")).thenReturn(Optional.of(sourceAccount));
        when(accountRepository.findByAccountNumber("1001002002")).thenReturn(Optional.of(destAccount));

        assertThrows(IllegalStateException.class, () -> transferService.processTransfer(idempKey, request));
    }

    @Test
    @DisplayName("Should query transfer by reference successfully")
    void shouldQueryTransferByReference() {
        Transfer transfer = Transfer.builder()
                .id(1L)
                .transferReference("TRX-20260924-0001")
                .idempotencyKey("uuid-query")
                .status(com.indibank.core.domain.model.TransferStatus.SETTLED)
                .sourceAccount(sourceAccount)
                .destinationAccount(destAccount)
                .amount(new BigDecimal("50000.00"))
                .currency("IDR")
                .description("Test description")
                .journalEntryId(99L)
                .build();

        when(transferRepository.findByTransferReference("TRX-20260924-0001")).thenReturn(Optional.of(transfer));

        TransferResponseDto result = transferService.getTransferByReference("TRX-20260924-0001");

        assertNotNull(result);
        assertEquals("TRX-20260924-0001", result.getReferenceNumber());
        assertEquals("uuid-query", result.getIdempotencyKey());
    }

    @Test
    @DisplayName("Should throw NoSuchElementException when transfer reference not found")
    void shouldThrowWhenTransferNotFound() {
        when(transferRepository.findByTransferReference("TRX-NONE")).thenReturn(Optional.empty());

        assertThrows(java.util.NoSuchElementException.class, () -> transferService.getTransferByReference("TRX-NONE"));
    }

    @Test
    @DisplayName("Should handle Kafka publish exception gracefully and complete transfer")
    void shouldHandleKafkaPublishExceptionGracefully() {
        String idempKey = "kafka-fail-key";
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("1000.00"))
                .currency("IDR")
                .build();

        when(idempotencyService.checkAndLock(eq(idempKey), any()))
                .thenReturn(new IdempotencyResult(IdempotencyStatus.ACQUIRED, null));
        when(lockService.acquireLock(eq("1001002001"), any())).thenReturn("lock-token-k");
        when(accountRepository.findByAccountNumber("1001002001")).thenReturn(Optional.of(sourceAccount));
        when(accountRepository.findByAccountNumber("1001002002")).thenReturn(Optional.of(destAccount));
        when(transferRepository.save(any(Transfer.class))).thenAnswer(inv -> inv.getArgument(0));
        when(journalEntryRepository.save(any(JournalEntry.class))).thenAnswer(inv -> {
            JournalEntry j = inv.getArgument(0);
            j.setId(88L);
            return j;
        });
        doThrow(new RuntimeException("Kafka unreachable")).when(eventProducer).publishTransferSettled(any());

        TransferResponseDto response = transferService.processTransfer(idempKey, request);

        assertNotNull(response);
        verify(lockService).releaseLock(eq("1001002001"), eq("lock-token-k"));
        verify(idempotencyService).markCompleted(eq(idempKey), any(), any());
    }
}

