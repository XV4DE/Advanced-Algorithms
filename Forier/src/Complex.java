public class Complex {
    double real, imaginary;
    public Complex (double _real, double _imaginary) {
        real = _real;
        imaginary = _imaginary;
    }

    public Complex multiply (Complex other) {
        return new Complex(real * other.real - imaginary * other.imaginary,
                real * other.imaginary + imaginary * other.real);
    }

    public Complex add (Complex other) {
        return new Complex(real + other.real, imaginary + other.imaginary);
    }

    public boolean equals(Complex other) {
        return real == other.real && imaginary == other.imaginary;
    }

    @Override
    public String toString() {
        return "" + real + " + " + imaginary + "i";
    }
}
