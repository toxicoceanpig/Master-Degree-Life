package com.example.demo;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;

import java.util.Map;

@Service
public class LanguageModelService {

    private final RestTemplate restTemplate = new RestTemplate();

    public String generateText(String prompt) {
        String pythonApiUrl = "http://localhost:5000/api/generate";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        Map<String, String> payload = Map.of("prompt", prompt);
        HttpEntity<Map<String, String>> entity = new HttpEntity<>(payload, headers);
        ResponseEntity<String> response = restTemplate.exchange(pythonApiUrl, HttpMethod.POST, entity, String.class);

        return response.getBody();
    }
}