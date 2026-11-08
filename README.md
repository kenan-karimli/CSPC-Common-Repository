# CSPC - Computer Science for Physics and Chemistry

My coursework repository. Each practical is under PW<n>/Lab <X>/.

## Setup
Create the environment for a given lab:
    conda env create -f PW<n>/Lab\ <X>/environment.yml
    conda activate cspc

---

## PW1 - Lab A: Reproducible Foundations

**What I built:**
- Unit tests in `test_decay.py` verifying exponential decay physics, initial conditions, and negative rate validation.
- Performance benchmarking script (`speed.py`) comparing pure-Python loops against vectorised NumPy implementations.

**Speed comparison (loop vs NumPy):**
- loop   : 1.9497 s
- numpy  : 0.0002 s
- speed-up: 11577.2 x faster

**Tests:** all passing? yes

**Conclusion:**
- Vectorised NumPy binomial operations (`rng.binomial`) significantly outperform pure-Python atom-by-atom loops by eliminating interpreter overhead and inner loops.
- All three unit tests passed successfully, proving that vectorisation maintains statistical physical accuracy against the analytical law $N(t) = N_0 e^{-\lambda t}$.
- Environment setup via Conda ensures seamless cross-machine execution and reproducibility.

**Reproducibility Test (Stretch Goal):**
- Tested with partner repository clone: The environment built seamlessly using `environment.yml` and all tests passed via `pytest -v` without requiring code modifications.


---

## PW1 --- Lab B: Data, Plotting, and Automation

**What the data showed:**
The observed radioactive decay dataset (`decay_observed.csv`) demonstrates a clear exponential decrease in remaining count over time.

**Comparison with analytical law:**
The observed scatter plot closely follows the smooth analytical decay curve $N(t) = N_0 e^{-\lambda t}$, confirming that the empirical data strongly matches theoretical physical predictions.

**Snakemake pipeline:**
The Snakemake workflow automates the execution of `plot.py` to regenerate `figure.png` whenever the underlying dataset or code is updated, ensuring complete computational reproducibility.ss

---

## PW2 --- Lab A: Derivatives, Noise, and Integration

**What I built:**
- Computed velocity ($v$) and acceleration ($a$) from noisy free-fall position tracking data using `np.gradient`.
- Integrated acceleration back up to recover velocity ($v_{\text{rec}}$) and position ($y_{\text{rec}}$) using `scipy.integrate.cumulative_trapezoid`.
- Produced a 3-panel figure saved as `motion.png` showing position, velocity, and acceleration against time.

**Acceleration statistics:**
- Mean acceleration: -8.58 m/s²
- Standard deviation of acceleration: 28.72 m/s²
- Maximum difference between original and recovered position: 0.78 m

**Why acceleration was noisy:**
Numerical differentiation magnifies measurement noise because computing rates of change between adjacent time steps divides tiny random position fluctuations by very small time intervals ($\Delta t$), causing two successive derivatives to swing wildly even when the position curve appears smooth.

**What integrating back showed:**
Numerical integration suppresses random noise because summing up values step-by-step allows positive and negative fluctuations to cancel out. The recovered position matched the original trajectory within 0.78 m despite the extreme noise in the acceleration data.

**Bonus (2D Trajectory):**
- Analyzed `trajectory.csv` by computing $v_x = \frac{dx}{dt}$ and $v_y = \frac{dy}{dt}$ using `np.gradient`.
- Calculated overall speed $\sqrt{v_x^2 + v_y^2}$ and saved the visualizations as `trajectory.png`.

---

## PW3 --- Data, Distributions, Testing, and Causation

**Datasets:**
- `Heart_disease_cleveland_new.csv`: Cleveland Heart Disease dataset (303 patients, 14 columns). Source: UCI Machine Learning Repository (Janosi, Steinbrunn, Pfisterer, Detrano, 1988), via Kaggle.
- `chemicals_cancer.csv`: synthetic chemical-exposure dataset (1000 patients) provided on Moodle.

**What I built:**
- `session1.py`: loads the heart data with pandas, plots histograms of `age`, `chol`, `trestbps`, `thalach` (`distributions.png`) and Q-Q plots (`qqplots.png`), and runs a Shapiro-Wilk test on each variable.
- `session2.py`: group comparison of `thalach` (`thalach_means.png`), age/heart-rate correlation (`age_thalach.png`), the chemical confounding analysis (`confounding.png`) and the entropy bonus.

