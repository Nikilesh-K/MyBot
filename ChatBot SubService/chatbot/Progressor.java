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

    //TODO FOR HANDLERS: Add response variation
    private void nameHandler(String phrase){
        String processedPhrase = phrase.toLowerCase();
        String[] phraseArray = phrase.split("\\s");
        String[] operatives = {"my", "name", "is", "the", "'s"};

        //If only the name is in the response
        if (phraseArray.length == 1){
            //Capitalizing first letter of name for better precision
            this.name = phraseArray[0].substring(0, 1).toUpperCase() + phraseArray[0].substring(1);
        }
        else{
            //Loop through response, look for a name.
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
        for (String posKey : posKeys) {
            if (processedPhrase.contains(posKey)) {
                this.mood = posKey;
                System.out.println("Great!");
                return;
            }
        }
        
        for (String negKey : negKeys) {
            if (processedPhrase.contains(negKey)) {
                this.mood = negKey;
                System.out.println("Oh no, hope you'll do better soon!");
                return;
            }
        }

    }

    private void moviesHandler(String phrase){
        String[] operatives = {"I", "liked", "loved", "watched", "watching", "love", "life", "my", "favorite", "movie", "is"};
        String[] phraseArray = phrase.split("\\s");
        for(int i = 0; i < phraseArray.length; i++){
            boolean isOperative = Arrays.asList(operatives).contains(phraseArray[i]);
            if(!isOperative){
                this.movies.add(phraseArray[i].substring(0, 1) + phraseArray[i].substring(1));
                break;
            }
        }

        System.out.println(this.movies.get(0) + " sounds like a great movie!");
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
                moviesHandler(phrase);
                break;
        }
    }

    //WIP
    public void startSession(Scanner inputObj){
        ArrayList<Topic> topicConstants = new ArrayList<>(
            Arrays.asList(Topic.NAME, Topic.MOOD, Topic.MOVIES)
        );

        while(topicConstants.size() > 0){
            //Choose topic
            Random randObj = new Random();
            int topicIndex = randObj.nextInt(topicConstants.size());
            Topic chosenTopic = topicConstants.get(topicIndex);
            ArrayList<String> topicQuestions = this.topicQuestionMapping.get(chosenTopic);

            //Choose question for topic
            int questionIndex = randObj.nextInt(topicQuestions.size());
            String chosenQuestion = topicQuestions.get(questionIndex);
            System.out.println(chosenQuestion);
            String userResponse = inputObj.nextLine();

            //Call handler for specified topic
            process(chosenTopic, userResponse);

            topicConstants.remove(chosenTopic);
        }
    }
}
