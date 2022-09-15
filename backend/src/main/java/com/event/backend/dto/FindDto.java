package com.event.backend.dto;

import lombok.*;

@Getter
@NoArgsConstructor
public class FindDto {
    private int id;
    private String brand;
    private String event;
    private String name;
    private String price;
    private String img;

    public FindDto(int id, String brand, String event, String name , String price, String img ) {
        this.id = id;
        this.brand = brand;
        this.event = event;
        this.name = name;
        this.price = price;
        this.img = img;
    }
    @Override
    public String toString(){
        return String.format("id : %d\nbrand : %s\nevent : %s\nname : %s\nprice : %s\nimg : %s",id,brand,event,name,price,img);
    }
}



