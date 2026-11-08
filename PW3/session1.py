"""
PW3 Session 1 -- Characterise the heart-disease data.
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

COLS = ["age", "chol", "trestbps", "thalach"]

df = pd.read_csv("Heart_disease_cleveland_new.csv", encoding="utf-8-sig")  # utf-8-sig otherwise first column name is weird
print("Shape:", df.shape)
print(df.head())
cont = df[COLS]

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for ax, col in zip(axes.flat, COLS):
    ax.hist(cont[col], bins=25, color="steelblue", edgecolor="black")
    ax.set_title(f"{col} (skew = {stats.skew(cont[col]):.2f})")
    ax.set_xlabel(col)
    ax.set_ylabel("Count")
    ax.grid(True)
plt.tight_layout()
plt.savefig("distributions.png")
print("distributions.png generated successfully.")

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for ax, col in zip(axes.flat, COLS):
    stats.probplot(cont[col], dist="norm", plot=ax)
    ax.set_title(f"Q-Q plot: {col}")
    ax.grid(True)
plt.tight_layout()
plt.savefig("qqplots.png")
print("qqplots.png generated successfully.")

for col in COLS:
    W, p = stats.shapiro(cont[col])
    verdict = "approximately normal" if p > 0.05 else "NOT normal"
    print(f"{col:9s}: W = {W:.4f}, p = {p:.4g}, skew = {stats.skew(cont[col]):.2f} -> {verdict}")
