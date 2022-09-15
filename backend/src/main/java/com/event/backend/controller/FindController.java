package com.event.backend.controller;

import com.event.backend.service.FindService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.sql.SQLException;
import java.util.List;
@RequiredArgsConstructor
@RestController
public class FindController {

    private final FindService findService;

    @GetMapping("findbrand")
    public List findbrand(@RequestParam String brand) throws SQLException {
        List itemList = findService.findbrand(brand);
        System.out.println(brand + "\n");
        return itemList;
    }
    @GetMapping("findevent")
    public List findevent(@RequestParam String brand,
                          @RequestParam String event) throws SQLException {
        List itemList = findService.findevent(brand, event);
        System.out.println(brand + "\n" + event);
        return itemList;
    }
    @GetMapping("findname")
    public List findname(@RequestParam String brand,
                          @RequestParam String event,
                          @RequestParam String name) throws SQLException {
        List itemList = findService.findname(brand, event, name);
        System.out.println(brand + "\n" + event + "\n" + name);
        return itemList;
    }
}