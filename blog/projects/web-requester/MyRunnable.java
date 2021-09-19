import java.net.*;
import java.io.*;

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
            String inputLine;
            while ((inputLine = in.readLine()) != null) {
              System.out.println(inputLine);
            }
            in.close();
        }
        catch (Exception e) {
            // Throwing an exception
            System.out.println("Exception is caught");
        }
    }
}