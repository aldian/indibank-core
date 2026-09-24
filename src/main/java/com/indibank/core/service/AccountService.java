package com.indibank.core.service;

import com.indibank.core.domain.model.Account;
import com.indibank.core.domain.model.JournalEntry;
import com.indibank.core.domain.repository.AccountRepository;
import com.indibank.core.domain.repository.JournalEntryRepository;
import com.indibank.core.dto.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;
import java.util.NoSuchElementException;

@Slf4j
@Service
@RequiredArgsConstructor
public class AccountService {

    private final AccountRepository accountRepository;
    private final JournalEntryRepository journalEntryRepository;
    private final AccountBalanceCacheService cacheService;

    @Transactional(readOnly = true)
    public List<AccountSummaryDto> getAllAccounts() {
        return accountRepository.findAll().stream()
                .map(this::mapToSummary)
                .toList();
    }

    @Transactional(readOnly = true)
    public AccountBalanceResponseDto getAccountBalance(String accountNumber) {
        // Fast-path: Check Redis Cache first
        AccountBalanceResponseDto cached = cacheService.getCachedBalance(accountNumber);
        if (cached != null) {
            log.debug("Served balance for {} from Redis cache", accountNumber);
            return cached;
        }

        // Cache miss: Fallback to Oracle DB
        Account account = accountRepository.findByAccountNumber(accountNumber)
                .orElseThrow(() -> new NoSuchElementException("Account not found: " + accountNumber));

        AccountBalanceResponseDto response = AccountBalanceResponseDto.builder()
                .accountNumber(account.getAccountNumber())
                .accountHolderName(account.getAccountHolderName())
                .balance(account.getBalance())
                .currency(account.getCurrency())
                .cached(false)
                .lastUpdated(Instant.now())
                .build();

        // Write-through to Redis
        cacheService.cacheBalance(accountNumber, response);
        return response;
    }

    @Transactional(readOnly = true)
    public AccountStatementResponseDto getAccountStatement(String accountNumber, int limit) {
        Account account = accountRepository.findByAccountNumber(accountNumber)
                .orElseThrow(() -> new NoSuchElementException("Account not found: " + accountNumber));

        List<JournalEntry> entries = journalEntryRepository.findByAccountNumberOrderByCreatedAtDesc(
                accountNumber, PageRequest.of(0, Math.min(limit, 100)));

        List<JournalLineDto> lineDtos = entries.stream()
                .map(entry -> JournalLineDto.builder()
                        .id(entry.getId())
                        .transferReference(entry.getTransfer().getTransferReference())
                        .entryType(entry.getEntryType())
                        .amount(entry.getAmount())
                        .balanceAfter(entry.getBalanceAfter())
                        .description(entry.getDescription())
                        .timestamp(entry.getCreatedAt())
                        .build())
                .toList();

        return AccountStatementResponseDto.builder()
                .accountNumber(account.getAccountNumber())
                .currentBalance(account.getBalance())
                .entries(lineDtos)
                .build();
    }

    private AccountSummaryDto mapToSummary(Account a) {
        return AccountSummaryDto.builder()
                .id(a.getId())
                .accountNumber(a.getAccountNumber())
                .accountHolderName(a.getAccountHolderName())
                .accountType(a.getAccountType())
                .currency(a.getCurrency())
                .balance(a.getBalance())
                .status(a.getStatus())
                .build();
    }
}
