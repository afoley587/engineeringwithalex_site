import java.net.*;
import java.io.*;

public class Main {
    public static void main(String[] args) throws Exception {
        String url = "https://api.chucknorris.io/jokes/random";
        for (int i = 0; i < 5; i++) {
            MyRunnable runnable = new MyRunnable(url);
            new Thread(runnable).start();
        }
        // URL norris = new URL("https://api.chucknorris.io/jokes/random");
        // URLConnection nc = norris.openConnection();
        // BufferedReader in = new BufferedReader(
        //                         new InputStreamReader(
        //                         nc.getInputStream()));
        // String inputLine;

        // while ((inputLine = in.readLine()) != null) 
        //     System.out.println(inputLine);
        // in.close();
    }

    // private JSONObject responseToJson() {}

}