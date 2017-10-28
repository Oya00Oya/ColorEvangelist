package com.heitian.ssm.controller;

import java.io.*;

/**
 * Created by GWY on 2017/7/17.
 */
public class test {
    public static void main(String args[]) {
        try {
            final Process p = Runtime.getRuntime().exec("python ../webapps/ROOT/func/colorization.py ../webapps/ROOT/func/input/colorization/pic/1500410196029.png ../webapps/ROOT/func/input/colorization/line/1500410196029.png ../webapps/ROOT/func/output/colorization/65156198416_out.png");
            new Thread(new Runnable() {

                //@Override
                public void run() {
                    BufferedReader br = new BufferedReader(
                            new InputStreamReader(p.getInputStream()));
                    try {
                        String line1=null;
                        while ((line1=br.readLine() )!= null)
                           System.out.println(line1);
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
    }
}
