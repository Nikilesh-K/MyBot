//Temporary class for testing ChatBot features
package chatbot;
import chatbot.Progressor.Topic;
import java.util.Scanner;
import java.util.ArrayList;
public class Output {
    Scanner inputObj = new Scanner(System.in);

    public static void main(String[] args){
        CStarter cstarter = new CStarter();
        Progressor progressor = new Progressor();
        Terminator terminator = new Terminator();
        Output output = new Output();
        
        //Start of conversation
        String starterPhrase = cstarter.choosePhrase();
        output.write(starterPhrase);

        //Progress conversation - pass output handling to Progressor
        progressor.progress(output);

        //Terminate conversation
    }

    public void write(String output){
        System.out.println(output);
    }

    public String read(){
        String userResponse = inputObj.nextLine();
        return userResponse;
    }
}
