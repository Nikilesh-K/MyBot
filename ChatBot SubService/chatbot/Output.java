//Temporary class for testing ChatBot features
package chatbot;
import chatbot.Progressor.Topic;
import java.util.Scanner;
public class Output {
    public void print(String output){
        System.out.println(output);
    }
    public static void main(String[] args){
        CStarter cstarter = new CStarter();
        Progressor progressor = new Progressor();
        System.out.println("Type here: ");
        Scanner inputObj = new Scanner(System.in);
        inputObj.nextLine();

        String starterPhrase = cstarter.choosePhrase();
        System.out.println(starterPhrase);
        Topic starterTopic = cstarter.getTopic(starterPhrase);

        String userPhrase = inputObj.nextLine();
        progressor.process(starterTopic, userPhrase);
        progressor.usedTopics.add(starterTopic);

        inputObj.nextLine();
        progressor.askSession(inputObj);



    }
}
