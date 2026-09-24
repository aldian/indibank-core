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
public class FraudAlertEvent implements Serializable {

    private String alertId;
    private String alertType; // HIGH_VALUE_TRANSACTION, RAPID_VELOCITY
    private String severity; // INFO, WARNING, CRITICAL
    private String transferReference;
    private String sourceAccountNumber;
    private String destinationAccountNumber;
    private BigDecimal amount;
    private String currency;
    private String triggerReason;
    private Instant detectedAt;
}
