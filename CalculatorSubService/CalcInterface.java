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
                //Get mode, input temp
                String mode = ticket.substring(9, 12);
                int inputTemp = Integer.parseInt(ticket.substring(13));

                //Check mode, do calculation, update central DB
                switch(mode){
                    case "C-F":
                        int fahren = tempCalc.CtoF(inputTemp);
                        IF.update(1, Integer.toString(fahren));
                    case "F-C":
                        int celsius = tempCalc.FtoC(inputTemp);
                        IF.update(1, Integer.toString(celsius));
                }
            }//end if statement

            if(ticket.contains("SCICALC")){
                //Get mode, input number list
                String mode = ticket.substring(8, 9);
                String inputStr = ticket.substring(10);
                String[] inputNumListStr = inputStr.split(", ");
                ArrayList<Integer> inputNumList = new ArrayList<>();

                //Convert string inputs to integer
                for(String numStr : inputNumListStr){
                    int num = Integer.parseInt(numStr);
                    inputNumList.add(num);
                }

                //Perform calculation
                int finalNum = scientificCalc.calculate(mode, inputNumList);
                
                //Send calculation to Central DB
                IF.update(1, Integer.toString(finalNum));
            }//end if statement

        } //end while loop
        
    }

}
