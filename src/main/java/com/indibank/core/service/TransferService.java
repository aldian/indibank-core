package com.indibank.core.service;

import com.indibank.core.domain.model.*;
import com.indibank.core.domain.repository.AccountRepository;
import com.indibank.core.domain.repository.JournalEntryRepository;
import com.indibank.core.domain.repository.TransferRepository;
import com.indibank.core.dto.TransferRequestDto;
import com.indibank.core.dto.TransferResponseDto;
import com.indibank.core.event.TransferEventProducer;
import com.indibank.core.event.TransferSettledEvent;
import com.indibank.core.service.IdempotencyService.IdempotencyResult;
import com.indibank.core.service.IdempotencyService.IdempotencyStatus;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Isolation;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.Duration;
import java.time.Instant;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.NoSuchElementException;
import java.util.UUID;
import java.util.concurrent.ThreadLocalRandom;

@Slf4j
@Service
@RequiredArgsConstructor
public class TransferService {

    private final AccountRepository accountRepository;
    private final TransferRepository transferRepository;
    private final JournalEntryRepository journalEntryRepository;
    private final IdempotencyService idempotencyService;
    private final DistributedLockService lockService;
    private final AccountBalanceCacheService cacheService;
    private final TransferEventProducer eventProducer;

    @Value("${indibank.idempotency.ttl-seconds:86400}")
    private long idempotencyTtlSeconds;

    private static final DateTimeFormatter REF_FORMATTER = DateTimeFormatter.ofPattern("yyyyMMdd-HHmmss")
            .withZone(ZoneId.of("UTC"));

    public TransferResponseDto processTransfer(String idempotencyKey, TransferRequestDto request) {
        log.info("Processing transfer request [IdempotencyKey={}, from={}, to={}, amount={} {}]",
                idempotencyKey, request.getSourceAccountNumber(), request.getDestinationAccountNumber(),
                request.getAmount(), request.getCurrency());

        // 1. Redis Idempotency Check
        IdempotencyResult idempResult = idempotencyService.checkAndLock(
                idempotencyKey, Duration.ofSeconds(60));

        if (idempResult.status == IdempotencyStatus.COMPLETED) {
            log.info("Idempotent replay detected for key {}. Returning cached settlement response.", idempotencyKey);
            return idempResult.cachedResponse;
        }

        if (idempResult.status == IdempotencyStatus.IN_PROGRESS) {
            log.warn("Concurrent duplicate transfer request in-flight for key {}", idempotencyKey);
            throw new IllegalStateException("A transfer with this idempotency key is already in progress.");
        }

        // 2. Business Validations
        if (request.getSourceAccountNumber().equals(request.getDestinationAccountNumber())) {
            idempotencyService.releaseKey(idempotencyKey);
            throw new IllegalArgumentException("Source and destination accounts cannot be identical.");
        }

        // 3. Acquire Distributed Lock on Source Account (prevent race-condition double-spending)
        String lockToken = lockService.acquireLock(request.getSourceAccountNumber(), Duration.ofSeconds(10));
        if (lockToken == null) {
            idempotencyService.releaseKey(idempotencyKey);
            throw new IllegalStateException("Account is currently undergoing another transaction. Please retry shortly.");
        }

        try {
            // 4. Execute ACID Transfer Ledger in Oracle DB
            TransferResponseDto settledResponse = executeLedgerTransfer(idempotencyKey, request);

            // 5. Invalidate Redis Caches
            cacheService.evictBalance(request.getSourceAccountNumber());
            cacheService.evictBalance(request.getDestinationAccountNumber());

            // 6. Cache Completed Response under Idempotency Key (24 hours)
            idempotencyService.markCompleted(idempotencyKey, settledResponse, Duration.ofSeconds(idempotencyTtlSeconds));

            // 7. Publish Event to Apache Kafka
            publishSettledEvent(settledResponse);

            return settledResponse;
        } catch (Exception e) {
            log.error("Transfer execution failed for idempotencyKey {}", idempotencyKey, e);
            idempotencyService.releaseKey(idempotencyKey);
            throw e;
        } finally {
            // Always release distributed lock
            lockService.releaseLock(request.getSourceAccountNumber(), lockToken);
        }
    }

