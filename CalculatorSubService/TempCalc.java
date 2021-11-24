public class TempCalc{

    protected int FtoC(int fahren){
        int interCalc1 = fahren - 32;
        int interCalc2 = interCalc1 * 5;
        int celsius = interCalc2 / 9;
        return celsius;
    }

    protected int CtoF(int celsius){
        int interCalc1 = celsius * 9;
        int interCalc2 = interCalc1 / 5;
        int fahren = interCalc2 + 32;

        return fahren;
    }
}
