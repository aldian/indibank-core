package com.indibank.core.controller;

import com.indibank.core.dto.AccountBalanceResponseDto;
import com.indibank.core.dto.AccountStatementResponseDto;
import com.indibank.core.dto.AccountSummaryDto;
import com.indibank.core.service.AccountService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/accounts")
@RequiredArgsConstructor
@Tag(name = "Accounts", description = "Account Balances and Immutable Ledger Statements")
public class AccountController {

    private final AccountService accountService;

    @GetMapping
    @Operation(summary = "List All Active Demo Accounts")
    public ResponseEntity<List<AccountSummaryDto>> listAccounts() {
        return ResponseEntity.ok(accountService.getAllAccounts());
    }

    @GetMapping("/{accountNumber}/balance")
    @Operation(summary = "Retrieve Cached Account Balance",
            description = "Returns real-time account balance from Redis cache or Oracle DB with cache write-through.")
    public ResponseEntity<AccountBalanceResponseDto> getAccountBalance(
            @Parameter(description = "10-digit account number", example = "1001002001")
            @PathVariable String accountNumber) {
        return ResponseEntity.ok(accountService.getAccountBalance(accountNumber));
    }

    @GetMapping("/{accountNumber}/statement")
    @Operation(summary = "Query Account Statement (Double-Entry Journal Entries)",
            description = "Returns immutable general ledger journal entries for the specified account from Oracle DB.")
    public ResponseEntity<AccountStatementResponseDto> getAccountStatement(
            @PathVariable String accountNumber,
            @RequestParam(defaultValue = "20") int limit) {
        return ResponseEntity.ok(accountService.getAccountStatement(accountNumber, limit));
    }
}
