package com.indibank.core;

import com.indibank.core.controller.AccountController;
import com.indibank.core.dto.AccountBalanceResponseDto;
import com.indibank.core.dto.AccountStatementResponseDto;
import com.indibank.core.dto.AccountSummaryDto;
import com.indibank.core.service.AccountService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.math.BigDecimal;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AccountControllerTest {

    @Mock
    private AccountService accountService;

    @InjectMocks
    private AccountController accountController;

    @Test
    @DisplayName("Should return list of accounts")
    void shouldListAccounts() {
        AccountSummaryDto summary = AccountSummaryDto.builder()
                .accountNumber("1001002001")
                .accountHolderName("Budi")
                .build();
        when(accountService.getAllAccounts()).thenReturn(List.of(summary));

        ResponseEntity<List<AccountSummaryDto>> response = accountController.listAccounts();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(1, response.getBody().size());
        assertEquals("1001002001", response.getBody().get(0).getAccountNumber());
    }

    @Test
    @DisplayName("Should return account balance")
    void shouldGetAccountBalance() {
        AccountBalanceResponseDto balance = AccountBalanceResponseDto.builder()
                .accountNumber("1001002001")
                .balance(new BigDecimal("1000000.00"))
                .build();
        when(accountService.getAccountBalance("1001002001")).thenReturn(balance);

        ResponseEntity<AccountBalanceResponseDto> response = accountController.getAccountBalance("1001002001");

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("1001002001", response.getBody().getAccountNumber());
    }

    @Test
    @DisplayName("Should return account statement")
    void shouldGetAccountStatement() {
        AccountStatementResponseDto statement = AccountStatementResponseDto.builder()
                .accountNumber("1001002001")
                .entries(List.of())
                .build();
        when(accountService.getAccountStatement("1001002001", 10)).thenReturn(statement);

        ResponseEntity<AccountStatementResponseDto> response = accountController.getAccountStatement("1001002001", 10);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("1001002001", response.getBody().getAccountNumber());
    }
}
