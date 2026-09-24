package com.indibank.core.controller;

import com.indibank.core.dto.ApiErrorDto;
import com.indibank.core.dto.TransferRequestDto;
import com.indibank.core.dto.TransferResponseDto;
import com.indibank.core.service.TransferService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
@RequestMapping("/api/v1/transfers")
@RequiredArgsConstructor
@Tag(name = "Transfers", description = "Interbank & Intra-bank Fund Transfer Operations")
public class TransferController {

    private final TransferService transferService;

    @PostMapping
    @Operation(
            summary = "Initiate an Idempotent Fund Transfer",
            description = "Executes real-time fund transfer between accounts with Redis idempotency guard, " +
                    "distributed lock, Oracle ACID double-entry ledger, and Kafka event streaming."
    )
    @ApiResponse(responseCode = "201", description = "Transfer executed and settled successfully",
            content = @Content(schema = @Schema(implementation = TransferResponseDto.class)))
    @ApiResponse(responseCode = "200", description = "Idempotent replay: original transfer response returned",
            content = @Content(schema = @Schema(implementation = TransferResponseDto.class)))
    @ApiResponse(responseCode = "400", description = "Invalid request payload",
            content = @Content(schema = @Schema(implementation = ApiErrorDto.class)))
    @ApiResponse(responseCode = "409", description = "Conflict / Duplicate request currently in-flight",
            content = @Content(schema = @Schema(implementation = ApiErrorDto.class)))
    @ApiResponse(responseCode = "422", description = "Business logic error (e.g. Insufficient Funds)",
            content = @Content(schema = @Schema(implementation = ApiErrorDto.class)))
    public ResponseEntity<TransferResponseDto> initiateTransfer(
            @Parameter(description = "Client UUID idempotency key", required = true, example = "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d")
            @RequestHeader(name = "Idempotency-Key") String idempotencyKey,
            @Parameter(description = "Distributed trace correlation ID", required = false)
            @RequestHeader(name = "X-Correlation-ID", required = false) String correlationId,
            @Valid @RequestBody TransferRequestDto request) {

        TransferResponseDto response = transferService.processTransfer(idempotencyKey, request);

        HttpHeaders headers = new HttpHeaders();
        headers.set("Idempotency-Key", idempotencyKey);
        if (correlationId != null) {
            headers.set("X-Correlation-ID", correlationId);
        }

        return new ResponseEntity<>(response, headers, HttpStatus.CREATED);
    }

    @GetMapping("/{referenceNumber}")
    @Operation(summary = "Query Transfer by Reference Number")
    @ApiResponse(responseCode = "200", description = "Transfer record found",
            content = @Content(schema = @Schema(implementation = TransferResponseDto.class)))
    @ApiResponse(responseCode = "404", description = "Transfer reference not found",
            content = @Content(schema = @Schema(implementation = ApiErrorDto.class)))
    public ResponseEntity<TransferResponseDto> getTransferByReference(
            @PathVariable String referenceNumber) {
        TransferResponseDto response = transferService.getTransferByReference(referenceNumber);
        return ResponseEntity.ok(response);
    }
}
