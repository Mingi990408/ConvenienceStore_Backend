package com.event.backend.repository;
import com.event.backend.dto.FindDto;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

@Repository
public class FindRepository {
    // 의존성 주입
    private DataSource dataSource;
    public FindRepository(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public List<FindDto> findbrand (String brand) throws SQLException {

        String sql = "select * from cvs where brand = ?";
        ArrayList pr = new ArrayList<String>();
        // DB 연결을 위한 객체들
        Connection conn = null;
        PreparedStatement ps = null;
        ResultSet rs = null;

        List<FindDto> itemlist = new ArrayList();

        // try-catch문
        try {
            conn = dataSource.getConnection();
            ps = conn.prepareStatement(sql);
            ps.setString(1, brand);
            rs = ps.executeQuery(); // 객체 반환

            while (rs.next()) {
                int Id = rs.getInt("id");
                String Brand = rs.getString("brand");
                String Event  = rs.getString("event");
                String Name = rs.getString("name");
                String Price = rs.getString("price");
                String Img = rs.getString("img");

                FindDto findDto = new FindDto(Id,Brand,Event,Name,Price,Img);
                itemlist.add(findDto);
            }
            return itemlist;
        }
        catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    public List<FindDto> findevent (String brand, String event) throws SQLException {

        String sql = "select * from cvs where brand = ? and event = ?";
        Connection conn = null;
        PreparedStatement ps = null;
        ResultSet rs = null;

        List<FindDto> itemlist = new ArrayList();

        // try-catch문
        try {
            conn = dataSource.getConnection();
            ps = conn.prepareStatement(sql);
            ps.setString(1, brand);
            ps.setString(2, event);
            rs = ps.executeQuery(); // 객체 반환

            while (rs.next()) {
                int Id = rs.getInt("id");
                String Brand = rs.getString("brand");
                String Event  = rs.getString("event");
                String Name = rs.getString("name");
                String Price = rs.getString("price");
                String Img = rs.getString("img");

                FindDto findDto = new FindDto(Id,Brand,Event,Name,Price,Img);
                itemlist.add(findDto);
            }
            return itemlist;
        }
        catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    public List<FindDto> findname (String brand, String event, String name) throws SQLException {

        String sql = "select * from cvs where brand = ? and event = ? and name  like CONCAT('%', ? ,'%' )";

        Connection conn = null;
        PreparedStatement ps = null;
        ResultSet rs = null;

        List<FindDto> itemlist = new ArrayList();

        // try-catch문
        try {
            conn = dataSource.getConnection();
            ps = conn.prepareStatement(sql);
            ps.setString(1, brand);
            ps.setString(2, event);
            ps.setString(3, name);
            rs = ps.executeQuery(); // 객체 반환

            while (rs.next()) {
                int Id = rs.getInt("id");
                String Brand = rs.getString("brand");
                String Event  = rs.getString("event");
                String Name = rs.getString("name");
                String Price = rs.getString("price");
                String Img = rs.getString("img");

                FindDto findDto = new FindDto(Id,Brand,Event,Name,Price,Img);
                itemlist.add(findDto);
            }
            return itemlist;
        }
        catch (SQLException e) {
            e.printStackTrace();
        }
        return null;

    }
}