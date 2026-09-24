package com.indibank.core;

import com.indibank.core.controller.SystemEventsController;
import com.indibank.core.dto.StreamEventDto;
import com.indibank.core.event.RecentEventsTracker;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class SystemEventsControllerTest {

    @Mock
    private RecentEventsTracker eventsTracker;

    @InjectMocks
    private SystemEventsController controller;

    @Test
    @DisplayName("Should return recent events list")
    void shouldReturnRecentEvents() {
        StreamEventDto event = StreamEventDto.builder().topic("test.topic").build();
        when(eventsTracker.getRecentEvents()).thenReturn(List.of(event));

        ResponseEntity<List<StreamEventDto>> response = controller.getRecentEvents();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(1, response.getBody().size());
        assertEquals("test.topic", response.getBody().get(0).getTopic());
    }
}
