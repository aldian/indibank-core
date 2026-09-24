package com.indibank.core;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.indibank.core.dto.TransferResponseDto;
import com.indibank.core.service.IdempotencyService;
import com.indibank.core.service.IdempotencyService.IdempotencyResult;
import com.indibank.core.service.IdempotencyService.IdempotencyStatus;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ValueOperations;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class IdempotencyServiceTest {

    @Mock
    private StringRedisTemplate stringRedisTemplate;

    @Mock
    private ValueOperations<String, String> valueOperations;

    @Mock
    private ObjectMapper objectMapper;

    @InjectMocks
    private IdempotencyService idempotencyService;

    @BeforeEach
    void setUp() {
        lenient().when(stringRedisTemplate.opsForValue()).thenReturn(valueOperations);
    }

    @Test
    @DisplayName("Should return ACQUIRED when key is newly locked")
    void shouldAcquireNewKey() {
        when(valueOperations.setIfAbsent(anyString(), anyString(), any(Duration.class)))
                .thenReturn(Boolean.TRUE);

        IdempotencyResult result = idempotencyService.checkAndLock("new-key", Duration.ofSeconds(60));

        assertEquals(IdempotencyStatus.ACQUIRED, result.status);
        assertNull(result.cachedResponse);
    }

    @Test
    @DisplayName("Should return IN_PROGRESS when key exists and is still being processed")
    void shouldReturnInProgress() {
        when(valueOperations.setIfAbsent(anyString(), anyString(), any(Duration.class)))
                .thenReturn(Boolean.FALSE);
        when(valueOperations.get(anyString())).thenReturn("IN_PROGRESS");

        IdempotencyResult result = idempotencyService.checkAndLock("in-flight-key", Duration.ofSeconds(60));

        assertEquals(IdempotencyStatus.IN_PROGRESS, result.status);
    }

    @Test
    @DisplayName("Should return COMPLETED with cached response when settled transfer exists")
    void shouldReturnCompletedWithCachedResponse() throws JsonProcessingException {
        TransferResponseDto dto = TransferResponseDto.builder()
                .referenceNumber("TRX-CACHED")
                .build();

        when(valueOperations.setIfAbsent(anyString(), anyString(), any(Duration.class)))
                .thenReturn(Boolean.FALSE);
        when(valueOperations.get(anyString())).thenReturn("{\"referenceNumber\":\"TRX-CACHED\"}");
        when(objectMapper.readValue(anyString(), eq(TransferResponseDto.class))).thenReturn(dto);

        IdempotencyResult result = idempotencyService.checkAndLock("completed-key", Duration.ofSeconds(60));

        assertEquals(IdempotencyStatus.COMPLETED, result.status);
        assertNotNull(result.cachedResponse);
        assertEquals("TRX-CACHED", result.cachedResponse.getReferenceNumber());
    }

    @Test
    @DisplayName("Should return IN_PROGRESS when cached json parsing throws exception")
    void shouldHandleJsonParseError() throws JsonProcessingException {
        when(valueOperations.setIfAbsent(anyString(), anyString(), any(Duration.class)))
                .thenReturn(Boolean.FALSE);
        when(valueOperations.get(anyString())).thenReturn("{corrupted-json}");
        when(objectMapper.readValue(anyString(), eq(TransferResponseDto.class)))
                .thenThrow(new com.fasterxml.jackson.core.JsonParseException(null, "JSON error"));

        IdempotencyResult result = idempotencyService.checkAndLock("bad-json-key", Duration.ofSeconds(60));

        assertEquals(IdempotencyStatus.IN_PROGRESS, result.status);
    }

    @Test
    @DisplayName("Should save completed response with TTL")
    void shouldMarkCompleted() throws JsonProcessingException {
        TransferResponseDto dto = TransferResponseDto.builder().referenceNumber("TRX-1").build();
        when(objectMapper.writeValueAsString(dto)).thenReturn("{\"referenceNumber\":\"TRX-1\"}");

        idempotencyService.markCompleted("key-1", dto, Duration.ofHours(24));

        verify(valueOperations).set(eq("indibank:idempotency:key-1"), eq("{\"referenceNumber\":\"TRX-1\"}"), eq(Duration.ofHours(24)));
    }

    @Test
    @DisplayName("Should release key by deleting from Redis")
    void shouldReleaseKey() {
        idempotencyService.releaseKey("key-to-delete");

        verify(stringRedisTemplate).delete("indibank:idempotency:key-to-delete");
    }
}
