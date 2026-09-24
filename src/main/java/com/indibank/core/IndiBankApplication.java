package com.indibank.core;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class IndiBankApplication {

    public static void main(String[] args) {
        SpringApplication.run(IndiBankApplication.class, args);
    }
}
