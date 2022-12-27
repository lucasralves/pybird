from scipy.optimize import newton_krylov

class A:

    def __init__(self) -> None:
        self.a = 0.5

    def solve(self):

        def fun(x):
            return [x[0] + self.a * x[1] - 1.0,
                    self.a * (x[1] - x[0]) ** 2]
        
        self.sol = newton_krylov(fun, [0, 0])

        return

a = A()

a.solve()
print(a.sol)