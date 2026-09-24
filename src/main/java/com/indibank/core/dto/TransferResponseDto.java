package com.indibank.core.dto;

import com.indibank.core.domain.model.TransferStatus;
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
@Schema(description = "Response returned upon transfer settlement")
public class TransferResponseDto implements Serializable {

    @Schema(description = "Unique banking transaction reference", example = "TRX-20260924-104921")
    private String referenceNumber;

    @Schema(description = "Client provided idempotency key", example = "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d")
    private String idempotencyKey;

    @Schema(description = "Settlement status", example = "SETTLED")
    private TransferStatus status;

    @Schema(description = "Originating account number", example = "1001002001")
    private String sourceAccountNumber;

    @Schema(description = "Destination account number", example = "1001002002")
    private String destinationAccountNumber;

    @Schema(description = "Transferred amount", example = "2500000.00")
    private BigDecimal amount;

    @Schema(description = "Currency", example = "IDR")
    private String currency;

    @Schema(description = "Description", example = "Payment for Invoice #INV-2026-09")
    private String description;

    @Schema(description = "General Ledger journal entry ID in Oracle DB", example = "1042")
    private Long journalEntryId;

    @Schema(description = "Timestamp when transaction settled", example = "2026-09-24T10:49:21Z")
    private Instant createdAt;
}
