package com.indibank.core.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.indibank.core.dto.TransferResponseDto;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;

import java.time.Duration;

@Slf4j
@Service
@RequiredArgsConstructor
public class IdempotencyService {

    private final StringRedisTemplate stringRedisTemplate;
    private final ObjectMapper objectMapper;

    private static final String IDEMPOTENCY_PREFIX = "indibank:idempotency:";
    private static final String STATE_IN_PROGRESS = "IN_PROGRESS";

    public enum IdempotencyStatus {
        ACQUIRED,
        IN_PROGRESS,
        COMPLETED
    }

    public static class IdempotencyResult {
        public final IdempotencyStatus status;
        public final TransferResponseDto cachedResponse;

        public IdempotencyResult(IdempotencyStatus status, TransferResponseDto cachedResponse) {
            this.status = status;
            this.cachedResponse = cachedResponse;
        }
    }

    /**
     * Checks and locks an idempotency key.
     */
    public IdempotencyResult checkAndLock(String idempotencyKey, Duration inProgressTtl) {
        String key = IDEMPOTENCY_PREFIX + idempotencyKey;
        Boolean isNew = stringRedisTemplate.opsForValue().setIfAbsent(key, STATE_IN_PROGRESS, inProgressTtl);

        if (Boolean.TRUE.equals(isNew)) {
            return new IdempotencyResult(IdempotencyStatus.ACQUIRED, null);
        }

        // Key already exists, read current value
        String existingVal = stringRedisTemplate.opsForValue().get(key);
        if (STATE_IN_PROGRESS.equals(existingVal)) {
            return new IdempotencyResult(IdempotencyStatus.IN_PROGRESS, null);
        }

        // It has a cached completed response
        try {
            if (existingVal != null) {
                TransferResponseDto response = objectMapper.readValue(existingVal, TransferResponseDto.class);
                return new IdempotencyResult(IdempotencyStatus.COMPLETED, response);
            }
        } catch (JsonProcessingException e) {
            log.error("Failed to parse cached response for idempotency key {}", idempotencyKey, e);
        }

        return new IdempotencyResult(IdempotencyStatus.IN_PROGRESS, null);
    }

    /**
     * Saves settled transfer response under the idempotency key with 24-hour TTL.
     */
    public void markCompleted(String idempotencyKey, TransferResponseDto response, Duration completedTtl) {
        String key = IDEMPOTENCY_PREFIX + idempotencyKey;
        try {
            String json = objectMapper.writeValueAsString(response);
            stringRedisTemplate.opsForValue().set(key, json, completedTtl);
            log.info("Idempotency key {} marked COMPLETED (TTL {}s)", idempotencyKey, completedTtl.toSeconds());
        } catch (JsonProcessingException e) {
            log.error("Failed to serialize response for idempotency key {}", idempotencyKey, e);
        }
    }

    /**
     * Deletes the idempotency key if transaction failed, allowing clean retries.
     */
    public void releaseKey(String idempotencyKey) {
        String key = IDEMPOTENCY_PREFIX + idempotencyKey;
        stringRedisTemplate.delete(key);
        log.debug("Released idempotency key {}", idempotencyKey);
    }
}
