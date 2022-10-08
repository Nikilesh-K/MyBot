package chatbot;

import java.util.*;

public class Progressor {
    private enum Topic{
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

        System.out.println("progress: " + topics);
        System.out.println("progress: " + topics.size());

        /*
        Start termination
        NOTE: When the last element is removed from the topics list in Central DB, it leaves behind an empty string
        which counts as an element in the list. We remove this empty string (if it exists) before checking if
        termination is necessary.
         */
        topics.remove("");
        if(topics.size() == 0){
            String termination = terminator.terminate();
            IF.reset_ctx(username);
            IF.update(username, "TERMINATE " + termination);
            return;
        }

        //Choose topic
        Random randObj = new Random();
        int topicIndex = randObj.nextInt(topics.size());
        System.out.println("progress: " + topicIndex);
        System.out.println("progress: " + topics.get(topicIndex));
        Topic chosenTopic = topicNameMapping.get(topics.get(topicIndex));
        System.out.println("progress: " + chosenTopic);
        ArrayList<String> topicQuestions = this.topicQuestionMapping.get(chosenTopic);

        //Choose question for topic
        int questionIndex = randObj.nextInt(topicQuestions.size());
        String chosenQuestion = topicQuestions.get(questionIndex);

        //Update interface
        IF.update(username, chosenQuestion);

        //Set current topic in Central DB
        IF.update_ctx(username, "CURRENT_TOPIC", topics.get(topicIndex));
    }

    public void reply(ChatInterface IF, String userResponse, String username){
        Topic currentTopic = topicNameMapping.get(IF.get_ctx(username, "CURRENT_TOPIC"));
        String response = process(currentTopic, userResponse, username);
        IF.update(username, response);

        //Long-winded way of updating topic list in Central DB
        ArrayList<String> topics = new ArrayList<String>( //Get current list of topics as ArrayList
                Arrays.asList(IF.get_ctx(username, "TOPICS").split("[,]", 0))
        );

        topics.remove(IF.get_ctx(username, "CURRENT_TOPIC")); //Update ArrayList
        StringBuilder newTopicList = new StringBuilder(); //Convert updated ArrayList to string
        for(int i = 0; i < topics.size(); i++){
            newTopicList.append(topics.get(i));
            if(i < topics.size() - 1){
                newTopicList.append(",");
            }
        }

        IF.update_ctx(username, "TOPICS", newTopicList.toString());
    }

}
