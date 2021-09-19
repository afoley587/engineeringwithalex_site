package requestor;

import java.net.*;
import java.io.*;
import requestor.MyRunnable;

public class Requestor {
    public static void main(String[] args) throws Exception {
        String url = "https://api.chucknorris.io/jokes/random";
        for (int i = 0; i < 5; i++) {
            MyRunnable runnable = new MyRunnable(url);
            new Thread(runnable).start();
        }
    }
}