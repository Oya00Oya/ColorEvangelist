package com.heitian.ssm.controller;

import org.apache.commons.io.FileUtils;
import org.apache.log4j.Logger;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import java.awt.image.BufferedImage;
import java.io.*;


/**
 * Created by GWY on 2017/7/10.
 */
@Controller

public class testController {
    public Long re_image_name;
    private Logger log = Logger.getLogger(testController.class);

    @RequestMapping("/index.do")
    public String test1(HttpServletRequest request, Model model) {

        log.info("test");
        return "index";
    }

    @RequestMapping(value = "/upload/sketch.do")
    @ResponseBody
    public long uploadSketch(@RequestParam("file") MultipartFile sketchFile, HttpServletRequest request) throws IOException {
        log.info("uploadSketch");
        long time_sketch;
        time_sketch = System.currentTimeMillis();
        if (!sketchFile.isEmpty()) {
            log.info("文件不为空");

            System.out.println(sketchFile.getOriginalFilename());
            // String realPath = request.getSession().getServletContext().getRealPath("/upload");//将文件保存在当前工程下的一个upload文件
            //System.out.println(realPath);
            String fileNameSketch = time_sketch + ".png";//现在的文件名是时间戳加原文件名，出现图片相同时，读取不出来的bug
            FileUtils.copyInputStreamToFile(sketchFile.getInputStream(), new File("../webapps/ROOT/func/input/sketch", fileNameSketch));//将文件的输入流输出到一个新的文件

            try {
                String command = null;
                command = "python ../webapps/ROOT/func/sketch.py" + " ../webapps/ROOT/func/input/sketch/" + fileNameSketch + " " + "../webapps/ROOT/func/output/sketch/" + time_sketch + "_out.png";//这里需要修改
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

        }
        return time_sketch;
    }

    @RequestMapping(value = "/upload/colorization.do")
    @ResponseBody
    public Long uploadColorization(@RequestParam("ref") MultipartFile refFile, @RequestParam("line") MultipartFile lineFile, HttpServletRequest request) throws IOException {
        log.info("uploadColorization");
        if (!lineFile.isEmpty() || !refFile.isEmpty()) {
            log.info("文件不为空");
            System.out.println(lineFile.getOriginalFilename());
            final Long time01 = System.currentTimeMillis();
            String fileNameRef = time01 + ".png";//现在的文件名是时间戳加原文件名，出现图片相同时，读取不出来的bug
            String fileNameLine = time01 + ".png";
            log.info("time01" + "value:" + time01);
            //String realPath = request.getSession().getServletContext().getRealPath("/upload");//将文件保存在当前工程下的一个upload文件
            System.out.println(fileNameRef + "  " + fileNameLine);

            FileUtils.copyInputStreamToFile(lineFile.getInputStream(), new File("../webapps/ROOT/func/input/colorization/line", fileNameRef));//将文件的输入流输出到一个新的文件
            FileUtils.copyInputStreamToFile(refFile.getInputStream(), new File("../webapps/ROOT/func/input/colorization/pic", fileNameLine));
            String pathRef = "../webapps/ROOT/func/input/colorization/pic/" + fileNameRef;//背景图片目录以及图片名称
            String pathLine = "../webapps/ROOT/func/input/colorization/line/" + fileNameLine;//图片线条目录名称
            re_image_name = time01;
            //下面与深度学习框架交互
            try {
                final String command = "python ../webapps/ROOT/func/colorization.py" + " " + pathRef + " " + pathLine + " " + "../webapps/ROOT/func/output/colorization/" + time01 + "_out.png";
                log.info("command:" + command);
//                System.out.println(Long.toString(System.currentTimeMillis()));
                final Process p = Runtime.getRuntime().exec(command);
                new Thread(new Runnable() {


                    public void run() {

                        BufferedReader br = new BufferedReader(
                                new InputStreamReader(p.getInputStream()));
                        try {
                            String line1 = null;
                            int i = 0;
                            while ((line1 = br.readLine()) != null) {
                                System.out.println(line1);
                                if (line1.equals("Success")) {
                                    System.out.println("py process is failed");
                                    break;
                                } else {
                                    re_image_name = time01;
                                }

                            }

                            br.close();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                }).start();
                BufferedReader br = null;
                br = new BufferedReader(new InputStreamReader(p.getErrorStream()));
                String line = null;
                while ((line = br.readLine()) != null) {
                    System.out.println(line);
                }
//                System.out.println(Long.toString(System.currentTimeMillis()));
                p.waitFor();
//                System.out.println(Long.toString(System.currentTimeMillis()));
                br.close();
                p.destroy();

            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return re_image_name;
    }
}
