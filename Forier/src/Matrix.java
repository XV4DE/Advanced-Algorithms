import java.util.ArrayList;

public class Matrix {
    ArrayList<ArrayList<Complex>> nums;
    public Matrix (ArrayList<ArrayList<Complex>> _nums) {
        nums = _nums;
    }

    public Matrix dotProduct (Matrix other) {
        ArrayList<ArrayList<Complex>> out = new ArrayList<>();
        for (int i = 0; i < nums.size(); i++) {
            out.add(vectorDotProduct(nums.get(i), other.nums.get(i)));
        }
        return new Matrix(out);
    }

    public ArrayList<Complex> dotProduct (ArrayList<Complex> other) {
        ArrayList<Complex> out = new ArrayList<>();
        for (ArrayList<Complex> num : nums) {
            Complex sum = new Complex(0, 0);
            for (int j = 0; j < nums.get(0).size(); j++) {
                sum = sum.add(num.get(j).multiply(other.get(j)));
            }
            out.add(sum);
        }
        return out;
    }

    private ArrayList<Complex> vectorDotProduct(ArrayList<Complex> a, ArrayList<Complex> b) {
        ArrayList<Complex> out = new ArrayList<>();
        for (int i = 0; i < a.size(); i++) {
            out.add(a.get(i).multiply(b.get(i)));
        }
        return out;
    }

    public static Matrix nRoots(int n) {
        ArrayList<ArrayList<Complex>> out = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            out.add(new ArrayList<>());
            for (int j = 0; j < n; j++) {
                double realComponent = round(Math.cos(2 * Math.PI * j * i / n), 15);
                double imagComponent = round(Math.sin(2 * Math.PI * j * i / n), 15);
                out.get(i).add(new Complex(realComponent, imagComponent));
            }
        }
        return new Matrix(out);
    }

    public void print() {
        for (ArrayList<Complex> vector : nums) {
            System.out.print("[");
            for (Complex num : vector) {
                System.out.print(num.toString() + ", ");
            }
            System.out.println("]");
        }
    }

    private static double round(double n, int places) {
        return ((double) Math.round(n*Math.pow(10, places)))/Math.pow(10, places);
    }
}
