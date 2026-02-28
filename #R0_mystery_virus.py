#R0_mystery_virus
#import statements
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from patients import Patients

# control settings for virus window search and R0 estimation
infectious_period_days = 5.0
min_window = 7
max_window = 14

# data from data release #1
location = r"/Users/isabelvikesland/Documents/UVA2/BME 2315 - Comp.BME/Module-2-Epidemics-SIR-Modeling/Data/mystery_virus_daily_active_counts_RELEASE#1.csv"
patients = Patients.instantiate_from_csv(location)

# data for fitting: days and active cases in empty lists
days = []
cases = []
for p in patients:
    days.append(p.day)
    cases.append(p.number_of_cases if p.number_of_cases > 0 else 1e-6)

# fit log(I) = r * t + log(I0) for each window and find the best fit based on R^2
def fit_exp_window(tw, Iw):
    """
    Fit log(I) = r * t + log(I0).
    Returns r, I0, r2 (R-squared on log-scale).
    """
    logI = [np.log(val) for val in Iw]
    r, logI0 = np.polyfit(tw, logI, 1)
    logI_pred = [r * ti + logI0 for ti in tw]
    ss_res = sum((logI[i] - logI_pred[i]) ** 2 for i in range(len(logI)))
    mean_logI = sum(logI) / len(logI)
    ss_tot = sum((val - mean_logI) ** 2 for val in logI)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else None
    I0 = np.exp(logI0)
    return r, I0, r2

#I used ClaudeAi to help me write the equations for fitting the exponential window, 
# calculating the R0 and helping me work back from the game ODE's

# best exponential fit parameters

best = None  # (r2, r, I0, t_start, t_end)
n = len(days)

# for loop to iterate through all possible windows of the data and fit an exponential curve to each window
# calculating the R^2 value for each fit and keeping track of the best fit based on R^2

for w in range(min_window, max_window + 1):
    for i in range(0, n - w + 1):
        tw = days[i:i+w]
        Iw = cases[i:i+w]
        if all(v == Iw[0] for v in Iw):
            continue
        r, I0, r2 = fit_exp_window(tw, Iw)
        if r2 is None:
            continue
        if (best is None) or (r2 > best[0]):
            best = (r2, r, I0, tw[0], tw[-1])

if best is None:
    print("ERROR could not find a good exponential window. Check data.")

best_r2, r, I0, t_start, t_end = best

# calcculate R0 and doubling time based on r 
doubling_time = np.log(2) / r if r > 0 else float('inf')
R0 = 1.0 + r * infectious_period_days

# print statements so i don't have to look at the graph 
print("Best exponential window: day " + str(t_start) + " to " + str(t_end) + " (length " + str(t_end - t_start + 1) + ")")
print("Fit on log(I): R^2 = " + str(round(best_r2, 4)))
print("Growth rate r: " + str(round(r, 4)) + " per day")
print("Doubling time: " + str(round(doubling_time, 2)) + " days")
print("Assumed infectious period D: " + str(infectious_period_days) + " days")
print("Estimated R0 = 1 + r*D = " + str(round(R0, 3)))

# matplotlib to plot graph w/new exponential fit and R^2

t_fit = list(np.linspace(min(days), max(days), 300))
I_fit = [I0 * np.exp(r * ti) for ti in t_fit]

#I used ClaudeAi to help me figure out the t_fit and I_fit equations for plotting the exponential fit curve on the graph

#formatting the graph, I used ClaudeAi to figure out how to squish the graph to make it look better
plt.figure(figsize=(9, 5.5))
plt.scatter(days, cases, s=28, alpha=0.8, label="Observed I(t)")
plt.plot(t_fit, I_fit, 'r', lw=2.0,label="Fitted exponential: I(t)=I0*e^(r*t)\n(r=" + str(round(r, 3)) + "/day, R^2=" + str(round(best_r2, 3)) + ")")
plt.axvspan(t_start, t_end, color="orange", alpha=0.15, label="Fit window")
plt.xlabel("Day")
plt.ylabel("Active infections")
plt.title("Exponential Fit to Mystery Virus Growth (for R0 estimate)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()