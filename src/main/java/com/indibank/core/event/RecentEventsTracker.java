package com.indibank.core.event;

import com.indibank.core.dto.StreamEventDto;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.LinkedList;
import java.util.List;

@Component
public class RecentEventsTracker {

    private final LinkedList<StreamEventDto> recentEvents = new LinkedList<>();
    private static final int MAX_EVENTS = 50;

    public synchronized void recordEvent(String topic, int partition, long offset, String key, Object payload) {
        StreamEventDto event = StreamEventDto.builder()
                .topic(topic)
                .partition(partition)
                .offset(offset)
                .key(key)
                .payload(payload)
                .timestamp(Instant.now())
                .build();

        recentEvents.addFirst(event);
        if (recentEvents.size() > MAX_EVENTS) {
            recentEvents.removeLast();
        }
    }

    public synchronized List<StreamEventDto> getRecentEvents() {
        return List.copyOf(recentEvents);
    }
}
