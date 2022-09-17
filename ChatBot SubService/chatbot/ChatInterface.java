package chatbot;
import java.sql.*;
import java.util.concurrent.TimeUnit;
import java.util.ArrayList;

public class ChatInterface{
    public boolean runStatus = true;
    
    public Connection connect(){
        Connection conn = null;
        try{
            Class.forName("org.sqlite.JDBC");
            conn = DriverManager.getConnection("jdbc:sqlite:C:/All Stuff/Programming/MyBot/SQLite Central DB/Central DB.db");
        } catch(Exception e){
            System.err.println(e.getMessage());
            System.exit(0);
        }
        return conn;
    }

    public void update(String username, String response){
        String command = "UPDATE CHATBOT SET RESPONSE = ? WHERE USERNAME = ?";
        try(Connection conn = this.connect();
            PreparedStatement PS = conn.prepareStatement(command)){
            PS.setString(1, response);
            PS.setString(2, username);
            PS.executeUpdate();

        } catch(SQLException e){
            System.out.println(e.getMessage());
        }
    }

    public void reset(String username){
        String command = "UPDATE CHATBOT SET TICKET = ' ' WHERE USERNAME = ?";
        try(Connection conn = this.connect();
            PreparedStatement PS = conn.prepareStatement(command)){
            PS.setString(1, username);
            PS.executeUpdate();
        } catch(SQLException e){
            System.out.println(e.getMessage());
        }
    }

    public String listen(){
        String ticket;
        String command = "SELECT * FROM CHATBOT";
        while(true){
            try(Connection conn = this.connect();
                Statement statement = conn.createStatement();
                ResultSet rs = statement.executeQuery(command)){
                while(rs.next()){
                    ticket = rs.getString("TICKET");
                    if(ticket != null && !ticket.equals(" ")){
                        System.out.println(ticket);
                        return ticket;
                    }
                }
            }

            catch(SQLException e){
                System.out.println(e.getMessage());
            }
        }
    }

    // Initializes CHATCTX by adding new row to the table for current session's ctx data
    public void init_ctx(String username){
        String command = "INSERT INTO CHATCTX (USERNAME, TOPICS) VALUES (?, ?)";
        try(Connection conn = this.connect();
            PreparedStatement PS = conn.prepareStatement(command)){
            PS.setString(1, username);
            PS.setString(2, "NAME, MOOD, MOVIES");
            PS.executeUpdate();
        } catch(SQLException e){
            System.out.println(e.getMessage());
        }
    }

    //Updates CHAT_CTX fields (column)
    public void update_ctx(String username, String field, String value){
        String command = "UPDATE CHATCTX SET ? = ? WHERE USERNAME = ?";
        System.out.println(command);
        try(Connection conn = this.connect();
            PreparedStatement PS = conn.prepareStatement(command)){
            PS.setString(1, field);
            PS.setString(2, value);
            PS.setString(3, username);
            PS.executeUpdate();
        } catch(SQLException e){
            System.out.println("UPDATE: " + e.getMessage());
        }
    }

    //Gets any field from CHATCTX
    public String get_ctx(String username, String field){
        String command = "SELECT " + field + " FROM CHATCTX WHERE USERNAME = " + "\"" + username + "\";";
        System.out.println(command);
        try(Connection conn = this.connect();
            Statement statement = conn.createStatement();
            ResultSet rs = statement.executeQuery(command)){
            rs.next();
            return rs.getString(field);
        }
        catch(SQLException e){
            System.out.println("GET: " + e.getMessage());
            return null;
        }
    }

    public static void main(String[] args) throws InterruptedException {
        ChatInterface IF = new ChatInterface();
        CStarter cstarter = new CStarter();
        Progressor progressor = new Progressor();
        Terminator terminator = new Terminator();

        while(IF.runStatus){
            String ticket = IF.listen();
            if(ticket.contains("CSTART ")){
                String[] ticketElements = ticket.split("-");
                String username = ticketElements[1];
                
                String starterPhrase = cstarter.choosePhrase();
                IF.update(username, starterPhrase);
                IF.reset(username);
            }

            if(ticket.contains("PROGSTART ")){
                String[] ticketElements = ticket.split("-");
                String username = ticketElements[1];

                //Initialize CHATCTX
                IF.init_ctx(username);

                //Pass output handling to Progressor
                progressor.progress(IF, username, terminator);

                IF.reset(username);
            }

            if(ticket.contains("PROGRESS ")){
                String[] ticketElements = ticket.split("-");
                String username = ticketElements[1];

                progressor.reply(IF, ticketElements[2], username);

                Thread.sleep(5000);

                //Pass output handling to Progressor
                progressor.progress(IF, username, terminator);

                IF.reset(username);
            }
        }
    }

}