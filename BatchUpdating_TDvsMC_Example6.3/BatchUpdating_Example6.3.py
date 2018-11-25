# Algorithm for batch updating

import numpy as np
import matplotlib.pyplot as plt
import copy
from decimal import Decimal

state_value_true = np.arange(1,6)/6

alfa_TD = 0.001
alfa_MC = 0.001
Episodes = 100


def run():
    state_value_estimate_TD = np.array([0, 0.5, 0.5, 0.5, 0.5, 0.5, 0])
    state_value_estimate_MC = np.array([0, 0.5, 0.5, 0.5, 0.5, 0.5, 0])

    states = []
    reward = []

    RMSE_TD = np.zeros(Episodes)
    RMSE_MC = np.zeros(Episodes)

    for episode in range(Episodes):
        terminated = False
        current_state = 3
        states.append(current_state)
        while not terminated:
            old_state = current_state
            e = np.random.random()
            if e > 0.5:
                current_state += 1
            else:
                current_state -= 1

            states.append(current_state)
            if current_state == 6:
                reward.append(1)
            else:
                reward.append(0)

            if current_state == 6 or current_state == 0:
                terminated = True

        # TD method batch updating
        converged = False
        while not converged:
            state_value_increments = [[0] for i in range(7)]
            reward_step = 0
            for step in range(len(states)):
                if states[step] not in [0,6]:
                    state_value_increments[states[step]].append(reward[reward_step] + state_value_estimate_TD[states[step+1]] - state_value_estimate_TD[states[step]])
                    reward_step+=1

            old_state_estimate = copy.copy(state_value_estimate_TD)

            for state in np.arange(1,6):
                state_value_estimate_TD[state] = state_value_estimate_TD[state] + alfa_TD * np.sum(state_value_increments[state])

            if abs(np.sum(state_value_estimate_TD - old_state_estimate)) < 10**-2:
                converged = True

        RMSE_TD[episode] = (np.sum((state_value_estimate_TD[1:6] - state_value_true) ** 2) / 5) ** 0.5

        # MC method batch updating
        converged = False
        while not converged:
            state_value_increments = [[0] for i in range(7)]
            reward_step = 1
            for step in np.arange(1,len(states)+1):
                if states[-step] not in [0, 6]:
                    G = G + reward[-reward_step]
                    state_value_increments[states[-step]].append( G - state_value_estimate_MC[states[-step]])
                    reward_step += 1
                else:
                    G = 0

            old_state_estimate = copy.copy(state_value_estimate_MC)

            for state in np.arange(1, 6):
                state_value_estimate_MC[state] = state_value_estimate_MC[state] + alfa_MC * np.sum(
                    state_value_increments[state])

            if abs(np.sum(state_value_estimate_MC - old_state_estimate)) < 10 ** -2:
                converged = True

        RMSE_MC[episode] = (np.sum((state_value_estimate_MC[1:6] - state_value_true) ** 2) / 5) ** 0.5

    return RMSE_TD, RMSE_MC

runs = 100

RMSE_Sum_TD = np.zeros(Episodes)
RMSE_Sum_MC = np.zeros(Episodes)
for run_number in range(runs):
    if run_number in np.arange(0,runs,runs/10):
        print('Run number {}'.format(run_number))
    RMSE_TD, RMSE_MC = run()

    RMSE_Sum_TD = RMSE_Sum_TD + RMSE_TD
    RMSE_Sum_MC = RMSE_Sum_MC + RMSE_MC

RMSE_Avg_TD = RMSE_Sum_TD/runs
RMSE_Avg_MC = RMSE_Sum_MC/runs


plt.figure(figsize=(10,8))
RMS_plot = plt.subplot()
RMS_plot.plot(np.arange(1, Episodes +1), RMSE_Avg_TD, color = 'xkcd:blue', label = 'TD method alfa = {}'.format(alfa_TD))
RMS_plot.plot(np.arange(1, Episodes +1), RMSE_Avg_MC, color = 'xkcd:red', label = 'MC method alfa = {}'.format(alfa_MC))
RMS_plot.set_yticks(np.arange(0, 0.26, 0.05))
RMS_plot.set_xticks(np.arange(0, 101, 25))
RMS_plot.set_xlabel('Walks/Episodes')
RMS_plot.set_ylabel('Average RMS Error (100 runs)')
RMS_plot.legend()

plt.savefig('RMS_TDvsMC_alfa = ({}, {}).png'.format(alfa_TD,alfa_MC))