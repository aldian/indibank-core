package com.indibank.core.service;

import com.indibank.core.dto.AccountBalanceResponseDto;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.time.Duration;

@Slf4j
@Service
@RequiredArgsConstructor
public class AccountBalanceCacheService {

    private final RedisTemplate<String, Object> redisTemplate;
    private static final String CACHE_PREFIX = "indibank:cache:balance:";
    private static final Duration DEFAULT_TTL = Duration.ofMinutes(5);

    public AccountBalanceResponseDto getCachedBalance(String accountNumber) {
        String key = CACHE_PREFIX + accountNumber;
        try {
            Object cached = redisTemplate.opsForValue().get(key);
            if (cached instanceof AccountBalanceResponseDto balanceDto) {
                balanceDto.setCached(true);
                return balanceDto;
            }
        } catch (Exception e) {
            log.warn("Error reading balance from Redis cache for account {}", accountNumber, e);
        }
        return null;
    }

    public void cacheBalance(String accountNumber, AccountBalanceResponseDto balanceDto) {
        String key = CACHE_PREFIX + accountNumber;
        try {
            balanceDto.setCached(false);
            redisTemplate.opsForValue().set(key, balanceDto, DEFAULT_TTL);
            log.debug("Cached balance for account {} in Redis", accountNumber);
        } catch (Exception e) {
            log.warn("Error writing balance to Redis cache for account {}", accountNumber, e);
        }
    }

    public void evictBalance(String accountNumber) {
        String key = CACHE_PREFIX + accountNumber;
        try {
            redisTemplate.delete(key);
            log.debug("Evicted balance cache for account {}", accountNumber);
        } catch (Exception e) {
            log.warn("Error evicting balance cache for account {}", accountNumber, e);
        }
    }
}
