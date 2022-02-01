import java.util.ArrayList;
public class ScientificCalc{

    public int calculate(String mode, ArrayList<Integer> numList){
        if(numList.size() < 2){
            return 0;
        }
        switch(mode){
            case "+":
                int finalNum = numList.get(0) + numList.get(1);
                if(numList.size() == 2){
                    return finalNum;
                }
                else{
                    for(int i = 2; i < numList.size(); i++){
                        finalNum += numList.get(i); 
                    }
                }
            case "-":
                int finalNum = numList.get(0) - numList.get(1);
                if(numList.size() == 2){
                    return finalNum;
                }
                else{
                    for(int i = 2; i < numList.size(); i++){
                        finalNum -= numList.get(i); 
                    }
                }
            case "*":
                int finalNum = numList.get(0) * numList.get(1);
                if(numList.size() == 2){
                    return finalNum;
                }
                else{
                    for(int i = 2; i < numList.size(); i++){
                        finalNum *= numList.get(i); 
                    }
                }
            case "/":
                int finalNum = numList.get(0) / numList.get(1);
                if(numList.size() == 2){
                    return finalNum;
                }
                else{
                    for(int i = 2; i < numList.size(); i++){
                        finalNum /= numList.get(i); 
                    }
                }
        }//end switch
    }
}
