package com.indibank.core.integration;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.indibank.core.controller.GlobalExceptionHandler;
import com.indibank.core.controller.TransferController;
import com.indibank.core.domain.model.TransferStatus;
import com.indibank.core.dto.TransferRequestDto;
import com.indibank.core.dto.TransferResponseDto;
import com.indibank.core.service.TransferService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.NoSuchElementException;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(TransferController.class)
@Import(GlobalExceptionHandler.class)
class TransferControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private TransferService transferService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    @DisplayName("POST /api/v1/transfers - should return 201 Created on valid transfer payload")
    void shouldReturn201OnValidTransfer() throws Exception {
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("1500000.00"))
                .currency("IDR")
                .description("Vendor payment")
                .build();

        TransferResponseDto responseDto = TransferResponseDto.builder()
                .referenceNumber("TRX-20260924-1001")
                .idempotencyKey("uuid-integration-01")
                .status(TransferStatus.SETTLED)
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("1500000.00"))
                .currency("IDR")
                .description("Vendor payment")
                .journalEntryId(42L)
                .createdAt(Instant.now())
                .build();

        when(transferService.processTransfer(eq("uuid-integration-01"), any(TransferRequestDto.class)))
                .thenReturn(responseDto);

        mockMvc.perform(post("/api/v1/transfers")
                        .header("Idempotency-Key", "uuid-integration-01")
                        .header("X-Correlation-ID", "corr-web-01")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(header().string("Idempotency-Key", "uuid-integration-01"))
                .andExpect(header().string("X-Correlation-ID", "corr-web-01"))
                .andExpect(jsonPath("$.referenceNumber").value("TRX-20260924-1001"))
                .andExpect(jsonPath("$.status").value("SETTLED"))
                .andExpect(jsonPath("$.amount").value(1500000.00))
                .andExpect(jsonPath("$.journalEntryId").value(42));
    }

    @Test
    @DisplayName("POST /api/v1/transfers - should return 400 Bad Request when Idempotency-Key header is missing")
    void shouldReturn400WhenMissingIdempotencyHeader() throws Exception {
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("500000.00"))
                .currency("IDR")
                .build();

        mockMvc.perform(post("/api/v1/transfers")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("MISSING_REQUIRED_HEADER"));
    }

    @Test
    @DisplayName("POST /api/v1/transfers - should return 400 Bad Request on invalid payload (amount <= 0)")
    void shouldReturn400OnValidationFailure() throws Exception {
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("-100.00")) // Invalid amount
                .currency("IDR")
                .build();

        mockMvc.perform(post("/api/v1/transfers")
                        .header("Idempotency-Key", "uuid-bad-amount")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("INVALID_PAYLOAD"));
    }

    @Test
    @DisplayName("POST /api/v1/transfers - should return 409 Conflict when transfer is already in progress")
    void shouldReturn409OnDuplicateConcurrentTransfer() throws Exception {
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("100000.00"))
                .currency("IDR")
                .build();

        when(transferService.processTransfer(eq("uuid-conflict"), any()))
                .thenThrow(new IllegalStateException("A transfer with this idempotency key is already in progress."));

        mockMvc.perform(post("/api/v1/transfers")
                        .header("Idempotency-Key", "uuid-conflict")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.code").value("STATE_CONFLICT"));
    }

    @Test
    @DisplayName("POST /api/v1/transfers - should return 422 Unprocessable Entity on insufficient funds")
    void shouldReturn422OnInsufficientFunds() throws Exception {
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("200000000.00"))
                .currency("IDR")
                .build();

        when(transferService.processTransfer(eq("uuid-insufficient"), any()))
                .thenThrow(new IllegalArgumentException("Insufficient funds in account 1001002001"));

        mockMvc.perform(post("/api/v1/transfers")
                        .header("Idempotency-Key", "uuid-insufficient")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isUnprocessableEntity())
                .andExpect(jsonPath("$.code").value("VALIDATION_ERROR"));
    }

    @Test
    @DisplayName("GET /api/v1/transfers/{ref} - should return 200 OK when reference exists")
    void shouldReturn200OnQueryByReference() throws Exception {
        TransferResponseDto responseDto = TransferResponseDto.builder()
                .referenceNumber("TRX-REF-FOUND")
                .status(TransferStatus.SETTLED)
                .amount(new BigDecimal("250000.00"))
                .currency("IDR")
                .build();

        when(transferService.getTransferByReference("TRX-REF-FOUND")).thenReturn(responseDto);

        mockMvc.perform(get("/api/v1/transfers/TRX-REF-FOUND"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.referenceNumber").value("TRX-REF-FOUND"))
                .andExpect(jsonPath("$.status").value("SETTLED"));
    }

    @Test
    @DisplayName("GET /api/v1/transfers/{ref} - should return 404 Not Found when reference does not exist")
    void shouldReturn404OnReferenceNotFound() throws Exception {
        when(transferService.getTransferByReference("TRX-UNKNOWN"))
                .thenThrow(new NoSuchElementException("Transfer reference not found: TRX-UNKNOWN"));

        mockMvc.perform(get("/api/v1/transfers/TRX-UNKNOWN"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.code").value("RESOURCE_NOT_FOUND"));
    }
}
