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

    // 根路径映射到 home.html
    @GetMapping("/")
    public String defaultHomePage(Model model) {
        model.addAttribute("message", "fdf的网站");
        return "home";
    }

    // /home 路径也映射到 home.html
    @GetMapping("/home")
    public String homePage(Model model) {
        model.addAttribute("message", "fdf的网站");
        return "home";
    }

    // 处理 /generate POST 请求，生成文本并返回到 home.html
    @PostMapping("/generate")
    public String generateText(@RequestParam("prompt") String prompt, Model model) {
        String response = languageModelService.generateText(prompt);
        model.addAttribute("response", response);
        return "home";
    }

    // /chatbox 路径映射到 chatbox.html
    @GetMapping("/chatbox")
    public String chatboxPage() {
        return "chatbox";
    }
}