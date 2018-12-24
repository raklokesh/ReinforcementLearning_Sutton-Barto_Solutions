import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

def run_episodes():
    state_value_estimate = np.zeros(21)
    RMSE = np.zeros(EPISODES)
    for episode in range(EPISODES):
        states = []
        reward = []
        current_state = 10
        states.append(current_state)
        time_step = 0
        T = 1
        while True:
            if T>time_step:
                e = np.random.random()
                if e > 0.5:
                    current_state +=1
                else:
                    current_state -=1

                states.append(current_state)
                if current_state == 20:
                    reward.append(1)
                    T = time_step
                elif current_state == 0:
                    reward.append(-1)
                    T = time_step
                else:
                    reward.append(0)
                    T+=1

            update_time = time_step - N_STEP+1
            if update_time >= 0:
                G = 0
                max_time_step = update_time+N_STEP
                if T<=time_step:
                    max_time_step = T+1
                for t in range(update_time,max_time_step):
                    G+= GAMMA**(t-update_time)*reward[t]
                if T>=time_step:
                    G+= GAMMA**(N_STEP)*state_value_estimate[states[update_time+N_STEP]]
                state_value_estimate[states[update_time]]+=ALFA*(G-state_value_estimate[states[update_time]])

            if update_time == T:
                break
            time_step += 1

        RMSE[episode] = (np.sum((state_value_estimate[1:20]-state_value_true)**2)/19)**0.5

    return RMSE

state_value_true = np.arange(-9,10,1)/10

ALFA_CHOICE = [0.1*i for i in range(11)]
N_STEP_CHOICE = [2**i for i in range(7)]
GAMMA = 1
ALFA = 0.4
EPISODES = 10
RUNS = 100
Avg_RMSE_NStep = np.zeros((len(ALFA_CHOICE),len(N_STEP_CHOICE)))
for i,ALFA in enumerate(ALFA_CHOICE):
    print('Running alfa {}'.format(ALFA))
    for j,N_STEP in enumerate(N_STEP_CHOICE):
        print('Running NStep {}'.format(N_STEP))
        Avg_RMSE_run = np.zeros(RUNS)
        for run in range(RUNS):
            Avg_RMSE_run[run] = np.mean(run_episodes())

        Avg_RMSE_NStep[i,j] = np.mean(Avg_RMSE_run)

fig = plt.figure(1,figsize=(12,8))
RMSE_plot = plt.subplot()
x_values = np.linspace(0, 1, 100)
for i,N in enumerate(N_STEP_CHOICE):
    spl = make_interp_spline(ALFA_CHOICE,Avg_RMSE_NStep[:,i],k=3)
    RMSE_values = spl(x_values)
    RMSE_plot.plot(x_values,RMSE_values,label = '{}'.format(N))
RMSE_plot.set_xlabel('alfa')
RMSE_plot.set_ylabel('Avg RMSE')
RMSE_plot.set_xticks([0.2*i for i in range(6)])
RMSE_plot.set_yticks(np.arange(0.25,0.6,0.05))
RMSE_plot.set_ylim((0.25,0.55))
RMSE_plot.legend(title = 'n-step number',loc='center left', bbox_to_anchor=(1, 0.5))