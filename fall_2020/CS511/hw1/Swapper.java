public class Swapper implements Runnable {
    private int offset;
    private Interval interval;
    private String content;
    private char[] buffer;

    public Swapper(Interval interval, String content, char[] buffer, int offset) {
        this.offset = offset;
        this.interval = interval;
        this.content = content;
        this.buffer = buffer;
    }

    public int startIndex() {
        return this.interval.getX();
    }
    public int endIndex() {
        return this.interval.getY();
    }

    @Override
    public void run() {
        int inc = startIndex();
        for (int i = offset; i <= offset + (endIndex() - startIndex()); i++) {
            buffer[i] = content.charAt(inc++);
        }

        // TODO: Implement me!
    }
}