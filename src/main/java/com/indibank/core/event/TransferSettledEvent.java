package com.indibank.core.event;

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
public class TransferSettledEvent implements Serializable {

    private String eventId;
    @Builder.Default
    private String eventType = "TRANSFER_SETTLED";
    private String transferReference;
    private String idempotencyKey;
    private String sourceAccountNumber;
    private String destinationAccountNumber;
    private BigDecimal amount;
    private String currency;
    private String description;
    private Instant settledAt;
}
