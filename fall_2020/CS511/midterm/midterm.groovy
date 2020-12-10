
Semaphore gasUp = new Semaphore(6, true);
Semaphore refuel = new Semaphore(2);

Thread.start { // Vehicle
	gasUp.acquire();
	// gas up
	gasUp.release();
}

Thread.start { // Truck

	gasUp.acquire(6);
	refuel.acquire();
	refuel.release();
	gasUp.release(6);

}


monitor Grid {
	int producers = 0;
	int consumers = 0;
	condition OKtoConsume, OKtoProduce;


	void startConsuming() {
		curr = consumers + 1;
		while (curr < producers) {
			OKtoConsume.wait();
		}
		consumers = consumers + 1;
	}

	void stopConsuming() {
		consumers = consumers - 1;
		OKtoProduce.signal();
		
	}

	void startProducing() {
		producers = producers + 1;
		if (producers >= consumers) {
			OKtoConsume.signal();
		}
	}

	void stopProducing() {
		while (producers <= consumers) {
			OKtoProduce.wait();
		}
		producers = producers - 1;
	}


}



