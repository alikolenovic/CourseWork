
Semaphore permToStartWorking0 = new Semaphore(0);
Semaphore permToMoveToStation1 = new Semaphore(0);
Semaphore permToStartWorking1 = new Semaphore(0);
Semaphore permToMoveToStation2 = new Semaphore(0);
Semaphore permToStartWorking2 = new Semaphore(0);
Semaphore permToLeave = new Semaphore(1);
Semaphore station0 = new Semaphore(1);
Semaphore station1 = new Semaphore(1);
Semaphore station2 = new Semaphore(1);

100.times {
	int car_id = it;
	Thread.start {
		println("Car " + car_id + " is waiting to get washed");
		station0.acquire();
		permToStartWorking0.release();
		
		println("Car " + car_id + " is waiting to get blasted");
		permToMoveToStation1.acquire();
		
		station1.acquire();
		station0.release();		
		
		permToStartWorking1.release();
		
		println("Car " + car_id + " is waiting to get rinsed");
		permToMoveToStation2.acquire();
		
		station2.acquire();
		station1.release();		
		
		permToStartWorking2.release();
		
		
		println("Car " + car_id + " is waiting to get dried");

		permToLeave.acquire();
		station2.release();


		println("Car " + car_id + " is waiting to get washed");


	}
}

Thread.start { // machine 0
	permToStartWorking0.acquire();
	permToMoveToStation1.release();

}


Thread.start { // machine 1
	permToStartWorking1.acquire();
	permToMoveToStation2.release();

}


Thread.start { // machine 2
	permToStartWorking2.acquire();
	permToLeave.release();

}