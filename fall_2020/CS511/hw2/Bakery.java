import java.util.ArrayList;
import java.util.Map;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Semaphore;

public class Bakery implements Runnable {
    private static final int TOTAL_CUSTOMERS = 200;
    private static final int ALLOWED_CUSTOMERS = 50;
    private static final int FULL_BREAD = 20;
    private Map<BreadType, Integer> availableBread;
    private List<Customer> customers = new ArrayList<Customer>();
    private ExecutorService executor;
    private float sales = 0;
    public Semaphore makeSale = new Semaphore(1);
    public Semaphore cashiers = new Semaphore(4);
    public Semaphore[] shelves;


    /**
     * Remove a loaf from the available breads and restock if necessary
     */
    public void takeBread(BreadType bread) {
        int breadLeft = availableBread.get(bread);
        if (breadLeft > 0) {
            availableBread.put(bread, breadLeft - 1);
        } else {
            System.out.println("No " + bread.toString() + " bread left! Restocking...");
            // restock by preventing access to the bread stand for some time
            try {
                Thread.sleep(1000);
            } catch (InterruptedException ie) {
                ie.printStackTrace();
            }
            availableBread.put(bread, FULL_BREAD - 1);
        }
    }

    /**
     * Add to the total sales
     */
    public void addSales(float value) {
        sales += value;
    }

    /**
     * Run all customers in a fixed thread pool
     */
    public void run() {
        availableBread = new ConcurrentHashMap<BreadType, Integer>();
        availableBread.put(BreadType.RYE, FULL_BREAD);
        availableBread.put(BreadType.SOURDOUGH, FULL_BREAD);
        availableBread.put(BreadType.WONDER, FULL_BREAD);

        executor = Executors.newFixedThreadPool(ALLOWED_CUSTOMERS);

        this.shelves = new Semaphore[3];
        for (int i = 0; i < 3; ++i) {
            this.shelves[i] = new Semaphore(1);
        }

        for (int i = 0; i < TOTAL_CUSTOMERS; i++) {
            customers.add(new Customer(this));
        }
        for (int i = 0; i < TOTAL_CUSTOMERS; i++) {
            executor.execute(customers.get(i));
        }
        executor.shutdown();
        while(!executor.isTerminated()){}
        System.out.println("Total sales for the day: " + this.sales + ".");

    }
}