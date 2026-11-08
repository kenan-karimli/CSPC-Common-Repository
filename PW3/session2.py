"""
PW3 Session 2 -- Draw conclusions.

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

heart = pd.read_csv("Heart_disease_cleveland_new.csv", encoding="utf-8-sig")


# thalach not normal so used mann whitney
disease = heart.loc[heart["target"] == 1, "thalach"]
healthy = heart.loc[heart["target"] == 0, "thalach"]
U, p_mw = stats.mannwhitneyu(disease, healthy, alternative="two-sided")
print(f"Mann-Whitney U = {U:.1f}, p = {p_mw:.3g}")

means = heart.groupby("target")["thalach"].mean()
print(f"Mean thalach for healthy: {means[0]:.1f}, Meanthalach for disease: {means[1]:.1f}")

fig = plt.figure(figsize=(6, 4))
plt.boxplot([healthy, disease], labels=["Healthy", "Disease"])
plt.title("Boxplot of thalach by target")
plt.ylabel("thalach")
plt.savefig("thalach_boxplot.png")

