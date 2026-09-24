package com.indibank.core.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.script.DefaultRedisScript;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.util.Collections;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class DistributedLockService {

    private final StringRedisTemplate stringRedisTemplate;

    private static final String LOCK_PREFIX = "indibank:lock:account:";
    private static final String RELEASE_LOCK_LUA =
            "if redis.call('get', KEYS[1]) == ARGV[1] then " +
            "    return redis.call('del', KEYS[1]) " +
            "else " +
            "    return 0 " +
            "end";

    /**
     * Attempts to acquire a distributed lock for an account.
     * @param accountNumber The account to lock
     * @param ttl Duration before auto-expiry
     * @return Lock token if acquired, or null if lock is held by another process
     */
    public String acquireLock(String accountNumber, Duration ttl) {
        String lockKey = LOCK_PREFIX + accountNumber;
        String lockToken = UUID.randomUUID().toString();
        Boolean success = stringRedisTemplate.opsForValue().setIfAbsent(lockKey, lockToken, ttl);
        if (Boolean.TRUE.equals(success)) {
            log.debug("Acquired distributed lock for account {} with token {}", accountNumber, lockToken);
            return lockToken;
        }
        log.warn("Failed to acquire distributed lock for account {}", accountNumber);
        return null;
    }

    /**
     * Releases the lock safely using Lua atomic comparison.
     */
    public boolean releaseLock(String accountNumber, String lockToken) {
        if (lockToken == null) return false;
        String lockKey = LOCK_PREFIX + accountNumber;
        DefaultRedisScript<Long> script = new DefaultRedisScript<>(RELEASE_LOCK_LUA, Long.class);
        Long result = stringRedisTemplate.execute(script, Collections.singletonList(lockKey), lockToken);
        boolean released = result != null && result > 0;
        if (released) {
            log.debug("Released distributed lock for account {}", accountNumber);
        } else {
            log.warn("Lock for account {} already expired or held by another token", accountNumber);
        }
        return released;
    }
}
