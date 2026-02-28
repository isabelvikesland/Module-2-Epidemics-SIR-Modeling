import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Load real outbreak data
data = pd.read_csv('Code/mystery_virus_daily_active_counts_RELEASE#1.csv')
infected_real = data["active reported daily cases"].values
days = data["day"].values

# Total population (assumption)
N = 450

# Initial conditions
I0 = infected_real[0]
R0 = 0
S0 = N - I0 - R0

# SIR differential equations
def sir_model(y, t, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# time points
t = np.linspace(0, len(days)-1, len(days))

# initial guesses (we will tune these)
beta = 0.17
gamma = 0.03
R0 = beta / gamma
print("Estimated basic reproduction number R0 =", R0)
# solve ODE
solution = odeint(sir_model, [S0, I0, R0], t, args=(beta, gamma))
S, I, R = solution.T

# Plot comparison
plt.figure(figsize=(9,5))
plt.plot(days, infected_real, 'ro', label="Real infected")
plt.plot(days, I, 'b-', label="SIR model infected")

plt.xlabel("Days")
plt.ylabel("Infected People")
plt.title("Real Outbreak vs SIR Model")
plt.legend()
plt.savefig("sir_model_fit.png", dpi=300)
plt.show()