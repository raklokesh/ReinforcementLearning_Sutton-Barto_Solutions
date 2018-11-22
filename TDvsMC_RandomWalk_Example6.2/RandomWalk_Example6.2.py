
import numpy as np
import matplotlib.pyplot as plt

def run():
    state_value_estimate_TD = np.array([0, 0.5, 0.5, 0.5, 0.5, 0.5, 0])
    state_value_estimate_MC = np.array([0, 0.5, 0.5, 0.5, 0.5, 0.5, 0])

    RMSE_TD = np.zeros(Episodes)
    RMSE_MC = np.zeros(Episodes)

    for episode in range(Episodes):
        states= []
        reward = []

        terminated = False
        current_state = 3
        states.append(current_state)
        while not terminated:
            old_state = current_state
            e = np.random.random()
            if e > 0.5:
                current_state +=1
            else:
                current_state -=1

            states.append(current_state)
            if current_state == 6:
                reward.append(1)
            else:
                reward.append(0)

            state_value_estimate_TD[old_state] = state_value_estimate_TD[old_state] + alfa * (
                    reward[-1] + state_value_estimate_TD[current_state] - state_value_estimate_TD[old_state])

            if current_state == 6 or current_state == 0:
                terminated = True

        RMSE_TD[episode] = (np.sum((state_value_estimate_TD[1:6] - state_value_true) ** 2)/5) ** 0.5

        #Calculate states value esimate by MC method
        G = 0
        for step in np.arange(1,len(reward)+1):
            G = reward[-step] + G
            state_value_estimate_MC[states[-step-1]] = state_value_estimate_MC[states[-step-1]] + alfa*(G - state_value_estimate_MC[states[-step-1]])

        RMSE_MC[episode] = (np.sum((state_value_estimate_MC[1:6] - state_value_true) ** 2)/5) ** 0.5

        plot_state = False
        if plot_state:
            if episode in np.array([0,9,99]):
                if episode == 0:
                    plt.figure(1, figsize=(10, 8))
                    value_plot = plt.subplot()
                    value_plot.plot(np.arange(1,6),np.repeat(0.5,5),label = '0',marker='o')

                value_plot.plot(np.arange(1,6), state_value_estimate_TD[1:6], label = str(episode + 1), marker='o')

                if episode == 99:
                    value_plot.plot(np.arange(1, 6), np.arange(1, 6) / 6, label='True value', marker='o')
                value_plot.set_yticks(np.arange(0, 1.2, 0.2))
                value_plot.set_xticks(np.arange(1, 6))
                value_plot.set_xticklabels(['A', 'B', 'C', 'D', 'E'])
                value_plot.set_xlabel('State')
                value_plot.set_ylabel('Estimated value of state')
                value_plot.legend()
                plt.savefig('State_Value_TDmethod(alfa = 0.1).png')

    return RMSE_TD,RMSE_MC



def run_alfa():
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

    return RMSE_Avg_TD,RMSE_Avg_MC

state_value_true = np.arange(1,6)/6
Episodes = 100

alfa_choice = [0.05,0.15]
RMSE_alfa_TD = []
for alfa in alfa_choice:
    print('Running TD for alfa {}'.format(alfa))
    RMSE_Avg_TD,RMSE_Avg_MC = run_alfa()
    RMSE_alfa_TD.append(RMSE_Avg_TD)

alfa_choice = [0.01,0.04]
RMSE_alfa_MC = []
for alfa in alfa_choice:
    print('Running MC for alfa {}'.format(alfa))
    RMSE_Avg_TD,RMSE_Avg_MC = run_alfa()
    RMSE_alfa_MC.append(RMSE_Avg_MC)

plot_RMS = True
if plot_RMS:
    plt.figure(1, figsize=(10, 8))
    RMS_plot = plt.subplot()
    RMS_plot.plot(np.arange(1,Episodes+1),RMSE_alfa_TD[0], color = 'xkcd:blue',label = 'TD method alfa = 0.05')
    RMS_plot.plot(np.arange(1,Episodes+1), RMSE_alfa_TD[1], color = 'xkcd:blue', linestyle = 'dashed',label = 'TD method alfa = 0.15')
    RMS_plot.plot(np.arange(1,Episodes+1),RMSE_alfa_MC[0], color = 'xkcd:red',label = 'MC method alfa = 0.01')
    RMS_plot.plot(np.arange(1,Episodes+1), RMSE_alfa_MC[1], color = 'xkcd:red', linestyle = 'dashed',label = 'MC method alfa = 0.04')

    RMS_plot.set_yticks(np.arange(0, 0.26, 0.05))
    RMS_plot.set_xticks(np.arange(0,101,25))
    RMS_plot.set_xlabel('Walks/Episodes')
    RMS_plot.set_ylabel('Average RMS Error (100 runs)')
    RMS_plot.legend()

    plt.savefig('RMSError_plot.png')