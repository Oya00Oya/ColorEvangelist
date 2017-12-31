package com.heitian.ssm.controller;

import com.alibaba.fastjson.JSONObject;
import org.apache.commons.io.FileUtils;
import org.apache.log4j.Logger;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import java.awt.image.BufferedImage;
import java.io.*;
import java.net.Socket;
import java.util.HashMap;
import java.util.Map;

import java.io.BufferedInputStream;


/**
 * Created by GWY on 2017/7/10.
 */
@Controller

public class testController {
    private Logger log = Logger.getLogger(testController.class);

    @RequestMapping("/index.do")
    public String test1(HttpServletRequest request, Model model) {

        log.info("test");
        return "index";
    }

    @RequestMapping(value = "/upload/sketch.do")
    @ResponseBody
    public String uploadSketch(@RequestParam("file") MultipartFile sketchFile, HttpServletRequest request) throws IOException {
        log.info("uploadSketch");
        long time = System.currentTimeMillis();
        if (sketchFile.isEmpty()) {
            return null;
        }
        log.info("文件不为空");
        String sessionId = request.getSession().getId();

//        System.out.println(sketchFile.getOriginalFilename()); //result: u=215538090,863306364&fm=11&gp=0.jpg
        // String realPath = request.getSession().getServletContext().getRealPath("/upload");//将文件保存在当前工程下的一个upload文件
        //System.out.println(realPath);

        String fileNameSketch = inputFileNameBuilder(sessionId,time);//现在的文件名是时间戳加原文件名，出现图片相同时，读取不出来的bug
        FileUtils.copyInputStreamToFile(sketchFile.getInputStream(), new File("../webapps/ROOT/func/input/sketch", fileNameSketch));//将文件的输入流输出到一个新的文件

        try {
            String command = "python ../webapps/ROOT/func/sketch.py" + " ../webapps/ROOT/func/input/sketch/" + fileNameSketch + " " + "../webapps/ROOT/func/output/sketch/" + outputFileNameBuilder(sessionId,time);
            log.info("command:" + command);
            final Process p1 = Runtime.getRuntime().exec(command);
            new Thread(new Runnable() {
                public void run() {
                    BufferedReader br = new BufferedReader(
                            new InputStreamReader(p1.getInputStream()));
                    try {
                        String line1 = null;
                        int i = 0;
                        while ((line1 = br.readLine()) != null) {
                            System.out.println(line1);
                            if (line1.equals("Success")) {
                                System.out.println("py process is failed?");
                                break;
                            } else {

                            }

                        }

                        br.close();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }).start();
            BufferedReader br = null;
            br = new BufferedReader(new InputStreamReader(p1.getErrorStream()));
            String line = null;
            while ((line = br.readLine()) != null) {
                System.out.println(line);
            }
            p1.waitFor();
            br.close();
            p1.destroy();
        } catch (Exception e) {
            e.printStackTrace();
        }


        return outputFileNameBuilder(sessionId,time);
    }


    @RequestMapping(value = "/upload/colorization.do")
    @ResponseBody
    public String uploadColorization(@RequestParam("ref") MultipartFile refFile, @RequestParam("line") MultipartFile lineFile, HttpServletRequest request) throws IOException {
        log.info("uploadColorization");
        if (lineFile.isEmpty() || refFile.isEmpty()) {
            return null;
        }
        log.info("文件不为空");
        System.out.println(lineFile.getOriginalFilename());
        final Long time = System.currentTimeMillis();
        String sessionId = request.getSession().getId();
        String fileNameRef = inputFileNameBuilder(sessionId,time);//现在的文件名是时间戳加原文件名，出现图片相同时，读取不出来的bug
        String fileNameLine = inputFileNameBuilder(sessionId,time);
        log.info("time" + "value:" + time);
        //String realPath = request.getSession().getServletContext().getRealPath("/upload");//将文件保存在当前工程下的一个upload文件
        System.out.println(fileNameRef + "  " + fileNameLine);

        FileUtils.copyInputStreamToFile(lineFile.getInputStream(), new File("../webapps/ROOT/func/input/colorization/line", fileNameLine));//将文件的输入流输出到一个新的文件
        FileUtils.copyInputStreamToFile(refFile.getInputStream(), new File("../webapps/ROOT/func/input/colorization/pic", fileNameRef));
        String pathRef = "../webapps/ROOT/func/input/colorization/pic/" + fileNameRef;//背景图片目录以及图片名称
        String pathLine = "../webapps/ROOT/func/input/colorization/line/" + fileNameLine;//图片线条目录名称
       //下面与深度学习框架交互

        try {
            // 1、创建客户端Socket，指定服务器地址和端口
            // Socket socket=new Socket("127.0.0.1",5200);
            Socket socket = new Socket("127.0.0.1", 1230);
            System.out.println("客户端启动成功");
            // 2、获取输出流，向服务器端发送信息
            // 向本机的52000端口发出客户请求
            // 由系统标准输入设备构造BufferedReader对象
            PrintWriter write = new PrintWriter(socket.getOutputStream());
            String sendData = String.format("{\"hint\":\"%s\",\"sketch\":\"%s\",\"out\":\"%s\"}", pathRef, pathLine, "../webapps/ROOT/func/output/colorization/"+ outputFileNameBuilder(sessionId,time));
            log.info(sendData);
            write.write(sendData);
            write.flush();
            log.info("data send success");
            // 由Socket对象得到输出流，并构造PrintWriter对象
            //3、获取输入流，并读取服务器端的响应信息
            BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            // 由Socket对象得到输入流，并构造相应的BufferedReader对象
            String readline;
            readline = br.readLine(); // 从系统标准输入读入一字符串
            log.info("data received from server:" + readline);
            //4、关闭资源
            write.close(); // 关闭Socket输出流
            log.info("writer closed");
            br.close(); // 关闭Socket输入流
            socket.close(); // 关闭Socket

        } catch (Exception e) {
            System.out.println("can not listen to:" + e);// 出错，打印出错信息
        }
        return outputFileNameBuilder(sessionId,time);
    }





    public String inputFileNameBuilder(String sessionId,Long time){
        return sessionId + "_" +time + ".png";
    }
    public String outputFileNameBuilder(String sessionId,Long time){
        return sessionId + "_" +time + "_out.png";
    }
}
