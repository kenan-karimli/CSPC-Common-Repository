"""
PW2 Lab B Part 4 -- chemical equilibrium via the equilibrium constant K.

Reaction  H2 + I2 <=> 2 HI, starting from 1 mol H2 and 1 mol I2.
As the reaction proceeds by an extent x:  H2 = 1-x,  I2 = 1-x,  HI = 2x.
At equilibrium the composition satisfies the equilibrium constant
        K = [HI]^2 / ([H2][I2]) = (2x)^2 / ((1-x)(1-x)).
Given K, find the extent x. Solve it TWO ways and compare.
Run:  python equilibrium.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton, minimize

K = 15.6
a = b = 1.0

# TODO 1: write k_imbalance(x) = (2x)^2/((a-x)(b-x)) - K.
#         It equals zero exactly at equilibrium.
k_imbalance = lambda x: (2*x)**2 / ((a-x)*(b-x)) - K

# TODO 2 (method 1): use scipy.optimize.newton to find the root of k_imbalance
#         (start x0=0.5). This is root-finding.
x0 = 0.5
x_eq1 = newton(k_imbalance, x0)

# TODO 3 (method 2): use scipy.optimize.minimize to minimise k_imbalance(x)**2
#         (method "SLSQP", bounds [(0, 0.999)], x0=[0.5]). Print both answers
#         and confirm they agree.
x_eq2 = minimize(lambda x: k_imbalance(x)**2, x0=[0.5], method="SLSQP", bounds=[(0, 0.999)]).x[0]

print(f"Equilibrium extent (root-finding): {x_eq1:.4f}")
print(f"Equilibrium extent (minimization): {x_eq2:.4f}")

# TODO 4: report the equilibrium amounts (H2, I2, HI), and plot how the three
#         amounts change with the extent x, marking the equilibrium. Save
#         equilibrium.png.

x_values = np.linspace(0, 0.999, 100)
H2_values = a - x_values
I2_values = b - x_values
HI_values = 2 * x_values

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x_values, H2_values, label="H2 (a-x)")
ax.plot(x_values, I2_values, label="I2 (b-x)")
ax.plot(x_values, HI_values, label="HI (2x)")
ax.axvline(x_eq1, color='k', linestyle='--', label=f'Equilibrium x={x_eq1:.4f}')
ax.set_xlabel("Extent of reaction x (mol)")
ax.set_ylabel("Amount (mol)")
ax.set_title("Chemical Equilibrium: H2 + I2 <=> 2 HI")
ax.legend()
plt.grid(True)
plt.savefig("equilibrium.png")