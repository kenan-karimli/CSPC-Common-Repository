"""
PW2 Lab B Part 5 (bonus) -- find a titration's equivalence point.

titration.csv holds a titration curve: pH versus the volume of base added.
The equivalence point is the volume where the pH changes fastest (the steep
jump). Numerically, that is where the SLOPE of the pH curve is largest.
Run:  python titration.py
"""
import numpy as np
import matplotlib.pyplot as plt

# TODO 1: read titration.csv (columns volume_base, pH) into arrays V, pH.

with open("titration.csv") as f:
    V, pH = np.loadtxt(f, delimiter=",", skiprows=1, unpack=True)

# TODO 2: compute the slope of the pH curve with np.gradient(pH, V), and find
#         the volume where that slope is largest (np.argmax). That is the
#         equivalence point. Print it.

slope = np.gradient(pH, V)
equivalence_index = np.argmax(slope)
equivalence_volume = V[equivalence_index]
print(f"Equivalence point volume: {equivalence_volume:.3f} mL")

# TODO 3: make two plots side by side: (left) pH vs volume with a line at the
#         equivalence point; (right) the slope vs volume, showing it peaks
#         at the equivalence point. Save as titration.png.

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(V, pH, label="pH curve")
ax1.axvline(equivalence_volume, color='r', linestyle='--', label="Equivalence point")
ax1.set_xlabel("Volume of base added (mL)")
ax1.set_ylabel("pH")
ax1.set_title("Titration Curve")
ax1.legend()


ax2.plot(V, slope, label="Slope of pH curve")
ax2.axvline(equivalence_volume, color='r', linestyle='--', label="Equivalence point")
ax2.set_xlabel("Volume of base added (mL)")
ax2.set_ylabel("Slope of pH curve")
ax2.set_title("Slope of Titration Curve")
ax2.legend()
plt.tight_layout()
plt.savefig("titration.png")