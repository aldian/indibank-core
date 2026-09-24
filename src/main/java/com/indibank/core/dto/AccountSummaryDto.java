package com.indibank.core.dto;

import com.indibank.core.domain.model.AccountStatus;
import com.indibank.core.domain.model.AccountType;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "Account overview")
public class AccountSummaryDto {
    private Long id;
    private String accountNumber;
    private String accountHolderName;
    private AccountType accountType;
    private String currency;
    private BigDecimal balance;
    private AccountStatus status;
}
