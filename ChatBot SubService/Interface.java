import java.sql.*;
import java.util.concurrent.TimeUnit;

public class Interface {
    public boolean runStatus = true;
    public Connection connect(){
        //Connect to DB
        Connection conn = null;
        try{
            Class.forName("org.sqlite.JDBC");
            conn = DriverManager.getConnection("jdbc:sqlite:C:/All Stuff/Programming/RPGdata.db");
        } catch(Exception e){
            System.err.println(e.getMessage());
            System.exit(0);
        }
        return conn;
    }

    public String read(){
        String ticket = null;
        String command = "SELECT * FROM CHATBOT";
        try(Connection conn = this.connect();
            Statement statement = conn.createStatement();
            ResultSet rs = statement.executeQuery(command)){
            while(rs.next()){
                ticket = rs.getString("TICKET");
                /*
                System.out.println(rs.getInt("ID") + "\t"
                        + rs.getString("TICKET") + "\t"
                        + rs.getString("RESPONSE") + "\t");

                 */


            }


        }
        catch(SQLException e){
            System.out.println(e.getMessage());
        }
        return ticket;
    }

    public void update(int id, String response){
        String command = "UPDATE CHATBOT SET RESPONSE = ? WHERE ID = ?";
        try(Connection conn = this.connect();
            PreparedStatement PS = conn.prepareStatement(command)){
            PS.setString(1, response);
            PS.setInt(2, id);

            PS.executeUpdate();

        } catch(SQLException e){
            System.out.println(e.getMessage());
        }
    }

    public static void main(String[] args) throws InterruptedException{
        //Initialize Objects
        Interface IF = new Interface();
        CStarter cstarter = new CStarter();
        Progressor progressor = new Progressor();
        Terminator terminator = new Terminator();
        //TESTING ZONE
        //System.out.println(cstarter.choosePhrase());
        IF.connect();
        while(IF.runStatus){
            String ticket = IF.read();
            if(ticket.equals("TEST TICKET")){
                IF.update(1, "TEST ACK");
                Thread.sleep(5000);
            }

            //UNSTABLE - DO NOT RUN
            if(ticket.equals("NEW SESSION")){
                IF.update(1, cstarter.choosePhrase());
                //MAIN LOOP FOR SESSION
                while(true){
                    ticket = IF.read();
                    if(ticket.startsWith("NEW MSSG")){
                        IF.update(1, cstarter.choosePhrase());
                        break;
                    }
                }
                Thread.sleep(8000);

            }
        }
    }


}
