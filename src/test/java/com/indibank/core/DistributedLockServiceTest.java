package com.indibank.core;

import com.indibank.core.service.DistributedLockService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.data.redis.core.script.DefaultRedisScript;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class DistributedLockServiceTest {

    @Mock
    private StringRedisTemplate stringRedisTemplate;

    @Mock
    private ValueOperations<String, String> valueOperations;

    @InjectMocks
    private DistributedLockService lockService;

    @BeforeEach
    void setUp() {
        lenient().when(stringRedisTemplate.opsForValue()).thenReturn(valueOperations);
    }

    @Test
    @DisplayName("Should return lock token when setIfAbsent succeeds")
    void shouldAcquireLockSuccessfully() {
        when(valueOperations.setIfAbsent(anyString(), anyString(), any(Duration.class)))
                .thenReturn(Boolean.TRUE);

        String token = lockService.acquireLock("1001002001", Duration.ofSeconds(10));

        assertNotNull(token);
    }

    @Test
    @DisplayName("Should return null when lock is already acquired by another thread")
    void shouldReturnNullWhenLockBusy() {
        when(valueOperations.setIfAbsent(anyString(), anyString(), any(Duration.class)))
                .thenReturn(Boolean.FALSE);

        String token = lockService.acquireLock("1001002001", Duration.ofSeconds(10));

        assertNull(token);
    }

    @Test
    @DisplayName("Should release lock via Lua script execution")
    void shouldReleaseLockSuccessfully() {
        when(stringRedisTemplate.execute(any(DefaultRedisScript.class), anyList(), anyString()))
                .thenReturn(1L);

        boolean released = lockService.releaseLock("1001002001", "valid-token");

        assertTrue(released);
    }

    @Test
    @DisplayName("Should return false when lock token is null")
    void shouldReturnFalseWhenTokenNull() {
        boolean released = lockService.releaseLock("1001002001", null);

        assertFalse(released);
    }

    @Test
    @DisplayName("Should return false when lock expired or owned by another process")
    void shouldReturnFalseWhenLockExpired() {
        when(stringRedisTemplate.execute(any(DefaultRedisScript.class), anyList(), anyString()))
                .thenReturn(0L);

        boolean released = lockService.releaseLock("1001002001", "expired-token");

        assertFalse(released);
    }
}
