package com.event.backend.service;

import com.event.backend.repository.*;
import org.springframework.stereotype.Service;

import java.sql.SQLException;
import java.util.List;


@Service
public class FindService {

    private FindRepository findRepository;
    public FindService(FindRepository findRepository) {
        this.findRepository = findRepository;
    }

    public List findbrand(String brand) throws SQLException {
        return findRepository.findbrand(brand);
    }
    public List findevent(String brand, String event) throws SQLException {
        return findRepository.findevent(brand, event);
    }
    public List findname(String brand, String event, String name) throws SQLException {
        return findRepository.findname(brand, event, name);
    }
}