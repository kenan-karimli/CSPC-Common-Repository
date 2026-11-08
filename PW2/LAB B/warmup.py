"""
PW2 Lab B Part 2 -- three routes to a minimum.

Compare gradient descent, Newton, and SLSQP on two functions:
  2A: f(x) = (x-3)**2 + 1          (easy, one minimum at x=3)
  2B: g(x) = x**4 - 3*x**2 + x + 5 (harder, several stationary points)
Run:  python warmup.py
"""
import numpy as np
from scipy.optimize import newton, minimize

# ---------- 2A: easy convex function ----------
def f(x):   return (x-3)**2 + 1
def df(x):  return 2*(x-3)
def d2f(x): return 2.0

# TODO 2A: minimise f three ways from x0=0 and print each result:
#   (1) gradient descent by hand (loop x = x - lr*df(x) until the step is tiny)
#   (2) scipy.optimize.newton(df, x0, fprime=d2f)
#   (3) scipy.optimize.minimize(f, x0, method="SLSQP")
starting_points = [0]
for x0 in starting_points:
    # gradient descent
    x = x0
    lr = 0.1
    for _ in range(100):
        step = lr * df(x)
        if abs(step) < 1e-6:
            break
        x -= step
    print(f"Gradient descent from {x0}: x={x}, f(x)={f(x)}")

    # Newton's method
    x_newton = newton(df, x0, fprime=d2f)
    print(f"Newton's method from {x0}: x={x_newton}, f(x)={f(x_newton)}")

    # SLSQP
    res = minimize(f, x0, method="SLSQP")
    print(f"SLSQP from {x0}: x={res.x[0]}, f(x)={res.fun}")

# ---------- 2B: harder landscape ----------
def g(x):   return x**4 - 3*x**2 + x + 5
def dg(x):  return 4*x**3 - 6*x + 1
def d2g(x): return 12*x**2 - 6

# TODO 2B: run the same three methods on g, from x0=0 AND from x0=2.
#   For Newton (which solves dg(x)=0), also check the sign of d2g at the answer:
#   d2g > 0 means a minimum, d2g < 0 means a maximum.
#   In your README note: do the methods agree? did Newton find a minimum or
#   another stationary point? how did the starting point change the result?

starting_points = [0, 2]
for x0 in starting_points:
    # (1) gradient descent
    x = x0
    lr = 0.01
    for _ in range(1000):
        step = lr * dg(x)
        if abs(step) < 1e-6:
            break
        x -= step
    print(f"Gradient descent from {x0}: x={x}, g(x)={g(x)}")

    # (2) Newton's method
    x_newton = newton(dg, x0, fprime=d2g)
    print(f"Newton's method from {x0}: x={x_newton}, g(x)={g(x_newton)}, d2g={d2g(x_newton)}")

    # (3) SLSQP
    res = minimize(g, x0, method="SLSQP")
    print(f"SLSQP from {x0}: x={res.x[0]}, g(x)={res.fun}")
