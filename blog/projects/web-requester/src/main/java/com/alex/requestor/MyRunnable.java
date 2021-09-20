// src/main/java/com/alex/requestor/MyRunnable.java
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
            // Create a URL object from the url string
            URL norris = new URL(this.url);
            // Open the HTTP connection to the URL
            URLConnection nc = norris.openConnection();
            // Read the response from the connection above
            BufferedReader in = new BufferedReader(
              new InputStreamReader(
                nc.getInputStream()
              )
            );
            // Get the raw JSON string response
            String inputLine = in.readLine();
            // Create the JSON representation so we can access 
            // it as if it is a map Object
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