package com.indibank.core;

import com.indibank.core.dto.AccountBalanceResponseDto;
import com.indibank.core.service.AccountBalanceCacheService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ValueOperations;

import java.math.BigDecimal;
import java.time.Duration;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AccountBalanceCacheServiceTest {

    @Mock
    private RedisTemplate<String, Object> redisTemplate;

    @Mock
    private ValueOperations<String, Object> valueOperations;

    @InjectMocks
    private AccountBalanceCacheService cacheService;

    @BeforeEach
    void setUp() {
        lenient().when(redisTemplate.opsForValue()).thenReturn(valueOperations);
    }

    @Test
    @DisplayName("Should return cached balance when found in Redis")
    void shouldReturnCachedBalance() {
        AccountBalanceResponseDto dto = AccountBalanceResponseDto.builder()
                .accountNumber("1001002001")
                .balance(new BigDecimal("50000.00"))
                .cached(false)
                .build();

        when(valueOperations.get("indibank:cache:balance:1001002001")).thenReturn(dto);

        AccountBalanceResponseDto result = cacheService.getCachedBalance("1001002001");

        assertNotNull(result);
        assertTrue(result.isCached());
    }

    @Test
    @DisplayName("Should return null on cache miss or wrong type")
    void shouldReturnNullOnCacheMiss() {
        when(valueOperations.get("indibank:cache:balance:1001002001")).thenReturn(null);

        AccountBalanceResponseDto result = cacheService.getCachedBalance("1001002001");
        assertNull(result);

        when(valueOperations.get("indibank:cache:balance:1001002001")).thenReturn("unexpected-string");
        assertNull(cacheService.getCachedBalance("1001002001"));
    }

    @Test
    @DisplayName("Should return null gracefully when Redis throws exception on get")
    void shouldHandleExceptionOnGet() {
        when(valueOperations.get(anyString())).thenThrow(new RuntimeException("Redis connection error"));

        AccountBalanceResponseDto result = cacheService.getCachedBalance("1001002001");
        assertNull(result);
    }

    @Test
    @DisplayName("Should cache balance successfully in Redis")
    void shouldCacheBalance() {
        AccountBalanceResponseDto dto = AccountBalanceResponseDto.builder()
                .accountNumber("1001002001")
                .balance(new BigDecimal("50000.00"))
                .build();

        cacheService.cacheBalance("1001002001", dto);

        verify(valueOperations).set(eq("indibank:cache:balance:1001002001"), eq(dto), any(Duration.class));
        assertFalse(dto.isCached());
    }

    @Test
    @DisplayName("Should handle exception gracefully when Redis throws on set")
    void shouldHandleExceptionOnSet() {
        AccountBalanceResponseDto dto = AccountBalanceResponseDto.builder().accountNumber("1001002001").build();
        doThrow(new RuntimeException("Redis error")).when(valueOperations).set(anyString(), any(), any(Duration.class));

        assertDoesNotThrow(() -> cacheService.cacheBalance("1001002001", dto));
    }

    @Test
    @DisplayName("Should evict balance from Redis")
    void shouldEvictBalance() {
        cacheService.evictBalance("1001002001");

        verify(redisTemplate).delete("indibank:cache:balance:1001002001");
    }

    @Test
    @DisplayName("Should handle exception gracefully when Redis throws on delete")
    void shouldHandleExceptionOnDelete() {
        doThrow(new RuntimeException("Redis error")).when(redisTemplate).delete(anyString());

        assertDoesNotThrow(() -> cacheService.evictBalance("1001002001"));
    }
}
