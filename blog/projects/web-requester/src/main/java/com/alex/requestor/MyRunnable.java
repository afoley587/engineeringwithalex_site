package requestor;

import java.net.*;
import java.io.*;
import org.json.JSONObject;

public class MyRunnable implements Runnable {
    
    private String url;

    public MyRunnable(String url) {
        this.url = url;
   }

    public void run()
    {
        try {
            // Displaying the thread that is running
            URL norris = new URL(this.url);
            URLConnection nc = norris.openConnection();
            BufferedReader in = new BufferedReader(
              new InputStreamReader(
                nc.getInputStream()
              )
            );
            String inputLine = in.readLine();
            JSONObject obj  = new JSONObject(inputLine);
            in.close();
            System.out.println(obj.getString("value"));
        }
        catch (Exception e) {
            // Throwing an exception
            System.out.println("Exception is caught");
        }
    }
}