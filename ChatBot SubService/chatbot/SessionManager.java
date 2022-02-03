package chatbot;
public class SessionManager{
    private CStarter cstarter;
    private Progressor progressor;
    private ChatInterface IF;

    //Makes DB write/read functions accessible to this class
    public SessionManager(ChatInterface IF){
        this.IF = IF;
    }

    public void runSession(String username){
        cstarter = new CStarter();
        progressor = new Progressor();

        String starterPhrase = cstarter.choosePhrase();
        IF.update(username, starterPhrase);
        


    }


}