byte sem = 0;
byte jets = 0;
byte pats = 0;

inline acquire() {
	atomic {
		sem > 0;
		sem--
	}
}

inline release() {
	atomic {
		sem++
	}
}

proctype Pat() {
	pats++;
	release()
}

proctype Jet() {
	acquire();
	acquire();
	jets++
}


init {
	byte i;
	for (i:0..10) {
		run Pat();
		run Jet();
	}
	assert(pats / jets > 2)
}