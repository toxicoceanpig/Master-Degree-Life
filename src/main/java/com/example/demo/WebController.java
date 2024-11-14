package com.example.demo;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class WebController {

    @GetMapping("/home")
    public String homePage(Model model) {
        // 传递数据到网页 (可选)
        model.addAttribute("message", "fdf的网站");

        // 返回名为 "home" 的模板
        return "home";
    }

    @GetMapping("/chatbox")
    public String chatboxPage() {
        return "chatbox"; // 
    }

    
}