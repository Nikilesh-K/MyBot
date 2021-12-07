package chatbot;

import java.util.*;

public class Progressor {
    private String name;
    private ArrayList<String> movies = new ArrayList<>();
    private String mood;
    public enum Topic{
        NAME,
        MOVIES,
        MOOD
    }

    private ArrayList<String> nameQuestions = new ArrayList<>(
        Arrays.asList("So what's your name?", "What should I call you?")
    );
    private ArrayList<String> moodQuestions = new ArrayList<>(
            Arrays.asList("How do you do?", "How are you doing?")
    );
    private ArrayList<String> movieQuestions = new ArrayList<>(
            Arrays.asList("What movies do you watch?", "What are some of your favorite movies?")
    );
    private Map<Topic, ArrayList<String>> topicQuestionMapping = Map.of(
            Topic.NAME, nameQuestions,
            Topic.MOOD, moodQuestions,
            Topic.MOVIES, movieQuestions
    );
    public ArrayList<Topic> usedTopics = new ArrayList<>();
    private void nameHandler(String phrase){
        String[] phraseArray = phrase.split("\\s");
        String[] operatives = {"my", "name", "is", "the", "'s"};
        if (phraseArray.length == 1){
            System.out.println("That's a great name, " + phraseArray[0] + "!");
        }
        else{
            for(int i = 0; i < phraseArray.length; i++){
                boolean isOperative = Arrays.asList(operatives).contains(phraseArray[i]);
                if(!isOperative){
                    this.name = phraseArray[i];
                    break;
                }
            }

            System.out.println("That's a great name, " + this.name + "!");
        }
    }

    private void moodHandler(String phrase){
        String processedPhrase = phrase.toLowerCase();
        String[] posKeys = {"good", "fine", "well", "ok", "okay"};
        String[] negKeys = {"bad", "terrible", "horrible", "not"};
        boolean isPosKey = false;
        for (String posKey : posKeys) {
            if (processedPhrase.contains(posKey)) {
                this.mood = posKey;
                isPosKey = true;
                break;
            }
        }
        if(isPosKey){
            System.out.println("Great!");
        }
        else {
            for (String negKey : negKeys) {
                if (processedPhrase.contains(negKey)) {
                    this.mood = negKey;
                    System.out.println("Oh no, hope you'll do better soon!");
                    break;
                }
            }
        }

    }

    private void moviesHandler(){

    }

    public void process(Topic topic, String phrase){
        switch(topic){
            case NAME:
                nameHandler(phrase);
                break;
            case MOOD:
                moodHandler(phrase);
                break;
            case MOVIES:
                moviesHandler();
                break;
        }
    }

    //WIP
    public void askSession(Scanner inputObj){
        while(true){
            ArrayList<Topic> topicConstants= new ArrayList<>(
                    Arrays.asList(Topic.NAME, Topic.MOOD, Topic.MOVIES)
            );
            for(Topic topic : this.usedTopics){
                topicConstants.remove(topic);
            }

            if(topicConstants.size() == 0){
                break;
            }
            Random randObj = new Random();
            int topicIndex = randObj.nextInt(topicConstants.size());
            Topic chosenTopic = topicConstants.get(topicIndex);
            ArrayList<String> topicQuestions = this.topicQuestionMapping.get(chosenTopic);

            int questionIndex = randObj.nextInt(topicQuestions.size());
            String chosenQuestion = topicQuestions.get(questionIndex);
            System.out.println(chosenQuestion);
            String userResponse = inputObj.nextLine();
            process(chosenTopic, userResponse);

            this.usedTopics.add(chosenTopic);

        }
    }
}
