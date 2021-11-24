import java.sql.*;
import java.util.concurrent.TimeUnit;
public class Interface extends TempCalc {
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
        String command = "SELECT * FROM CALCULATOR";
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
        String command = "UPDATE CALCULATOR SET RESPONSE = ? WHERE ID = ?";
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
        Interface IF = new Interface();
        IF.connect();
        while(IF.runStatus){
            String ticket = IF.read();
            if(ticket.equals("TEST TICKET")){
                IF.update(1, "TEST ACK");
                Thread.sleep(5000);
            }

            if(ticket.startsWith("TEMPCALC F-C")){
                String param = ticket.substring(13, ticket.length() );
                int output = IF.FtoC(Integer.parseInt(param));
                IF.update(1, Integer.toString(output));
                Thread.sleep(5000);
            }

            if(ticket.startsWith("TEMPCALC C-F")){
                String param = ticket.substring(13, ticket.length() );
                int output = IF.CtoF(Integer.parseInt(param));
                IF.update(1, Integer.toString(output));
                Thread.sleep(5000);
            }

        }





    }
}
