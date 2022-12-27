double division(double a, double b)
{

    double b_abs = abs_d(b);

    if (b_abs < 1e-12)
    {
        return a * b / (b_abs * (b_abs + 1e-12));
    }
    else
    {
        return a / b;
    }
}