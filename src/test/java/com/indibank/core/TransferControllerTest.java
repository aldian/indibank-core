package com.indibank.core;

import com.indibank.core.controller.TransferController;
import com.indibank.core.domain.model.TransferStatus;
import com.indibank.core.dto.TransferRequestDto;
import com.indibank.core.dto.TransferResponseDto;
import com.indibank.core.service.TransferService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.math.BigDecimal;
import java.time.Instant;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class TransferControllerTest {

    @Mock
    private TransferService transferService;

    @InjectMocks
    private TransferController transferController;

    @Test
    @DisplayName("Should initiate transfer successfully with correlation id header")
    void shouldInitiateTransferWithCorrelationId() {
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("500000.00"))
                .currency("IDR")
                .description("Test")
                .build();

        TransferResponseDto mockResponse = TransferResponseDto.builder()
                .referenceNumber("TRX-12345")
                .idempotencyKey("idemp-1")
                .status(TransferStatus.SETTLED)
                .amount(new BigDecimal("500000.00"))
                .createdAt(Instant.now())
                .build();

        when(transferService.processTransfer("idemp-1", request)).thenReturn(mockResponse);

        ResponseEntity<TransferResponseDto> response = transferController.initiateTransfer(
                "idemp-1", "corr-999", request);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("TRX-12345", response.getBody().getReferenceNumber());
        assertEquals("idemp-1", response.getHeaders().getFirst("Idempotency-Key"));
        assertEquals("corr-999", response.getHeaders().getFirst("X-Correlation-ID"));
    }

    @Test
    @DisplayName("Should initiate transfer successfully without correlation id header")
    void shouldInitiateTransferWithoutCorrelationId() {
        TransferRequestDto request = TransferRequestDto.builder()
                .sourceAccountNumber("1001002001")
                .destinationAccountNumber("1001002002")
                .amount(new BigDecimal("500000.00"))
                .currency("IDR")
                .build();

        TransferResponseDto mockResponse = TransferResponseDto.builder()
                .referenceNumber("TRX-67890")
                .idempotencyKey("idemp-2")
                .status(TransferStatus.SETTLED)
                .amount(new BigDecimal("500000.00"))
                .build();

        when(transferService.processTransfer("idemp-2", request)).thenReturn(mockResponse);

        ResponseEntity<TransferResponseDto> response = transferController.initiateTransfer(
                "idemp-2", null, request);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("TRX-67890", response.getBody().getReferenceNumber());
        assertEquals("idemp-2", response.getHeaders().getFirst("Idempotency-Key"));
        assertNull(response.getHeaders().getFirst("X-Correlation-ID"));
    }

    @Test
    @DisplayName("Should query transfer by reference number")
    void shouldGetTransferByReference() {
        TransferResponseDto mockResponse = TransferResponseDto.builder()
                .referenceNumber("TRX-REF-100")
                .amount(new BigDecimal("100000.00"))
                .build();

        when(transferService.getTransferByReference("TRX-REF-100")).thenReturn(mockResponse);

        ResponseEntity<TransferResponseDto> response = transferController.getTransferByReference("TRX-REF-100");

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("TRX-REF-100", response.getBody().getReferenceNumber());
    }
}
