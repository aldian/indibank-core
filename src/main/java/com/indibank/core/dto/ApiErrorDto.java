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
@Schema(description = "RFC 7807 compliant error format")
public class ApiErrorDto {
    private int status;
    private String code;
    private String message;
    private String details;
    private Instant timestamp;
}
