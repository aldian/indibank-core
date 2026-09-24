package com.indibank.core;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.indibank.core.config.KafkaConfig;
import com.indibank.core.dto.StreamEventDto;
import com.indibank.core.event.*;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.test.util.ReflectionTestUtils;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class EventComponentsTest {

    @Mock
    private KafkaTemplate<String, Object> kafkaTemplate;

    @Mock
    private RecentEventsTracker eventsTracker;

    @Mock
    private TransferEventProducer eventProducer;

    private ObjectMapper objectMapper;

    @BeforeEach
    void setUp() {
        objectMapper = new ObjectMapper();
        objectMapper.registerModule(new com.fasterxml.jackson.datatype.jsr310.JavaTimeModule());
    }

    @Test
    @DisplayName("TransferEventProducer should publish settled and fraud events to Kafka")
    void testProducerPublishing() {
        TransferEventProducer producer = new TransferEventProducer(kafkaTemplate);

        TransferSettledEvent settledEvent = TransferSettledEvent.builder()
                .transferReference("TRX-101")
                .amount(new BigDecimal("50000.00"))
                .currency("IDR")
                .build();
        producer.publishTransferSettled(settledEvent);
        verify(kafkaTemplate).send(eq(KafkaConfig.TOPIC_TRANSFERS_SETTLED), eq("TRX-101"), eq(settledEvent));

        FraudAlertEvent alertEvent = FraudAlertEvent.builder()
                .transferReference("TRX-102")
                .severity("CRITICAL")
                .triggerReason("AML threshold")
                .build();
        producer.publishFraudAlert(alertEvent);
        verify(kafkaTemplate).send(eq(KafkaConfig.TOPIC_FRAUD_ALERTS), eq("TRX-102"), eq(alertEvent));
    }

    @Test
    @DisplayName("RecentEventsTracker should record events and enforce 50-item rolling window")
    void testRecentEventsTracker() {
        RecentEventsTracker tracker = new RecentEventsTracker();
        assertEquals(0, tracker.getRecentEvents().size());

        for (int i = 1; i <= 60; i++) {
            tracker.recordEvent("topic-1", 0, i, "key-" + i, "payload-" + i);
        }

        List<StreamEventDto> events = tracker.getRecentEvents();
        assertEquals(50, events.size());
        assertEquals("key-60", events.get(0).getKey()); // most recent is first
    }

    @Test
    @DisplayName("TransferFraudDetectorConsumer evaluates transfer below AML threshold")
    void testFraudDetectorBelowThreshold() {
        TransferFraudDetectorConsumer consumer = new TransferFraudDetectorConsumer(
                eventProducer, eventsTracker, objectMapper);
        ReflectionTestUtils.setField(consumer, "highValueThreshold", new BigDecimal("100000000.00"));

        TransferSettledEvent event = TransferSettledEvent.builder()
                .transferReference("TRX-REGULAR")
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("500000.00"))
                .currency("IDR")
                .settledAt(Instant.now())
                .build();

        ConsumerRecord<String, Object> record = new ConsumerRecord<>(
                KafkaConfig.TOPIC_TRANSFERS_SETTLED, 0, 10L, "TRX-REGULAR", event);

        consumer.evaluateSettledTransfer(record);

        verify(eventsTracker).recordEvent(eq(KafkaConfig.TOPIC_TRANSFERS_SETTLED), eq(0), eq(10L), eq("TRX-REGULAR"), any());
        verifyNoInteractions(eventProducer);
    }

    @Test
    @DisplayName("TransferFraudDetectorConsumer triggers FraudAlertEvent when amount >= threshold")
    void testFraudDetectorAboveThreshold() {
        TransferFraudDetectorConsumer consumer = new TransferFraudDetectorConsumer(
                eventProducer, eventsTracker, objectMapper);
        ReflectionTestUtils.setField(consumer, "highValueThreshold", new BigDecimal("100000000.00"));

        TransferSettledEvent event = TransferSettledEvent.builder()
                .transferReference("TRX-AML-ALERT")
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("150000000.00"))
                .currency("IDR")
                .settledAt(Instant.now())
                .build();

        ConsumerRecord<String, Object> record = new ConsumerRecord<>(
                KafkaConfig.TOPIC_TRANSFERS_SETTLED, 0, 11L, "TRX-AML-ALERT", event);

        consumer.evaluateSettledTransfer(record);

        verify(eventsTracker).recordEvent(eq(KafkaConfig.TOPIC_TRANSFERS_SETTLED), eq(0), eq(11L), eq("TRX-AML-ALERT"), any());
        ArgumentCaptor<FraudAlertEvent> alertCaptor = ArgumentCaptor.forClass(FraudAlertEvent.class);
        verify(eventProducer).publishFraudAlert(alertCaptor.capture());

        FraudAlertEvent captured = alertCaptor.getValue();
        assertEquals("TRX-AML-ALERT", captured.getTransferReference());
        assertEquals("CRITICAL", captured.getSeverity());
        assertEquals("HIGH_VALUE_TRANSACTION", captured.getAlertType());
    }

    @Test
    @DisplayName("TransferFraudDetectorConsumer handles corrupt payload gracefully")
    void testFraudDetectorErrorHandling() {
        TransferFraudDetectorConsumer consumer = new TransferFraudDetectorConsumer(
                eventProducer, eventsTracker, objectMapper);

        ConsumerRecord<String, Object> record = new ConsumerRecord<>(
                KafkaConfig.TOPIC_TRANSFERS_SETTLED, 0, 12L, "TRX-ERR", "not-a-valid-event");

        assertDoesNotThrow(() -> consumer.evaluateSettledTransfer(record));
    }

    @Test
    @DisplayName("TransferNotificationConsumer records fraud alerts to tracker")
    void testNotificationConsumer() {
        TransferNotificationConsumer consumer = new TransferNotificationConsumer(eventsTracker, objectMapper);

        FraudAlertEvent alert = FraudAlertEvent.builder()
                .alertId("alert-1")
                .transferReference("TRX-103")
                .severity("CRITICAL")
                .triggerReason("High volume")
                .build();

        ConsumerRecord<String, Object> record = new ConsumerRecord<>(
                KafkaConfig.TOPIC_FRAUD_ALERTS, 0, 5L, "TRX-103", alert);

        consumer.onFraudAlert(record);

        verify(eventsTracker).recordEvent(eq(KafkaConfig.TOPIC_FRAUD_ALERTS), eq(0), eq(5L), eq("TRX-103"), any());
    }

    @Test
    @DisplayName("TransferNotificationConsumer handles errors gracefully")
    void testNotificationConsumerErrorHandling() {
        TransferNotificationConsumer consumer = new TransferNotificationConsumer(eventsTracker, objectMapper);

        ConsumerRecord<String, Object> record = new ConsumerRecord<>(
                KafkaConfig.TOPIC_FRAUD_ALERTS, 0, 6L, "TRX-104", "invalid-alert-object");

        assertDoesNotThrow(() -> consumer.onFraudAlert(record));
    }
}
