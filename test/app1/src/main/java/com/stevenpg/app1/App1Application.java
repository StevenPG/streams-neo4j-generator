package com.stevenpg.app1;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.util.function.Supplier;

@SpringBootApplication
public class App1Application {

    public static void main(String[] args) {
        SpringApplication.run(App1Application.class, args);
    }

    @Bean
    public Supplier<String> initialPublisher() {
        return () -> "testEvent";
    }

}
