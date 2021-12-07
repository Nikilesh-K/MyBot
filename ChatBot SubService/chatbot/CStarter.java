package chatbot;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.Random;
import java.util.Map;
import chatbot.Progressor.Topic;
public class CStarter {
    ArrayList<String> phraseList = new ArrayList<>(
            Arrays.asList("Hello! What's your name?", "Hi, how are you?")
    );

    Map<String, Topic> topicMapping = Map.of(
            phraseList.get(0), Topic.NAME,
            phraseList.get(1), Topic.MOOD
    );

    public String choosePhrase(){
        Random randObj = new Random();
        int index = randObj.nextInt(phraseList.size());
        return phraseList.get(index);
    }

    public Topic getTopic(String phrase){
        return topicMapping.get(phrase);
    }


}
