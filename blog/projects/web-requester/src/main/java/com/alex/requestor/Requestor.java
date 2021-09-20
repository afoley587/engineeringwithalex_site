// The Requestor (Main) class
// src/main/java/com/alex/requestor/Requestor.java
package requestor;
 
import requestor.MyRunnable;
 
public class Requestor {
   public static void main(String[] args) throws Exception {
       String url = "https://api.chucknorris.io/jokes/random";
       for (int i = 0; i < 5; i++) {
	    // Creates 5 different runnables to request jokes from
 	    // the above API
           MyRunnable runnable = new MyRunnable(url);
           new Thread(runnable).start();
       }
   }
}
