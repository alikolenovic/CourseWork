byte np = 0;
byte nq = 0;
byte critical = 0;

proctype P() {
	do 
		:: true ->
			np = 1;
			np = nq + 1;
			nq == 0 || np <= nq;
			critical++;
            critical--;
			np = 0;
	od;
}

proctype Q() {
	do 
		:: true ->
			nq = 1;
			nq = np + 1;
			np == 0 || nq < np;
			critical++;
			assert(critical <= 1);
            critical--;
			nq = 0;
	od;
}

init {
	run P();
	run Q();
}