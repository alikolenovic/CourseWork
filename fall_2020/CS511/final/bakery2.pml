byte np = 0;
byte nq = 0;
byte critical = 0;
byte temp;

proctype P() {
    do 
        :: true ->
            temp = nq + 1;
            np = temp;
            nq == 0 || np <= nq;
            critical++;
            critical--;
            np = 0;
    od;
}

proctype Q() {
    do 
        :: true ->
            temp = np + 1;
            nq = temp;
            np == 0 || nq < np;
            critical++;
            assert(critical <= 1);
            critical--;
            nq = 0;
    od;
}