package com.indibank.core.domain.model;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;

@Entity
@Table(name = "OUTBOX_EVENTS", indexes = {
        @Index(name = "IDX_OUTBOX_PENDING", columnList = "STATUS, CREATED_AT")
})
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class OutboxEvent {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "EVENT_ID", nullable = false, unique = true, length = 64)
    private String eventId;

    @Column(name = "AGGREGATE_TYPE", nullable = false, length = 50)
    private String aggregateType;

    @Column(name = "AGGREGATE_ID", nullable = false, length = 64)
    private String aggregateId;

    @Column(name = "EVENT_TYPE", nullable = false, length = 50)
    private String eventType;

    @Lob
    @Column(name = "PAYLOAD", nullable = false)
    private String payload;

    @Column(name = "STATUS", nullable = false, length = 20)
    @Builder.Default
    private String status = "PENDING"; // PENDING, PUBLISHED, FAILED

    @Column(name = "RETRY_COUNT", nullable = false)
    @Builder.Default
    private Integer retryCount = 0;

    @CreationTimestamp
    @Column(name = "CREATED_AT", nullable = false, updatable = false)
    private Instant createdAt;

    @Column(name = "PROCESSED_AT")
    private Instant processedAt;
}
