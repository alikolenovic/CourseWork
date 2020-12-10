byte np = 0;
byte nq = 0;

proctype P() {
	do 
		:: true ->
			np = nq + 1;
			nq == 0 || np <= nq;
			np = 0;
	od;
}

proctype Q() {
	do 
		:: true ->
			nq = np + 1;
			np == 0 || nq < np;
			nq = 0;
	od;
}

init {
	run P();
	run Q()
}