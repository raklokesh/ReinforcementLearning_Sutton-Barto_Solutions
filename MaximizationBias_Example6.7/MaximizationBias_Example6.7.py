import numpy as np
import matplotlib.pyplot as plt

def choose_action(state):
    e = np.random.random()
    if e < EPSILON:
        action = np.random.choice(ACTIONS[state])
    else:
        action = np.random.choice(np.flatnonzero(Q_values[state] == np.max(Q_values[state])))

    return action

def determine_nextState(state,action,episode):
    reward = 0
    cur_state = 2
    if state == 0:
        if action == 0:
            cur_state = 1
            left_actions[episode]=1
    if state == 1:
        reward = np.random.normal(-0.1, 1)
    return cur_state,reward


def update_qValues(current_state,action,next_state,reward):
    max_Q = Q_values[next_state][np.random.choice(np.flatnonzero(Q_values[next_state] == np.max(Q_values[next_state])))]
    Q_values[current_state][action] += ALFA * (reward+ max_Q- Q_values[current_state][action])


def run_simulation():
    Avg_left_actions = np.zeros(EPISODES)
    for run in range(RUNS):
        if run in np.arange(0,RUNS,RUNS/10):
            print('Running {}'.format(run))
        global Q_values,left_actions
        Q_values = [[0, 0], [0 for i in range(B_ACTIONS)], [0]]
        left_actions = np.zeros(EPISODES)
        for episode in range(EPISODES):
            current_state = 0
            while True:
                action = choose_action(current_state)
                next_state,reward = determine_nextState(current_state,action,episode)
                update_qValues(current_state,action,next_state,reward)
                current_state = next_state
                if next_state==2:
                    break

        left_actions = np.divide(np.cumsum(left_actions),np.arange(1,EPISODES+1))
        Avg_left_actions+=left_actions

    return Avg_left_actions/RUNS*100


ALFA = 0.1
RUNS = 1000
EPISODES = 300
EPSILON = 0.1

B_ACTION_CHOICE = [1,2,5,10,100]
Percentage_left_actions = []
for B_ACTIONS in B_ACTION_CHOICE:
    ACTIONS = [[0, 1], [i for i in range(B_ACTIONS)]]
    Percentage_left_actions.append(run_simulation())


fig = plt.figure(figsize=(8,10))
Actions_Plot = plt.subplot()
for i,action_choice in enumerate(B_ACTION_CHOICE):
    Actions_Plot.plot(np.arange(1,EPISODES+1),Percentage_left_actions[i],label = '{}'.format(action_choice))
Actions_Plot.set_xticks([1,100,200,300])
Actions_Plot.set_yticks([0,5,25,50,75,100])
Actions_Plot.set_ylabel('% left actions from A')
Actions_Plot.set_xlabel('Episodes')
Actions_Plot.legend(title = 'Number of actions in B')