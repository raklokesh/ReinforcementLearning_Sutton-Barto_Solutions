import numpy as np
import matplotlib.pyplot as plt
Episodes = 10000

def run_episodes(policy):
    Returns = np.zeros(Episodes)
    ImpSampRatios = np.zeros(Episodes)
    for episode in range(Episodes):
        # if episode in np.arange(0,Episodes,Episodes/10):
        #     print('Running episode {}'.format(episode))
        terminated = False
        ImpSampRatio = 1
        while not terminated:
            action_choice = np.random.random()
            if action_choice < 0.5:
                e = np.random.random()
                if e< 0.1:
                    Returns[episode] = 1
                    terminated = True
                ImpSampRatio = ImpSampRatio *1/0.5
            else:
                Returns[episode] = 0
                terminated = True
                ImpSampRatio = 0

        ImpSampRatios[episode] = ImpSampRatio

    if policy == 'OIS':
        run_state_value = np.cumsum(Returns * ImpSampRatios) / np.arange(1,Episodes+1)
    else:
        with np.errstate(divide='ignore', invalid='ignore'):
            run_state_value = np.cumsum(Returns * ImpSampRatios)/ np.cumsum(ImpSampRatios)

        run_state_value[np.flatnonzero(np.isnan(run_state_value))] = 0

    return run_state_value

runs = 10
policy = 'WIS' # Choose OIS for ordinary importance sampling and WIS for Weighted Importance Sampling
for run in range(runs):
    print('Run number {}'.format(run))
    State_value = run_episodes(policy)
    plt.figure(1,figsize=(15,8))
    State_value_plot = plt.subplot()
    for i in [1.0,2.0]:
        State_value_plot.axhline(y = i, color = 'k', linewidth = 1.0, linestyle = 'dashed', alpha = 0.5)
    State_value_plot.semilogx(np.arange(1,Episodes+1),State_value)
    State_value_plot.set_ylim([0,3])
    State_value_plot.set_ylabel('State value')
    State_value_plot.set_xlabel('Episode number')

    plt.show()

plt.savefig('StateValue-Episodes_'+policy+'.png')

