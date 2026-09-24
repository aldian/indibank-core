package com.indibank.core.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.math.BigDecimal;
import java.time.Instant;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "Account balance information")
public class AccountBalanceResponseDto implements Serializable {
    private String accountNumber;
    private String accountHolderName;
    private BigDecimal balance;
    private String currency;
    private boolean cached;
    private Instant lastUpdated;
}
