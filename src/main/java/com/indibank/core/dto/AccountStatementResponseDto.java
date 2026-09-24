package com.indibank.core.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "Account statement containing double-entry journal entries")
public class AccountStatementResponseDto {
    private String accountNumber;
    private BigDecimal currentBalance;
    private List<JournalLineDto> entries;
}
