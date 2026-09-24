package com.indibank.core.event;

import com.indibank.core.config.KafkaConfig;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class TransferEventProducer {

    private final KafkaTemplate<String, Object> kafkaTemplate;

    public void publishTransferSettled(TransferSettledEvent event) {
        log.info("Publishing TransferSettledEvent to Kafka [topic={}, key={}, amount={} {}]",
                KafkaConfig.TOPIC_TRANSFERS_SETTLED, event.getTransferReference(), event.getAmount(), event.getCurrency());
        kafkaTemplate.send(KafkaConfig.TOPIC_TRANSFERS_SETTLED, event.getTransferReference(), event);
    }

    public void publishFraudAlert(FraudAlertEvent alert) {
        log.warn("Publishing FraudAlertEvent to Kafka [topic={}, key={}, severity={}, reason={}]",
                KafkaConfig.TOPIC_FRAUD_ALERTS, alert.getTransferReference(), alert.getSeverity(), alert.getTriggerReason());
        kafkaTemplate.send(KafkaConfig.TOPIC_FRAUD_ALERTS, alert.getTransferReference(), alert);
    }
}
