package com.heitian.ssm.controller;

import org.apache.commons.io.FileUtils;
import org.apache.log4j.Logger;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;

import javax.imageio.ImageIO;
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
    public String test1(HttpServletRequest request, Model model){

        log.info("test");
        return "index";
    }
    @RequestMapping(value = "imgUpload.do")
    @ResponseBody
    public long  imgUpload(@RequestParam("file") MultipartFile file, HttpServletRequest request) throws IOException {
        String tishi="no";
        long time_sketch;time_sketch=System.currentTimeMillis();
        log.info("imgupload");
        System.out.println("arrive here");
        if(!file.isEmpty()) {
            log.info("文件不为空");

            System.out.println(file.getOriginalFilename());

            String message ="";//现在的文件名是时间戳加原文件名，出现图片相同时，读取不出来的bug
           // String realPath = request.getSession().getServletContext().getRealPath("/upload");//将文件保存在当前工程下的一个upload文件
            //System.out.println(realPath);
            message=time_sketch+".png";
            FileUtils.copyInputStreamToFile(file.getInputStream(), new File("../webapps/ROOT/func/input/sketch", message));//将文件的输入流输出到一个新的文件

            try {
                String command=null;
                command="python ../webapps/ROOT/func/sketch.py"+" ../webapps/ROOT/func/input/sketch/"+message+" "+"../webapps/ROOT/func/output/sketch/"+time_sketch+"_out.png";//这里需要修改
                log.info("command:"+command);
                final Process p1 = Runtime.getRuntime().exec(command);
                new Thread(new Runnable() {


                    public void run() {
                        BufferedReader br = new BufferedReader(
                                new InputStreamReader(p1.getInputStream()));
                        try {
                            String line1=null;
                            int i=0;
                            while ((line1=br.readLine() )!= null)
                            {
                                System.out.println(line1);
                                if(line1.equals("Success")) {
                                    System.out.println("py process is failed?");
                                    break;
                                }
                                else {

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

            tishi="yes";//返回yes,表示存储成功，可以使用try,catch来捕捉错误，这里偷懒不用
        }
        return time_sketch;
    }
    @RequestMapping(value = "imgUpload2.do")
    @ResponseBody
    public synchronized String imgUpload2(@RequestParam("file2") MultipartFile file, HttpServletRequest request) throws IOException {
        String tishi="no";
        log.info("imgupload");
        System.out.println("arrive here");
        if(!file.isEmpty()) {
            log.info("文件不为空");
            System.out.println(file.getOriginalFilename());
            String message = System.currentTimeMillis() + file.getOriginalFilename();//现在的文件名是时间戳加原文件名，出现图片相同时，读取不出来的bug
            String realPath = request.getSession().getServletContext().getRealPath("/upload");//将文件保存在当前工程下的一个upload文件
            System.out.println(realPath);
            FileUtils.copyInputStreamToFile(file.getInputStream(), new File("D://weblearn//shortsem//web-ssm-shortsem//target//web-ssm//upload2", message));//将文件的输入流输出到一个新的文件
            message="upload/"+message;

            tishi="yes";//返回yes,表示存储成功，可以使用try,catch来捕捉错误，这里偷懒不用
        }
        return tishi;
    }
    @RequestMapping(value = "post.do")
    @ResponseBody
    public synchronized String paintUpload1(@RequestParam("ref") MultipartFile file1, @RequestParam("line") MultipartFile file, @RequestParam("id") String id,@RequestParam("blur") String blur ,HttpServletRequest request) throws IOException {
        String tishi="no";
        String message1="";
        String message2="";
        log.info("post");
        System.out.println("arrive here");
        if(!file.isEmpty()||!file1.isEmpty()) {
            log.info("文件不为空");
            System.out.println(file.getOriginalFilename());
            final Long time01=System.currentTimeMillis();
            String message = time01 +".png";//现在的文件名是时间戳加原文件名，出现图片相同时，读取不出来的bug
            String messageline=time01+".png";
            log.info("time01"+"value:"+time01);
            //String realPath = request.getSession().getServletContext().getRealPath("/upload");//将文件保存在当前工程下的一个upload文件
            System.out.println(message+"  "+messageline);

            FileUtils.copyInputStreamToFile(file.getInputStream(), new File("../webapps/func/input/colorization/line", message));//将文件的输入流输出到一个新的文件
            FileUtils.copyInputStreamToFile(file1.getInputStream(),new File("../webapps/ROOT/func/input/colorization/pic",messageline));
            message1="../webapps/ROOT/func/input/colorization/pic/"+message;//背景图片目录以及图片名称
            message2="../webapps/ROOT/func/input/colorization/line/"+messageline;//图片线条目录名称
            re_image_name=time01;
           //下面与深度学习框架交互
            try {
                String command=null;
                command="python ../webapps/ROOT/func/colorization.py"+" "+message1+" "+message2+" "+"../webapps/ROOT/func/output/colorization/"+time01+"_out.png";
                log.info("command:"+command);
                final Process p = Runtime.getRuntime().exec(command);
                new Thread(new Runnable() {


                    public void run() {
                        BufferedReader br = new BufferedReader(
                                new InputStreamReader(p.getInputStream()));
                        try {
                            String line1=null;
                            int i=0;
                            while ((line1=br.readLine() )!= null)
                            {
                                System.out.println(line1);
                                if(line1.equals("Success")) {
                                    System.out.println("py process is failed");
                                    break;
                                }
                                else {
                                    re_image_name= time01;
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
                p.waitFor();
                br.close();
                p.destroy();
            } catch (Exception e) {
                e.printStackTrace();
            }


            tishi="yes";//返回yes,表示存储成功，可以使用try,catch来捕捉错误，这里偷懒不用
        }
        return tishi;
    }
    @RequestMapping(value = "paint.do")
    @ResponseBody
    public   Long getImageBinary(){
        return re_image_name;
    }

}


