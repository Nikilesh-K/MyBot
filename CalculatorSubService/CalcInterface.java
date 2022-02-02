import java.sql.*;
import java.util.concurrent.TimeUnit;
import java.util.ArrayList;
public class CalcInterface{
    public boolean runStatus = true;

    public Connection connect(){
        //Connect to DB
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

    private String read(){
        String ticket = null;
        String command = "SELECT * FROM CALCULATOR";
        try(Connection conn = this.connect();
            Statement statement = conn.createStatement();
            ResultSet rs = statement.executeQuery(command)){
            while(rs.next()){
                ticket = rs.getString("TICKET");
            }
        }

        catch(SQLException e){
            System.out.println(e.getMessage());
        }
        return ticket;
    }

    public void update(String username, String response){
        String command = "UPDATE CALCULATOR SET RESPONSE = ? WHERE USERNAME = ?";
        try(Connection conn = this.connect();
            PreparedStatement PS = conn.prepareStatement(command)){
            PS.setString(1, response);
            PS.setString(2, username);
            PS.executeUpdate();
        } catch(SQLException e){
            System.out.println(e.getMessage());
        }
    }

    public String listen(){
        while(true){
            String ticket = this.read();
            if(ticket != null){
                return ticket;
            }
        }
    }

    public static void main(String[] args) throws InterruptedException{
        CalcInterface IF = new CalcInterface();
        TempCalc tempCalc = new TempCalc();
        ScientificCalc scientificCalc = new ScientificCalc();
        IF.connect();
        while(IF.runStatus){
            //Listen for ticket
            String ticket = IF.listen();
            
            //Check ticket content
            if(ticket.contains("TEMPCALC")){
                //Get mode, username, input temp
                String[] ticketElements = ticket.split(" ");
                String mode = ticketElements[1];
                String username = ticketElements[2];
                int inputTemp = Integer.parseInt(ticketElements[3]);

                //Check mode, do calculation, update central DB
                switch(mode){
                    case "C-F":
                        int fahren = tempCalc.CtoF(inputTemp);
                        IF.update(username, Integer.toString(fahren));
                    case "F-C":
                        int celsius = tempCalc.FtoC(inputTemp);
                        IF.update(username, Integer.toString(celsius));
                }
            }//end if statement

            if(ticket.contains("SCICALC")){
                //Get mode, input number list
                String[] ticketElements = ticket.split(" ");
                String mode = ticketElements[1];
                String username = ticketElements[2];
                String[] inputNumListStr = ticketElements[3].split(">");
                ArrayList<Integer> inputNumList = new ArrayList<>();

                //Convert string inputs to integer
                for(String numStr : inputNumListStr){
                    int num = Integer.parseInt(numStr);
                    inputNumList.add(num);
                }

                //Perform calculation
                int finalNum = scientificCalc.calculate(mode, inputNumList);
                
                //Send calculation to Central DB
                IF.update(username, Integer.toString(finalNum));
            }//end if statement

        } //end while loop
        
    }

}
