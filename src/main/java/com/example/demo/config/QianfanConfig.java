// package com.example.demo.config;

// import com.baidubce.auth.DefaultBceCredentials;
// import com.baidubce.services.qianfan.QianfanClient;
// import com.baidubce.services.qianfan.QianfanClientConfiguration;
// import org.springframework.beans.factory.annotation.Value;
// import org.springframework.context.annotation.Bean;
// import org.springframework.context.annotation.Configuration;

// @Configuration
// public class QianfanConfig {

//     @Value("${qianfan.accessKey}")
//     private String accessKey;

//     @Value("${qianfan.secretKey}")
//     private String secretKey;

//     @Bean
//     public QianfanClient qianfanClient() {
//         QianfanClientConfiguration config = new QianfanClientConfiguration();
//         config.setCredentials(new DefaultBceCredentials(accessKey, secretKey));
//         return new QianfanClient(config);
//     }
// }
