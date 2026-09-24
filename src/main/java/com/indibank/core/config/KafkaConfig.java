package com.indibank.core.config;

import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.config.TopicBuilder;
import org.springframework.kafka.core.KafkaOperations;
import org.springframework.kafka.listener.CommonErrorHandler;
import org.springframework.kafka.listener.DeadLetterPublishingRecoverer;
import org.springframework.kafka.listener.DefaultErrorHandler;
import org.springframework.util.backoff.FixedBackOff;

@Configuration
@EnableKafka
public class KafkaConfig {

    public static final String TOPIC_TRANSFERS_SETTLED = "bank.transfers.settled";
    public static final String TOPIC_FRAUD_ALERTS = "bank.fraud.alerts";
    public static final String TOPIC_TRANSFERS_DLQ = "bank.transfers.dlq";

    @Bean
    public NewTopic settledTransfersTopic() {
        return TopicBuilder.name(TOPIC_TRANSFERS_SETTLED)
                .partitions(3)
                .replicas(1)
                .build();
    }

    @Bean
    public NewTopic fraudAlertsTopic() {
        return TopicBuilder.name(TOPIC_FRAUD_ALERTS)
                .partitions(3)
                .replicas(1)
                .build();
    }

    @Bean
    public NewTopic transfersDlqTopic() {
        return TopicBuilder.name(TOPIC_TRANSFERS_DLQ)
                .partitions(3)
                .replicas(1)
                .build();
    }

    @Bean
    public CommonErrorHandler kafkaErrorHandler(KafkaOperations<Object, Object> kafkaOperations) {
        DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(kafkaOperations);
        // Retry 3 times with 1-second interval before publishing to DLQ
        return new DefaultErrorHandler(recoverer, new FixedBackOff(1000L, 3L));
    }
}
