package com.indibank.core;

import com.indibank.core.domain.model.Account;
import com.indibank.core.domain.model.AccountStatus;
import com.indibank.core.domain.model.AccountType;
import com.indibank.core.domain.model.JournalEntry;
import com.indibank.core.domain.model.JournalEntryType;
import com.indibank.core.domain.model.Transfer;
import com.indibank.core.domain.repository.AccountRepository;
import com.indibank.core.domain.repository.JournalEntryRepository;
import com.indibank.core.dto.AccountBalanceResponseDto;
import com.indibank.core.dto.AccountStatementResponseDto;
import com.indibank.core.dto.AccountSummaryDto;
import com.indibank.core.service.AccountBalanceCacheService;
import com.indibank.core.service.AccountService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AccountServiceTest {

    @Mock
    private AccountRepository accountRepository;

    @Mock
    private JournalEntryRepository journalEntryRepository;

    @Mock
    private AccountBalanceCacheService cacheService;

    @InjectMocks
    private AccountService accountService;

    private Account testAccount;

    @BeforeEach
    void setUp() {
        testAccount = Account.builder()
                .id(1L)
                .accountNumber("1001002001")
                .accountHolderName("Budi Santoso")
                .accountType(AccountType.CHECKING)
                .currency("IDR")
                .balance(new BigDecimal("500000000.00"))
                .status(AccountStatus.ACTIVE)
                .createdAt(Instant.now())
                .updatedAt(Instant.now())
                .build();
    }

    @Test
    @DisplayName("Should return all accounts mapped to summary DTOs")
    void shouldReturnAllAccounts() {
        when(accountRepository.findAll()).thenReturn(List.of(testAccount));

        List<AccountSummaryDto> result = accountService.getAllAccounts();

        assertEquals(1, result.size());
        assertEquals("1001002001", result.get(0).getAccountNumber());
        assertEquals("Budi Santoso", result.get(0).getAccountHolderName());
    }

    @Test
    @DisplayName("Should serve balance from Redis cache if present")
    void shouldReturnBalanceFromCache() {
        AccountBalanceResponseDto cached = AccountBalanceResponseDto.builder()
                .accountNumber("1001002001")
                .balance(new BigDecimal("500000000.00"))
                .cached(true)
                .build();

        when(cacheService.getCachedBalance("1001002001")).thenReturn(cached);

        AccountBalanceResponseDto result = accountService.getAccountBalance("1001002001");

        assertNotNull(result);
        assertTrue(result.isCached());
        verifyNoInteractions(accountRepository);
    }

    @Test
    @DisplayName("Should fetch balance from Oracle DB on cache miss and write through to Redis")
    void shouldFetchBalanceFromDbOnCacheMiss() {
        when(cacheService.getCachedBalance("1001002001")).thenReturn(null);
        when(accountRepository.findByAccountNumber("1001002001")).thenReturn(Optional.of(testAccount));

        AccountBalanceResponseDto result = accountService.getAccountBalance("1001002001");

        assertNotNull(result);
        assertEquals("1001002001", result.getAccountNumber());
        assertEquals(new BigDecimal("500000000.00"), result.getBalance());
        assertFalse(result.isCached());
        verify(cacheService).cacheBalance(eq("1001002001"), any());
    }

    @Test
    @DisplayName("Should throw NoSuchElementException when account not found for balance")
    void shouldThrowWhenAccountNotFoundForBalance() {
        when(cacheService.getCachedBalance("9999999999")).thenReturn(null);
        when(accountRepository.findByAccountNumber("9999999999")).thenReturn(Optional.empty());

        assertThrows(NoSuchElementException.class, () -> accountService.getAccountBalance("9999999999"));
    }

    @Test
    @DisplayName("Should return account statement with journal entries")
    void shouldReturnAccountStatement() {
        Transfer transfer = Transfer.builder()
                .id(1L)
                .transferReference("TRX-TEST-001")
                .build();

        JournalEntry entry = JournalEntry.builder()
                .id(10L)
                .transfer(transfer)
                .account(testAccount)
                .entryType(JournalEntryType.DEBIT)
                .amount(new BigDecimal("1000000.00"))
                .balanceAfter(new BigDecimal("499000000.00"))
                .description("Test Debit")
                .createdAt(Instant.now())
                .build();

        when(accountRepository.findByAccountNumber("1001002001")).thenReturn(Optional.of(testAccount));
        when(journalEntryRepository.findByAccountNumberOrderByCreatedAtDesc(eq("1001002001"), any()))
                .thenReturn(List.of(entry));

        AccountStatementResponseDto statement = accountService.getAccountStatement("1001002001", 10);

        assertNotNull(statement);
        assertEquals("1001002001", statement.getAccountNumber());
        assertEquals(1, statement.getEntries().size());
        assertEquals("TRX-TEST-001", statement.getEntries().get(0).getTransferReference());
    }

    @Test
    @DisplayName("Should throw when account not found for statement")
    void shouldThrowWhenAccountNotFoundForStatement() {
        when(accountRepository.findByAccountNumber("9999999999")).thenReturn(Optional.empty());

        assertThrows(NoSuchElementException.class, () -> accountService.getAccountStatement("9999999999", 10));
    }
}
