import java.util.ArrayList;

public class Vector {
    ArrayList<Complex> comp;
    public Vector(ArrayList<Complex> _comp) {
        comp = new ArrayList<>();
        comp.addAll(_comp);
    }

    public Vector copy() {
        return new Vector(comp);
    }

    public int size() {
        return comp.size();
    }

    public Complex get(int idx) {
        return comp.get(idx);
    }

    public static Vector product(Vector v, Complex in) {
        ArrayList<Complex> al = new ArrayList<>();
        al.addAll(v.comp);
        for (int i = 0; i < al.size(); i++) {
            al.set(i, al.get(i).multiply(in));
        }
        return new Vector(al);
    }

    public static Vector dotProduct(Vector v0, Vector v1) {
        ArrayList<Complex> out = new ArrayList<>();
        for (int i = 0; i < v0.size(); i++) {
            Complex sum = new Complex(0, 0);
            for (int j = 0; j < v1.size(); j++) {
                sum = sum.add(v0.get(j).multiply(v1.get(j)));
            }
            out.add(sum);
        }
        return new Vector(out);
    }
}
