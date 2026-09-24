package com.indibank.core.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "Kafka event stream message snapshot")
public class StreamEventDto {
    private String topic;
    private Integer partition;
    private Long offset;
    private String key;
    private Object payload;
    private Instant timestamp;
}
