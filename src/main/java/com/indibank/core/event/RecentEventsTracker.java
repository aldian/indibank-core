package com.indibank.core.event;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.indibank.core.dto.StreamEventDto;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

@Slf4j
@Component
public class RecentEventsTracker {

    private final StringRedisTemplate stringRedisTemplate;
    private final ObjectMapper objectMapper;
    private final LinkedList<StreamEventDto> inMemoryEvents = new LinkedList<>();

    private static final String REDIS_EVENTS_KEY = "indibank:events:recent";
    private static final int MAX_EVENTS = 50;

    public RecentEventsTracker() {
        this.stringRedisTemplate = null;
        ObjectMapper mapper = new ObjectMapper();
        mapper.registerModule(new JavaTimeModule());
        this.objectMapper = mapper;
    }

    @Autowired
    public RecentEventsTracker(StringRedisTemplate stringRedisTemplate, ObjectMapper objectMapper) {
        this.stringRedisTemplate = stringRedisTemplate;
        this.objectMapper = objectMapper;
    }

    public synchronized void recordEvent(String topic, int partition, long offset, String key, Object payload) {
        StreamEventDto event = StreamEventDto.builder()
                .topic(topic)
                .partition(partition)
                .offset(offset)
                .key(key)
                .payload(payload)
                .timestamp(Instant.now())
                .build();

        // 1. Maintain in-memory buffer
        inMemoryEvents.addFirst(event);
        if (inMemoryEvents.size() > MAX_EVENTS) {
            inMemoryEvents.removeLast();
        }

        // 2. Publish to distributed Redis list so all cluster pods share the stream
        if (stringRedisTemplate != null) {
            try {
                String json = objectMapper.writeValueAsString(event);
                stringRedisTemplate.opsForList().leftPush(REDIS_EVENTS_KEY, json);
                stringRedisTemplate.opsForList().trim(REDIS_EVENTS_KEY, 0, MAX_EVENTS - 1);
            } catch (Exception e) {
                log.warn("Failed to cache event in Redis list {}: {}", REDIS_EVENTS_KEY, e.getMessage());
            }
        }
    }

    public synchronized List<StreamEventDto> getRecentEvents() {
        if (stringRedisTemplate != null) {
            try {
                List<String> rawEvents = stringRedisTemplate.opsForList().range(REDIS_EVENTS_KEY, 0, MAX_EVENTS - 1);
                if (rawEvents != null && !rawEvents.isEmpty()) {
                    List<StreamEventDto> redisEvents = new ArrayList<>(rawEvents.size());
                    for (String json : rawEvents) {
                        redisEvents.add(objectMapper.readValue(json, StreamEventDto.class));
                    }
                    return redisEvents;
                }
            } catch (Exception e) {
                log.warn("Failed to fetch events from Redis list, falling back to in-memory: {}", e.getMessage());
            }
        }
        return List.copyOf(inMemoryEvents);
    }
}