    @Transactional(isolation = Isolation.READ_COMMITTED)
    public TransferResponseDto executeLedgerTransfer(String idempotencyKey, TransferRequestDto request) {
        Account sourceAccount = accountRepository.findByAccountNumber(request.getSourceAccountNumber())
                .orElseThrow(() -> new NoSuchElementException("Source account not found: " + request.getSourceAccountNumber()));

        Account destAccount = accountRepository.findByAccountNumber(request.getDestinationAccountNumber())
                .orElseThrow(() -> new NoSuchElementException("Destination account not found: " + request.getDestinationAccountNumber()));

        if (sourceAccount.getStatus() != AccountStatus.ACTIVE) {
            throw new IllegalStateException("Source account is not ACTIVE: status=" + sourceAccount.getStatus());
        }

        if (destAccount.getStatus() != AccountStatus.ACTIVE) {
            throw new IllegalStateException("Destination account is not ACTIVE: status=" + destAccount.getStatus());
        }

        BigDecimal amount = request.getAmount();
        if (!sourceAccount.hasSufficientBalance(amount)) {
            throw new IllegalArgumentException(String.format(
                    "Insufficient funds in account %s. Current balance: %s %s, Requested: %s %s",
                    sourceAccount.getAccountNumber(), sourceAccount.getBalance().toPlainString(),
                    sourceAccount.getCurrency(), amount.toPlainString(), request.getCurrency()));
        }

        // Perform balance updates with optimistic locking
        sourceAccount.debit(amount);
        destAccount.credit(amount);

        accountRepository.save(sourceAccount);
        accountRepository.save(destAccount);

        // Generate Transaction Reference
        String timestamp = REF_FORMATTER.format(Instant.now());
        int randomSuffix = ThreadLocalRandom.current().nextInt(1000, 9999);
        String referenceNumber = String.format("TRX-%s-%04d", timestamp, randomSuffix);

        // Create Transfer Entity
        Transfer transfer = Transfer.builder()
                .transferReference(referenceNumber)
                .idempotencyKey(idempotencyKey)
                .sourceAccount(sourceAccount)
                .destinationAccount(destAccount)
                .amount(amount)
                .currency(request.getCurrency())
                .status(TransferStatus.SETTLED)
                .description(request.getDescription())
                .build();

        transfer = transferRepository.save(transfer);

        // Post Double-Entry Journal: DEBIT Source Account
        JournalEntry debitEntry = JournalEntry.builder()
                .transfer(transfer)
                .account(sourceAccount)
                .entryType(JournalEntryType.DEBIT)
                .amount(amount)
                .balanceAfter(sourceAccount.getBalance())
                .description(String.format("Transfer to %s - %s", destAccount.getAccountNumber(),
                        request.getDescription() != null ? request.getDescription() : "Fund Transfer"))
                .build();
        debitEntry = journalEntryRepository.save(debitEntry);

        // Post Double-Entry Journal: CREDIT Destination Account
        JournalEntry creditEntry = JournalEntry.builder()
                .transfer(transfer)
                .account(destAccount)
                .entryType(JournalEntryType.CREDIT)
                .amount(amount)
                .balanceAfter(destAccount.getBalance())
                .description(String.format("Transfer from %s - %s", sourceAccount.getAccountNumber(),
                        request.getDescription() != null ? request.getDescription() : "Fund Transfer"))
                .build();
        creditEntry = journalEntryRepository.save(creditEntry);

        Long journalId = debitEntry != null ? debitEntry.getId() : null;
        transfer.setJournalEntryId(journalId);
        transferRepository.save(transfer);

        log.info("Double-entry ledger settled: Transfer {} [DEBIT #{} -> CREDIT #{}]",
                referenceNumber, journalId, creditEntry != null ? creditEntry.getId() : null);

        return TransferResponseDto.builder()
                .referenceNumber(transfer.getTransferReference())
                .idempotencyKey(idempotencyKey)
                .status(TransferStatus.SETTLED)
                .sourceAccountNumber(sourceAccount.getAccountNumber())
                .destinationAccountNumber(destAccount.getAccountNumber())
                .amount(amount)
                .currency(request.getCurrency())
                .description(request.getDescription())
                .journalEntryId(debitEntry.getId())
                .createdAt(transfer.getCreatedAt())
                .build();
    }

    @Transactional(readOnly = true)
    public TransferResponseDto getTransferByReference(String referenceNumber) {
        Transfer transfer = transferRepository.findByTransferReference(referenceNumber)
                .orElseThrow(() -> new NoSuchElementException("Transfer reference not found: " + referenceNumber));

        return TransferResponseDto.builder()
                .referenceNumber(transfer.getTransferReference())
                .idempotencyKey(transfer.getIdempotencyKey())
                .status(transfer.getStatus())
                .sourceAccountNumber(transfer.getSourceAccount().getAccountNumber())
                .destinationAccountNumber(transfer.getDestinationAccount().getAccountNumber())
                .amount(transfer.getAmount())
                .currency(transfer.getCurrency())
                .description(transfer.getDescription())
                .journalEntryId(transfer.getJournalEntryId())
                .createdAt(transfer.getCreatedAt())
                .build();
    }

    private void publishSettledEvent(TransferResponseDto response) {
        try {
            TransferSettledEvent event = TransferSettledEvent.builder()
                    .eventId(UUID.randomUUID().toString())
                    .eventType("TRANSFER_SETTLED")
                    .transferReference(response.getReferenceNumber())
                    .idempotencyKey(response.getIdempotencyKey())
                    .sourceAccountNumber(response.getSourceAccountNumber())
                    .destinationAccountNumber(response.getDestinationAccountNumber())
                    .amount(response.getAmount())
                    .currency(response.getCurrency())
                    .description(response.getDescription())
                    .settledAt(response.getCreatedAt() != null ? response.getCreatedAt() : Instant.now())
                    .build();

            eventProducer.publishTransferSettled(event);
        } catch (Exception e) {
            log.error("Failed to publish Kafka event for settled transfer {}", response.getReferenceNumber(), e);
        }
    }
}
