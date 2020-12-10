Semaphore okToHairWash = new Semaphore(0);
Semaphore moveToStyle = new Semaphore(0);
Semaphore okToStyle = new Semaphore(0);
Semaphore clientDone = new Semaphore(0);


Thread.start { // Client
	okToHairWash.release();
	moveToStyle.acquire();
	okToStyle.release();
	clientDone.acquire();


}


Thread.start { // Hair wash specialist
	while (true) {
		okToHairWash.acquire();
		// Wash Hair
		moveToStyle.release();


	}
	
}


Thread.start { // Hair Stylist
	while (true) {
		okToStyle.acquire();
		// Style
		clientDone.release();

	}
	
}


monitor HairSalon {
	int availableStylists = 0;
	int clientsWaiting = 0;
	Condition hairStylistAvailable;
	Condition clientsAvailable;
	Condition hairStylingDone;

	void getHairCut() { // called by client
		clientsWaiting++;
		clientsAvailable.signal();
		while (availableStylists == 0) {
			hairStylistAvailable.wait();

		}
		clientsWaiting--;
		hairStylingDone.wait()

	}

	void startHairStyling() { // called by hair stylist
		availableStylists++;
		hairStylistAvailable.signal();
		while (clientsWaiting == 0) {
			clientsAvailable.wait();

		}
		availableStylists--;

	}

	void doneHairStyling() { // called by hair stylist
		hairStylingDone.signal();


	}


}