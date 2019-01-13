import numpy as np
import matplotlib.pyplot as plt

def determine_state(state):
    reward = 0
    terminated = False
    e = np.random.random()
    if e > 0.5:
        next_state = np.random.choice(np.arange(state+1,state+101,1))
    else:
        next_state = np.random.choice(np.arange(state-1,state-101,-1))

    if next_state > 1000:
        next_state = 1001
        reward = 1
        terminated = True
    elif next_state < 1:
        next_state = 0
        reward = -1
        terminated = True

    return next_state,reward,terminated

ALFA = 2*10**-5

StateVisits = np.zeros(1002)
Weights = np.zeros(10)
EPISODES = 100000
for episode in range(EPISODES):
    if episode in np.arange(0,EPISODES,EPISODES/10):
        print('Running episode {}'.format(episode))
    current_state = 500
    terminated = False
    states= []

    while not terminated:
        StateVisits[current_state]+=1
        states.append(current_state)
        current_state,reward,terminated = determine_state(current_state)

    for step in np.arange(1,len(states)):
        G = reward
        index = (states[-step]-1)//100

        Weights[index]+=ALFA*(G - Weights[index])

State_Distribution = StateVisits/np.sum(StateVisits)

State_values = [Weights[j] for j in range(len(Weights)) for k in range(100)]

plt.figure(figsize= (8,12))
Statevalue_Plot = plt.subplot(211)
Statevalue_Plot.plot(np.arange(1,1001), State_values)
Statevalue_Plot.set_ylim([-1,1])
Statevalue_Plot.set_yticks([-1,0,1])
Statevalue_Plot.set_ylabel('State Values')

StateDist_Plot = plt.subplot(212)
StateDist_Plot.plot(np.arange(1,1001),State_Distribution[1:1001])
StateDist_Plot.set_yticks([0,0.0017,0.0137])
StateDist_Plot.set_xlabel('State')
StateDist_Plot.set_ylabel('Distribution of states')



