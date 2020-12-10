import java.util.concurrent.Semaphore;

Semaphore permToA = new Semaphore(0);
Semaphore permToES = new Semaphore(0);

Thread.start {
	permToA.acquire(); // P
	print("A");
	print("C");
	permToES.release();
}

Thread.start {
	print("R");
	permToA.release();
	permToES.acquire();
	print("E");
	print("S");
}

