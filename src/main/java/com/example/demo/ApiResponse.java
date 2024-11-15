package com.example.demo;

public class ApiResponse {
    private int code;
    private String message;
    private String data;

    public ApiResponse(int code, String message, String data) {
        this.code = code;
        this.message = message;
        this.data = data;
    }

    // Getters and Setters
}
