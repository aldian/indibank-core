package com.indibank.core.dto;

import com.indibank.core.domain.model.JournalEntryType;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.Instant;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "Individual general ledger journal line")
public class JournalLineDto {
    private Long id;
    private String transferReference;
    private JournalEntryType entryType;
    private BigDecimal amount;
    private BigDecimal balanceAfter;
    private String description;
    private Instant timestamp;
}
