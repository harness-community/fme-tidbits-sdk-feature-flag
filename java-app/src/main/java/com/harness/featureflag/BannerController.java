package com.harness.featureflag;

import io.split.client.SplitClient;
import io.split.client.SplitClientConfig;
import io.split.client.SplitFactory;
import io.split.client.SplitFactoryBuilder;
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
public class BannerController {

    // Use "localhost" for local testing, or replace with your real Server-side SDK key
    @Value("${fme.sdk.key:localhost}")
    private String sdkKey;

    // Path to local flags file for localhost mode testing
    @Value("${fme.flags.file:src/main/resources/flags.yaml}")
    private String flagsFile;

    private SplitClient splitClient;

    private static final String FLAG_NAME = "show-discount-banner";


    @PostConstruct
    public void init() throws Exception, InterruptedException {
        SplitFactory factory;

        if ("localhost".equals(sdkKey)) {
            SplitClientConfig config = SplitClientConfig.builder()
                    .splitFile(flagsFile)
                    .setBlockUntilReadyTimeout(5000)
                    .build();
            factory = SplitFactoryBuilder.build("localhost", config);
        } else {
            SplitClientConfig config = SplitClientConfig.builder()
                    .setBlockUntilReadyTimeout(10000)
                    .build();
            factory = SplitFactoryBuilder.build(sdkKey, config);
        }

        splitClient = factory.client();
        splitClient.blockUntilReady(); // wait until SDK is ready
        System.out.println("Harness FME Java SDK initialized. Mode: " +
                ("localhost".equals(sdkKey) ? "localhost" : "connected"));
    }

    @GetMapping("/banner")
    public Map<String, Object> getBannerConfig(
            @RequestParam(defaultValue = "user_anonymous") String userId) {

        String treatment = splitClient.getTreatment(userId, FLAG_NAME);

        Map<String, Object> response = new HashMap<>();
        response.put("userId", userId);
        response.put("flag", FLAG_NAME);
        response.put("treatment", treatment);

        if ("on".equals(treatment)) {
            response.put("showBanner", true);
            response.put("message", "🎉 10% off today! Use code HARNESS10");
        } else {
            response.put("showBanner", false);
            response.put("message", null);
        }

        return response;
    }

    @PreDestroy
    public void cleanup() {
        if (splitClient != null) {
            splitClient.destroy();
        }
    }
}
