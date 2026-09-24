package com.indibank.core.event;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.indibank.core.config.KafkaConfig;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

@Slf4j
@Component
@RequiredArgsConstructor
public class TransferFraudDetectorConsumer {

    private final TransferEventProducer eventProducer;
    private final RecentEventsTracker eventsTracker;
    private final ObjectMapper objectMapper;

    @Value("${indibank.fraud.high-value-threshold-idr:100000000.00}")
    private BigDecimal highValueThreshold;

    @KafkaListener(topics = KafkaConfig.TOPIC_TRANSFERS_SETTLED, groupId = "indibank-fraud-detector")
    public void evaluateSettledTransfer(ConsumerRecord<String, Object> record) {
        try {
            TransferSettledEvent event = objectMapper.convertValue(record.value(), TransferSettledEvent.class);
            log.info("Fraud engine received transfer settlement [ref={}, amount={} {}]",
                    event.getTransferReference(), event.getAmount(), event.getCurrency());

            eventsTracker.recordEvent(
                    record.topic(),
                    record.partition(),
                    record.offset(),
                    record.key(),
                    event
            );

            // Rule 1: High-Value Transaction Screening (> Rp 100,000,000)
            if (event.getAmount().compareTo(highValueThreshold) >= 0) {
                log.warn("🚨 AML ALERT: Transfer {} of IDR {} exceeds single-transaction limit of IDR {}!",
                        event.getTransferReference(), event.getAmount(), highValueThreshold);

                FraudAlertEvent alert = FraudAlertEvent.builder()
                        .alertId(UUID.randomUUID().toString())
                        .alertType("HIGH_VALUE_TRANSACTION")
                        .severity("CRITICAL")
                        .transferReference(event.getTransferReference())
                        .sourceAccountNumber(event.getSourceAccountNumber())
                        .destinationAccountNumber(event.getDestinationAccountNumber())
                        .amount(event.getAmount())
                        .currency(event.getCurrency())
                        .triggerReason(String.format("Transfer amount IDR %s exceeds high-value reporting threshold of IDR %s",
                                event.getAmount().toPlainString(), highValueThreshold.toPlainString()))
                        .detectedAt(Instant.now())
                        .build();

                eventProducer.publishFraudAlert(alert);
            }
        } catch (Exception e) {
            log.error("Error evaluating fraud rule for record {}", record, e);
        }
    }
}
