package com.indibank.core;

import com.indibank.core.domain.model.Account;
import com.indibank.core.domain.model.AccountStatus;
import com.indibank.core.domain.model.AccountType;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.*;

class AccountModelTest {

    @Test
    @DisplayName("Test Account domain debit, credit, and balance validation")
    void testAccountOperations() {
        Account account = Account.builder()
                .id(1L)
                .accountNumber("1001002001")
                .accountHolderName("Test User")
                .accountType(AccountType.CHECKING)
                .status(AccountStatus.ACTIVE)
                .currency("IDR")
                .balance(new BigDecimal("100000.00"))
                .build();

        assertTrue(account.hasSufficientBalance(new BigDecimal("50000.00")));
        assertTrue(account.hasSufficientBalance(new BigDecimal("100000.00")));
        assertFalse(account.hasSufficientBalance(new BigDecimal("100001.00")));

        // Debit
        account.debit(new BigDecimal("30000.00"));
        assertEquals(new BigDecimal("70000.00"), account.getBalance());

        // Credit
        account.credit(new BigDecimal("50000.00"));
        assertEquals(new BigDecimal("120000.00"), account.getBalance());

        // Debit beyond balance throws IllegalStateException
        assertThrows(IllegalStateException.class, () -> account.debit(new BigDecimal("200000.00")));
    }
}
