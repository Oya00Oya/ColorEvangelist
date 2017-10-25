package com.heitian.ssm.controller;

import java.io.*;

/**
 * Created by GWY on 2017/7/17.
 */
public class test {
    public static void main(String args[]) {
        try {
            final Process p = Runtime.getRuntime().exec("python func/eval.py /home/orashi/IdeaProjects/web-ssm-shortsem/func/temp/2/1500410196029.png /home/orashi/IdeaProjects/web-ssm-shortsem/func/temp/1/1500410196029.png 65156198416");
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
