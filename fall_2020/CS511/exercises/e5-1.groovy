
Semaphore permForJet = new Semaphore(0);
Semaphore mutex = new Semaphore(1);

1000.times {
	Thread.start { // Jets
		mutex.acquire();
		permForJet.acquire();
		permForJet.acquire();
		goInside();
		mutex.release();

	}
}

1000.times {
	Thread.start { // Patriots
		goInside();
		permForJet.release();


	}
}