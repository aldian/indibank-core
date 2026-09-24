package com.indibank.core.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "Request payload to initiate a fund transfer")
public class TransferRequestDto {

    @NotBlank(message = "Source account number is required")
    @Pattern(regexp = "^[0-9]{10}$", message = "Source account number must be 10 digits")
    @Schema(description = "10-digit source account number", example = "1001002001")
    private String sourceAccountNumber;

    @NotBlank(message = "Destination account number is required")
    @Pattern(regexp = "^[0-9]{10}$", message = "Destination account number must be 10 digits")
    @Schema(description = "10-digit destination account number", example = "1001002002")
    private String destinationAccountNumber;

    @NotNull(message = "Amount is required")
    @DecimalMin(value = "1000.00", message = "Minimum transfer amount is IDR 1,000")
    @DecimalMax(value = "500000000.00", message = "Maximum single transfer amount is IDR 500,000,000")
    @Schema(description = "Transfer amount in IDR", example = "2500000.00")
    private BigDecimal amount;

    @Builder.Default
    @Schema(description = "Currency code", example = "IDR", defaultValue = "IDR")
    private String currency = "IDR";

    @Size(max = 140, message = "Description cannot exceed 140 characters")
    @Schema(description = "Transfer memo or invoice reference", example = "Payment for Invoice #INV-2026-09")
    private String description;
}
