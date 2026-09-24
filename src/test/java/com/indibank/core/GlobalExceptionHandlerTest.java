package com.indibank.core;

import com.indibank.core.controller.GlobalExceptionHandler;
import com.indibank.core.dto.ApiErrorDto;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.core.MethodParameter;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.MissingRequestHeaderException;

import java.lang.reflect.Method;
import java.util.List;
import java.util.NoSuchElementException;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class GlobalExceptionHandlerTest {

    private final GlobalExceptionHandler handler = new GlobalExceptionHandler();

    @Test
    @DisplayName("Should handle NoSuchElementException with 404")
    void testHandleNotFound() {
        ResponseEntity<ApiErrorDto> response = handler.handleNotFound(new NoSuchElementException("Account not found"));
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("RESOURCE_NOT_FOUND", response.getBody().getCode());
        assertEquals("Account not found", response.getBody().getMessage());
    }

    @Test
    @DisplayName("Should handle IllegalArgumentException with 422")
    void testHandleBadRequest() {
        ResponseEntity<ApiErrorDto> response = handler.handleBadRequest(new IllegalArgumentException("Invalid amount"));
        assertEquals(HttpStatus.UNPROCESSABLE_ENTITY, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("VALIDATION_ERROR", response.getBody().getCode());
        assertEquals("Invalid amount", response.getBody().getMessage());
    }

    @Test
    @DisplayName("Should handle IllegalStateException with CONFLICT when in-progress")
    void testHandleConflict() {
        ResponseEntity<ApiErrorDto> response = handler.handleConflictOrState(
                new IllegalStateException("A transfer with this idempotency key is already in progress."));
        assertEquals(HttpStatus.CONFLICT, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("STATE_CONFLICT", response.getBody().getCode());
    }

    @Test
    @DisplayName("Should handle IllegalStateException with 422 when not in-progress")
    void testHandleStateOther() {
        ResponseEntity<ApiErrorDto> response = handler.handleConflictOrState(
                new IllegalStateException("Account is not ACTIVE"));
        assertEquals(HttpStatus.UNPROCESSABLE_ENTITY, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("STATE_CONFLICT", response.getBody().getCode());
    }

    @Test
    @DisplayName("Should handle MissingRequestHeaderException with 400")
    void testHandleMissingHeader() throws Exception {
        Method method = getClass().getDeclaredMethod("dummyMethod", String.class);
        MethodParameter param = new MethodParameter(method, 0);
        MissingRequestHeaderException ex = new MissingRequestHeaderException("Idempotency-Key", param);

        ResponseEntity<ApiErrorDto> response = handler.handleMissingHeader(ex);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("MISSING_REQUIRED_HEADER", response.getBody().getCode());
        assertTrue(response.getBody().getMessage().contains("Idempotency-Key"));
    }

    @Test
    @DisplayName("Should handle MethodArgumentNotValidException with 400")
    void testHandleValidationErrors() {
        BindingResult bindingResult = mock(BindingResult.class);
        FieldError fieldError = new FieldError("object", "amount", "must be greater than 0");
        when(bindingResult.getFieldErrors()).thenReturn(List.of(fieldError));

        MethodArgumentNotValidException ex = new MethodArgumentNotValidException(null, bindingResult);

        ResponseEntity<ApiErrorDto> response = handler.handleValidationErrors(ex);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("INVALID_PAYLOAD", response.getBody().getCode());
        assertTrue(response.getBody().getDetails().contains("amount: must be greater than 0"));
    }

    @Test
    @DisplayName("Should handle generic Exception with 500")
    void testHandleGeneric() {
        ResponseEntity<ApiErrorDto> response = handler.handleGeneric(new RuntimeException("Database timeout"));
        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("INTERNAL_SERVER_ERROR", response.getBody().getCode());
        assertEquals("Database timeout", response.getBody().getDetails());
    }

    @SuppressWarnings("unused")
    private void dummyMethod(String header) {}
}