### Session 1 --- Characterise the data

**Shape of each variable:**
- `age`: roughly bell-shaped, centred around 55-60, with a slightly longer tail toward younger patients (skew = -0.21).
- `chol`: skewed to the right (skew = 1.13). Most values fall between 200 and 300, with a long tail of high outliers up to 564.
- `trestbps`: right-skewed (skew = 0.70) and lumpy, with peaks at round values (120, 130, 140) because blood pressure is usually rounded when recorded.
- `thalach`: left-skewed (skew = -0.53). Most patients reach 140-180 bpm, with a tail of low maximum heart rates.

**Normality verdicts (Shapiro-Wilk, alpha = 0.05 + Q-Q plots):**

| Variable | W | p-value | Verdict |
|---|---|---|---|
| age | 0.9865 | 0.0061 | not normal (close to normal by eye) |
| chol | 0.9473 | 5.9e-09 | not normal |
| trestbps | 0.9665 | 1.8e-06 | not normal |
| thalach | 0.9765 | 7.0e-05 | not normal |

**Reasoning:** for every variable, p < 0.05, so the null hypothesis of normality is rejected. The Q-Q plots agree: `chol` and `trestbps` bend upward at the high end (right tail), `thalach` bends at the low end (left tail). `age` lies close to the line, and it fails the test only mildly, so it is "nearly normal". Because none of the variables pass, Session 2 uses rank-based (non-parametric) methods.

### Session 2 --- Draw conclusions

**Is the effect real? (thalach: disease vs healthy)**
- Method: Mann-Whitney U test, because `thalach` is not normal (a Welch t-test was also run as a cross-check).
- Mann-Whitney U = 5806.5, p = 1.9e-13 (Welch t = -7.86, p = 9.1e-14).
- Disease (n = 139): mean thalach = 139.3 ± 1.9 bpm (SEM)
- Healthy (n = 164): mean thalach = 158.4 ± 1.5 bpm (SEM)
- **Conclusion:** the difference is real. Heart-disease patients reach a maximum heart rate about 19 bpm lower than healthy patients. In `thalach_means.png` the two error bars are far apart and do not overlap, which agrees with the very small p-value.

**Do age and thalach move together?**
- Spearman rho = -0.392 (p = 1.5e-12); Pearson r = -0.394. The fitted slope is about -1 bpm per year.
- **Interpretation:** there is a moderate negative relationship: older patients tend to reach a lower maximum heart rate. The scatter in `age_thalach.png` is wide, though, so age explains only a part of the variation (rho² ≈ 0.15).

**Chemical mystery --- naive analysis:**
- benzene vs malignancy: r = 0.385
- cadmium vs malignancy: r = 0.880
- At face value, **cadmium** looks like the cause.

**Chemical mystery --- look again (controlling for pollution_index):**
- The correlation matrix shows cadmium is almost the same thing as pollution (r = 0.982), and pollution itself correlates with malignancy at r = 0.895. That makes pollution a suspected confounder.
- Stratification: I restricted the data to narrow pollution bands (5 units wide) and recomputed the correlations inside each band:
  - benzene: r = 0.64 to 0.87 in every band. **The association survives and even gets stronger.**
  - cadmium: r between -0.19 and +0.19 in every band, i.e. about zero. **The association disappears.**
- Partial correlation (residuals after removing the linear effect of pollution): benzene r = 0.755, cadmium r = 0.013.
- Wide bands (such as 40-60) are not enough: cadmium still shows r ≈ 0.3 there, because inside a wide band cadmium still tracks pollution.

**Conclusion:** **benzene is the real cause of malignancy; cadmium only looked guilty.** High-pollution areas have both high cadmium and high malignancy, so cadmium correlates with malignancy without causing it. Once patients with the same pollution level are compared, cadmium no longer predicts malignancy, while benzene still does. In the full data, benzene's effect was hidden by the large pollution-driven variation in malignancy, which is why its naive r was low.

**Bonus --- how unpredictable is a category? (Shannon entropy H = -Σ p log₂ p)**
- `target`: 54.1% healthy / 45.9% disease → H = 0.995 bits (max 1). Almost perfectly balanced, so it is close to the hardest case to guess.
- `sex`: 68% male / 32% female → H = 0.905 bits. Lopsided, so it is easier to guess (always guessing "male" is right 68% of the time).
