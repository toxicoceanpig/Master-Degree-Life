package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class WebController {

    @Autowired
    private LanguageModelService languageModelService;

    @GetMapping("/home")
    public String homePage(Model model) {
        model.addAttribute("message", "fdf的网站");
        return "home";
    }

    @PostMapping("/generate")
    public String generateText(@RequestParam("prompt") String prompt, Model model) {
        String response = languageModelService.generateText(prompt);
        model.addAttribute("response", response);
        return "home";
    }

    @GetMapping("/chatbox")
    public String chatboxPage() {
        return "chatbox"; // 
    }

    
}