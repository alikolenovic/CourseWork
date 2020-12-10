import java.io.*;
import java.lang.reflect.Array;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class TextSwap {

    private static String readFile(String filename) throws Exception {
        String line;
        StringBuilder buffer = new StringBuilder();
        File file = new File(filename);
        BufferedReader br = new BufferedReader(new FileReader(file));
        while ((line = br.readLine()) != null) {
            buffer.append(line);
        }
        br.close();
        return buffer.toString();
    }

    private static Interval[] getIntervals(int numChunks, int chunkSize) {
        Interval arr[] = new Interval[numChunks];
        int inc = 0;
        for (int i = 0; i < (numChunks * chunkSize); i += chunkSize) {
            arr[inc++] = new Interval(i,i + chunkSize - 1);
        }
        return arr;
    }

    private static List<Character> getLabels(int numChunks) {
        Scanner scanner = new Scanner(System.in);
        List<Character> labels = new ArrayList<Character>();
        int endChar = numChunks == 0 ? 'a' : 'a' + numChunks - 1;
        System.out.printf("Input %d character(s) (\'%c\' - \'%c\') for the pattern.\n", numChunks, 'a', endChar);
        for (int i = 0; i < numChunks; i++) {
            labels.add(scanner.next().charAt(0));
        }
        scanner.close();
        return labels;
    }

        private static char[] runSwapper(String content, int chunkSize, int numChunks) throws InterruptedException {
        List<Character> labels = getLabels(numChunks);
        char[] buffer = new char[numChunks * chunkSize];
        Interval[] intervals = getIntervals(numChunks, chunkSize);
        Interval[] ordered = new Interval[numChunks];

        // TODO: Order the intervals properly, then run the Swapper instances.
        for (int i = 0; i < numChunks; i++) {
            int index = content.toLowerCase().indexOf(labels.get(i)) / chunkSize;
            ordered[i] = intervals[index];
        }
        Thread[] threads = new Thread[numChunks];
        for (int i = 0; i < numChunks; i++) {
            threads[i] = new Thread(new Swapper(ordered[i], content, buffer, i * chunkSize));
            threads[i].start();
        }
        for (int i = 0; i < numChunks; i++) {
            threads[i].join();
        }

        return buffer;
    }

    private static void writeToFile(String contents, int chunkSize, int numChunks) throws Exception {
        char[] buff = runSwapper(contents, chunkSize, contents.length() / chunkSize);
        PrintWriter writer = new PrintWriter("output.txt", "UTF-8");
        writer.print(buff);
        writer.close();
    }

    public static void main(String[] args) throws InterruptedException {
        if (args.length != 2) {
            System.out.println("Usage: java TextSwap <chunk size> <filename>");
            return;
        }
        String contents = "";
        int chunkSize = Integer.parseInt(args[0]);
        try {
            contents = readFile(args[1]);
            int numChunks = contents.length() / chunkSize;
            if (numChunks > 26) {
                System.out.println("Chunk size too small.");
                return;
            }
            if (chunkSize < 0 || (contents.length() % chunkSize != 0)) {
                System.out.println("Chunk size must be positive and file size must be a multiple of the chunk size.");
                return;
            }
            writeToFile(contents, chunkSize, numChunks);
        } catch (Exception e) {
            System.out.println("Error with IO.");
            return;
        }

    }
}