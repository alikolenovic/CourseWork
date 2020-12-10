Semaphore permToLoad = new Semaphore(0);
Semaphore doneLoading = new Semaphore(0);
Semaphore northSouth = new Semaphore(1);
Semaphore southNorth = new Semaphore(1);
tracks = [new Semaphore(1), new Semaphore(1)];


// Direction
// 0 = going North, 1 = going South

Thread.start { // PassengerTrain
	Random rnd = new Random();
	int dir = rnd.nextInt(1);
	
	tracks[dir].acquire();
	// load/unload passengers
	tracks[dir].release();
}

Thread.start { // FreightTrain

	Random rnd = new Random();
	int dir = rnd.nextInt(1);
	tracks[0].acquire();
	tracks[1].acquire();
	permToLoad.release();
	// Wait for loading to complete
	doneLoading.acquire();
	tracks[0].release();
	tracks[1].release();

}

Thread.start {
	while (true) {
		permToLoad.acquire();

		doneLoading.release();
	}
}