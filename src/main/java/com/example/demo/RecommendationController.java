package com.example.demo;

import java.util.HashMap;
import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import org.springframework.core.io.ClassPathResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.nio.file.Files;

@RestController
public class RecommendationController {

    @GetMapping("/recommendation")
    public ResponseEntity<byte[]> getRecommendation(@RequestParam String subject) {
        String imagePath;

        // 根据学科选择图片路径
        switch (subject.toLowerCase()) {
            case "math":
                imagePath = "static/images/math.png";
                break;
            case "physics":
                imagePath = "static/images/physics.jpg";
                break;
            case "chemistry":
                imagePath = "static/images/chemistry.jpeg";
                break;
            default:
                imagePath = "static/images/default.jpg";
        }

        try {
            // 读取图片文件
            ClassPathResource imgFile = new ClassPathResource(imagePath);
            byte[] imageBytes = Files.readAllBytes(imgFile.getFile().toPath());

            // 设置响应头和内容类型
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.IMAGE_JPEG); // 或 IMAGE_PNG，视图片格式而定

            return new ResponseEntity<>(imageBytes, headers, HttpStatus.OK);
        } catch (IOException e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
    }
}
