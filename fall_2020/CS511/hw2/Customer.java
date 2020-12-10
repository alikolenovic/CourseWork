import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public class Customer implements Runnable {
    private Bakery bakery;
    private Random rnd;
    private List<BreadType> shoppingCart;
    private int shopTime;
    private int checkoutTime;

    /**
     * Initialize a customer object and randomize its shopping cart
     */
    public Customer(Bakery bakery) {
        this.bakery = bakery;
        rnd = new Random();
        shoppingCart = new ArrayList<BreadType>();
        fillShoppingCart();
        shopTime = 1 + rnd.nextInt(1000);
        checkoutTime = 1 + rnd.nextInt(1000);

    }

    /**
     * Run tasks for the customer
     */
    public void run() {
        try {
            System.out.println("Customer " + hashCode() + " has started shopping.");

            for (BreadType Bread : shoppingCart) {
                bakery.shelves[Bread.ordinal()].acquire();
                Thread.sleep(shopTime);
                bakery.takeBread(Bread);
                bakery.shelves[Bread.ordinal()].release();
                System.out.println("Customer " + hashCode() + " has taken " + Bread.name() + ".");
            }
            bakery.cashiers.acquire();
            Thread.sleep(checkoutTime);
            System.out.println("Customer " + hashCode() + " is paying.");
            bakery.makeSale.acquire();
            bakery.addSales(getItemsValue());
            bakery.makeSale.release();
            bakery.cashiers.release();
            System.out.println("Customer " + hashCode() + " has finished.");
            


        } catch (InterruptedException e) {
            e.printStackTrace();
        }

    }

    /**
     * Return a string representation of the customer
     */
    public String toString() {
        return "Customer " + hashCode() + ": shoppingCart=" + Arrays.toString(shoppingCart.toArray()) + ", shopTime=" + shopTime + ", checkoutTime=" + checkoutTime;
    }

    /**
     * Add a bread item to the customer's shopping cart
     */
    private boolean addItem(BreadType bread) {
        // do not allow more than 3 items, chooseItems() does not call more than 3 times
        if (shoppingCart.size() >= 3) {
            return false;
        }
        shoppingCart.add(bread);
        return true;
    }

    /**
     * Fill the customer's shopping cart with 1 to 3 random breads
     */
    private void fillShoppingCart() {
        int itemCnt = 1 + rnd.nextInt(3);
        while (itemCnt > 0) {
            addItem(BreadType.values()[rnd.nextInt(BreadType.values().length)]);
            itemCnt--;
        }
    }

    /**
     * Calculate the total value of the items in the customer's shopping cart
     */
    private float getItemsValue() {
        float value = 0;
        for (BreadType bread : shoppingCart) {
            value += bread.getPrice();
        }
        return value;
    }
}