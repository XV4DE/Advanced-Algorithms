import java.util.ArrayList;

public class Test {
    static int passes = 0;
    static int attempts = 0;
    public static void main(String[] args) {
        passOnTrue(testComplexMultiply());
        passOnTrue(testComplexAddition());
        passOnTrue(testNRoots());
        passOnTrue(testFourier());
        System.out.println("Passed " + passes + " tests of " + attempts);
    }

    public static void passOnTrue (boolean t) {
        attempts++;
        if (t) passes++;
    }

    public static boolean testComplexMultiply() {
        Complex c0 = new Complex(0, 0);
        for (int i  = 0; i < 100; i++) {
            for (int j = 0; j < 100; j++) {
                if (!c0.multiply(new Complex(i, j)).equals(c0)) {
                    System.out.println("" + i + " " + j);
                    return false;
                }
            }
        }
        return true;
    }

    public static boolean testComplexAddition() {
        Complex c0 = new Complex(0, 0);
        for (int i  = 0; i < 100; i++) {
            for (int j = 0; j < 100; j++) {
                if (!c0.add(new Complex(i, j)).equals(new Complex(i, j))) {
                    System.out.println("" + i + " " + j);
                    return false;
                }
            }
        }
        return true;
    }

    public static boolean testNRoots() {
        for (int i = 1; i < 100; i++) {
            Matrix roots = Matrix.nRoots(i);
            for (int j = 0; j < i; j++) {
                if (!roots.nums.get(0).get(j).equals(new Complex(1, 0)) ||
                        !roots.nums.get(j).get(0).equals(new Complex(1, 0))) {
                    return false;
                }
            }
        }
        return true;
    }

    public static boolean testFourier() {
        ArrayList<Complex> signal = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            signal.add(new Complex(0, 0));
        }

        if (!Matrix.equal(Matrix.Fourier(signal), signal)) {
            System.out.println(Matrix.Fourier(signal));
            return false;
        }


        ArrayList<Complex> signaltwo = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            signaltwo.add(new Complex(1, 0));
        }
        ArrayList<Complex> correct = new ArrayList<>();
        correct.add(new Complex(1, 0));
        for (int i = 0; i < 9; i++) {
            correct.add(new Complex(0, 0));
        }
        if (!Matrix.equal(Matrix.Fourier(signaltwo), correct)) {
            System.out.println(Matrix.Fourier(signaltwo));
            return false;
        }
        return true;
    }



}
