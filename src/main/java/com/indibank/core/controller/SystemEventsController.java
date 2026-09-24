package com.indibank.core.controller;

import com.indibank.core.dto.StreamEventDto;
import com.indibank.core.event.RecentEventsTracker;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/v1/events")
@RequiredArgsConstructor
@Tag(name = "System", description = "Health Checks & Operational Telemetry")
public class SystemEventsController {

    private final RecentEventsTracker eventsTracker;

    @GetMapping("/recent")
    @Operation(summary = "Query Recent Kafka Stream Events (Demo Inspection)",
            description = "Returns latest Kafka event stream messages received by the consumer (settled transfers, AML fraud alerts).")
    public ResponseEntity<List<StreamEventDto>> getRecentEvents() {
        return ResponseEntity.ok(eventsTracker.getRecentEvents());
    }
}
