package chatbot;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

public class Terminator {
    private ArrayList<String> phraseList = new ArrayList<>(
            Arrays.asList("Ok, well that's all I got to talk about! Thanks for chatting!", "" +
                    "That was a nice chat! I've honestly run out of chat ideas, lol, so see ya later!"));

    public String terminate(){
        Random randObj = new Random();
        int index = randObj.nextInt(phraseList.size());
        return phraseList.get(index);
    }
}
