import java.util.concurrent.Semaphore;
Semaphore cleanAvailable = new Semaphore(10);
Semaphore dirtyAvailabe = new Semaphore(90);


100.times {
	Thread.start { // Worker
		cleanAvailable.acquire();
		dirtyAvailabe.release();


	}
}


20.times {
	Thread.start { // Machine

		while (true) {
			dirtyAvailabe.acquire();
			cleanAvailable.release();


		}
	}
}