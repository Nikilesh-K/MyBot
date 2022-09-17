package chatbot;

import java.util.*;

public class Progressor {
    public enum Topic{
        NAME,
        MOVIES,
        MOOD
    }

    private ChatInterface IF;
    private final ArrayList<String> nameQuestions = new ArrayList<>(
        Arrays.asList("So what's your name?", "What should I call you?")
    );
    private final ArrayList<String> moodQuestions = new ArrayList<>(
            Arrays.asList("How do you do?", "How are you doing?")
    );
    private final ArrayList<String> movieQuestions = new ArrayList<>(
            Arrays.asList("What movies do you watch?", "What are some of your favorite movies?")
    );
    private final Map<Topic, ArrayList<String>> topicQuestionMapping = Map.of(
            Topic.NAME, nameQuestions,
            Topic.MOOD, moodQuestions,
            Topic.MOVIES, movieQuestions
    );

    private final Map<String, Topic> topicNameMapping = Map.of(
            "NAME", Topic.NAME,
            "MOOD", Topic.MOOD,
            "MOVIES", Topic.MOVIES
    );

    private Topic currentTopic;

    //TODO FOR HANDLERS: Add response variation
    private String nameHandler(String phrase, String username){
        String processedPhrase = phrase.toLowerCase();
        String[] phraseArray = phrase.split("\\s");
        String[] operatives = {"my", "name", "is", "the", "'s"};
        String name = "";

        //If only the name is in the response
        if (phraseArray.length == 1){
            //Capitalizing first letter of name for better precision
            name = phraseArray[0].substring(0, 1).toUpperCase() + phraseArray[0].substring(1);
            IF.update_ctx(username, "NAME", name);

        }
        else{
            //Loop through response, look for a name.
            for(int i = 0; i < phraseArray.length; i++){
                boolean isOperative = Arrays.asList(operatives).contains(phraseArray[i]);
                if(!isOperative){
                    name = phraseArray[i];
                    IF.update_ctx(username, "NAME", name);
                    break;
                }
            }
        }
        return "That's a great name, " + name + "!";
    }

    private String moodHandler(String phrase, String username){
        String processedPhrase = phrase.toLowerCase();
        String[] posKeys = {"good", "fine", "well", "ok", "okay"};
        String[] negKeys = {"bad", "terrible", "horrible", "not"};
        String mood;

        for (String posKey : posKeys) {
            if (processedPhrase.contains(posKey)) {
                mood = posKey;
                IF.update_ctx(username, "MOOD", mood);
                return "Great!";
            }
        }
        
        for (String negKey : negKeys) {
            if (processedPhrase.contains(negKey)) {
                mood = negKey;
                IF.update_ctx(username, "MOOD", mood);
                return "Oh no, hope you'll do better soon!";
            }
        }
        return "Oh, ok.";
    }

    private String moviesHandler(String phrase, String username){
        String[] operatives = {"I", "liked", "loved", "watched", "watching", "love", "life", "my", "favorite", "movie", "is", "like", "watch"};
        String[] phraseArray = phrase.split("\\s");
        ArrayList<String> movies = new ArrayList<>();
        for(int i = 0; i < phraseArray.length; i++){
            boolean isOperative = false;
            for(int j = 0; j < operatives.length; j++){
                if(phraseArray[i].toLowerCase().equals(operatives[j].toLowerCase())){
                    isOperative = true;
                    break;
                }
            }
            if(!isOperative){
                movies.add(phraseArray[i].substring(0, 1) + phraseArray[i].substring(1));
                IF.update_ctx(username, "MOVIES", phraseArray[i].substring(0, 1) + phraseArray[i].substring(1));
                break;
            }
        }

        return movies.get(0) + " sounds like a great movie!";
    }

    public String process(Topic topic, String phrase, String username){
        String response = " ";
        switch(topic){
            case NAME:
                response = nameHandler(phrase, username);
                break;
            case MOOD:
                response = moodHandler(phrase, username);
                break;
            case MOVIES:
                response = moviesHandler(phrase, username);
                break;
        }
        return response;
    }

    public void progress(ChatInterface IF, String username, Terminator terminator){
        //Initialize ChatInterface if not already initialized
        if(this.IF == null){
            this.IF = IF;
        }
        ArrayList<String> topics = new ArrayList<String>(
                Arrays.asList(IF.get_ctx(username, "TOPICS").split("[,]", 0))
        );

        //Start termination
        if(topics.size() == 0){
            String termination = terminator.terminate();
            IF.update(username, "TERMINATE " + termination);
            return;
        }

        //Choose topic
        Random randObj = new Random();
        int topicIndex = randObj.nextInt(topics.size());
        Topic chosenTopic = topicNameMapping.get(topics.get(topicIndex));
        ArrayList<String> topicQuestions = this.topicQuestionMapping.get(chosenTopic);

        //Choose question for topic
        int questionIndex = randObj.nextInt(topicQuestions.size());
        String chosenQuestion = topicQuestions.get(questionIndex);

        //Update interface
        IF.update(username, chosenQuestion);

        //Set current topic so Progressor can remember
        currentTopic = chosenTopic;
    }

    public void reply(ChatInterface IF, String userResponse, String username){
        String response = process(currentTopic, userResponse, username);
        IF.update(username, response);

        //Long-winded way of updating topic list in Central DB
        ArrayList<String> topics = new ArrayList<String>( //Get current list of topics
                Arrays.asList(IF.get_ctx(username, "TOPICS").split("[,]", 0))
        );

        for(String key : topicNameMapping.keySet()){ //Find corresponding topic name for currentTopic
            if(topicNameMapping.get(key) == currentTopic){
                topics.remove(key); //Update ArrayList, convert ArrayList into string, update CHATCTX
                String topicList = "";
                for(String topic : topics){
                    topicList += topic;
                }
                IF.update_ctx(username, "TOPICS", topicList);
            }
        }
    }

}
