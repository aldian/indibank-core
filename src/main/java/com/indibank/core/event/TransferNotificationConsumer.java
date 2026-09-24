package com.indibank.core.event;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.indibank.core.config.KafkaConfig;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class TransferNotificationConsumer {

    private final RecentEventsTracker eventsTracker;
    private final ObjectMapper objectMapper;

    @KafkaListener(topics = KafkaConfig.TOPIC_FRAUD_ALERTS, groupId = "indibank-notification-service")
    public void onFraudAlert(ConsumerRecord<String, Object> record) {
        try {
            FraudAlertEvent alert = objectMapper.convertValue(record.value(), FraudAlertEvent.class);
            log.warn("📩 COMPLIANCE ALERT DISPATCH: Ref={}, Severity={}, Reason={}",
                    alert.getTransferReference(), alert.getSeverity(), alert.getTriggerReason());

            eventsTracker.recordEvent(
                    record.topic(),
                    record.partition(),
                    record.offset(),
                    record.key(),
                    alert
            );
        } catch (Exception e) {
            log.error("Error processing fraud alert notification", e);
        }
    }
}
