package com.indibank.core.integration;

import com.indibank.core.controller.AccountController;
import com.indibank.core.controller.GlobalExceptionHandler;
import com.indibank.core.domain.model.AccountType;
import com.indibank.core.dto.AccountBalanceResponseDto;
import com.indibank.core.dto.AccountStatementResponseDto;
import com.indibank.core.dto.AccountSummaryDto;
import com.indibank.core.dto.JournalLineDto;
import com.indibank.core.service.AccountService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;
import java.util.NoSuchElementException;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(AccountController.class)
@Import(GlobalExceptionHandler.class)
class AccountControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private AccountService accountService;

    @Test
    @DisplayName("GET /api/v1/accounts - should return list of accounts")
    void shouldReturnAccountsList() throws Exception {
        AccountSummaryDto acc1 = AccountSummaryDto.builder()
                .id(1L)
                .accountNumber("1001002001")
                .accountHolderName("Budi Santoso")
                .accountType(AccountType.CHECKING)
                .currency("IDR")
                .balance(new BigDecimal("500000000.00"))
                .status(com.indibank.core.domain.model.AccountStatus.ACTIVE)
                .build();

        when(accountService.getAllAccounts()).thenReturn(List.of(acc1));

        mockMvc.perform(get("/api/v1/accounts"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].accountNumber").value("1001002001"))
                .andExpect(jsonPath("$[0].accountHolderName").value("Budi Santoso"));
    }

    @Test
    @DisplayName("GET /api/v1/accounts/{accountNumber}/balance - should return balance with cache status")
    void shouldReturnBalance() throws Exception {
        AccountBalanceResponseDto balanceDto = AccountBalanceResponseDto.builder()
                .accountNumber("1001002001")
                .balance(new BigDecimal("500000000.00"))
                .currency("IDR")
                .cached(true)
                .build();

        when(accountService.getAccountBalance("1001002001")).thenReturn(balanceDto);

        mockMvc.perform(get("/api/v1/accounts/1001002001/balance"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.accountNumber").value("1001002001"))
                .andExpect(jsonPath("$.balance").value(500000000.00))
                .andExpect(jsonPath("$.cached").value(true));
    }

    @Test
    @DisplayName("GET /api/v1/accounts/{accountNumber}/balance - should return 404 on unknown account")
    void shouldReturn404OnUnknownAccount() throws Exception {
        when(accountService.getAccountBalance("9999999999"))
                .thenThrow(new NoSuchElementException("Account not found: 9999999999"));

        mockMvc.perform(get("/api/v1/accounts/9999999999/balance"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.code").value("RESOURCE_NOT_FOUND"));
    }

    @Test
    @DisplayName("GET /api/v1/accounts/{accountNumber}/statement - should return ledger journal entries")
    void shouldReturnStatement() throws Exception {
        JournalLineDto entry = JournalLineDto.builder()
                .id(1L)
                .transferReference("TRX-TEST-01")
                .entryType(com.indibank.core.domain.model.JournalEntryType.DEBIT)
                .amount(new BigDecimal("1000000.00"))
                .balanceAfter(new BigDecimal("499000000.00"))
                .description("Test debit")
                .timestamp(Instant.now())
                .build();

        AccountStatementResponseDto statementDto = AccountStatementResponseDto.builder()
                .accountNumber("1001002001")
                .currentBalance(new BigDecimal("499000000.00"))
                .entries(List.of(entry))
                .build();

        when(accountService.getAccountStatement("1001002001", 10)).thenReturn(statementDto);

        mockMvc.perform(get("/api/v1/accounts/1001002001/statement?limit=10"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.accountNumber").value("1001002001"))
                .andExpect(jsonPath("$.entries[0].transferReference").value("TRX-TEST-01"));
    }
}
