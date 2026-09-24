package com.indibank.core.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.servers.Server;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("IndiBank Core Transaction & Ledger API")
                        .version("1.0.0")
                        .description("High-Throughput Core Banking Interbank Fund Transfer & Event-Driven Ledger System.\n" +
                                "Showcases Java 21, Apache Kafka, Redis, and Oracle DB.")
                        .contact(new Contact()
                                .name("IndiBank Core Engineering")
                                .email("engineering@indibank.com")
                                .url("https://indibank.aldianapps.com"))
                        .license(new License()
                                .name("Apache 2.0")
                                .url("https://www.apache.org/licenses/LICENSE-2.0")))
                .servers(List.of(
                        new Server().url("https://indibank.aldianapps.com").description("Production GKE Environment"),
                        new Server().url("http://localhost:8080").description("Local Development Environment")
                ));
    }
}
