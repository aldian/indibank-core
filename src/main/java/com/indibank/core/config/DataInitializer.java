package com.indibank.core.config;

import com.indibank.core.domain.model.Account;
import com.indibank.core.domain.model.AccountStatus;
import com.indibank.core.domain.model.AccountType;
import com.indibank.core.domain.repository.AccountRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.util.List;

@Slf4j
@Component
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {

    private final AccountRepository accountRepository;

    @Override
    public void run(String... args) {
        if (accountRepository.count() == 0) {
            log.info("Seeding initial demo bank accounts into Oracle DB ledger...");

            List<Account> seedAccounts = List.of(
                    Account.builder()
                            .accountNumber("1001002001")
                            .accountHolderName("Budi Santoso (PT Solusi Digital)")
                            .accountType(AccountType.CHECKING)
                            .currency("IDR")
                            .balance(new BigDecimal("500000000.00"))
                            .status(AccountStatus.ACTIVE)
                            .build(),
                    Account.builder()
                            .accountNumber("1001002002")
                            .accountHolderName("Siti Rahma (Retail Savings)")
                            .accountType(AccountType.SAVINGS)
                            .currency("IDR")
                            .balance(new BigDecimal("15000000.00"))
                            .status(AccountStatus.ACTIVE)
                            .build(),
                    Account.builder()
                            .accountNumber("1001002003")
                            .accountHolderName("IndiBank Corporate Treasury")
                            .accountType(AccountType.CHECKING)
                            .currency("IDR")
                            .balance(new BigDecimal("1250000000.00"))
                            .status(AccountStatus.ACTIVE)
                            .build(),
                    Account.builder()
                            .accountNumber("1001002004")
                            .accountHolderName("Ahmad Hidayat (Payroll)")
                            .accountType(AccountType.SAVINGS)
                            .currency("IDR")
                            .balance(new BigDecimal("3200000.00"))
                            .status(AccountStatus.ACTIVE)
                            .build(),
                    Account.builder()
                            .accountNumber("1001002099")
                            .accountHolderName("National Clearing Settlement GL")
                            .accountType(AccountType.SETTLEMENT_CLEARING)
                            .currency("IDR")
                            .balance(new BigDecimal("9999999999.00"))
                            .status(AccountStatus.ACTIVE)
                            .build()
            );

            accountRepository.saveAll(seedAccounts);
            log.info("Successfully seeded {} demo accounts into Oracle DB.", seedAccounts.size());
        } else {
            log.info("Accounts already present in database (count={}). Skipping seeding.", accountRepository.count());
        }
    }
}
