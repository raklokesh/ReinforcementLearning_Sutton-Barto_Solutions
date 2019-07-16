import numpy as np
import matplotlib.pyplot as plt

# Two methods have been shown: 1 - Q-learning of state action values 2 - Simultaneous solution to bellmans equations

# METHOD 1
def choose_action():
    e = np.random.random()
    if e<epsilon:
        action = 1
    else:
        action = 0

    return action

state_value = []
ACTIONS = np.array([0, 1])
ACTION_EFFECTS = np.array([[0, 1], [1, -1], [-1, 1]])
EPISODES = 10000
EPSILON_RANGE = np.arange(0.02,1,0.02)
for epsilon in EPSILON_RANGE:
    print('epsilon = {}'.format(epsilon))
    stateAction_value = np.zeros((4,2))

    for episode in range(EPISODES):
        next_state = 0
        current_state = next_state
        next_action = np.random.choice(ACTIONS)
        current_action = next_action
        while True:
            next_state = current_state+ACTION_EFFECTS[current_state, current_action]
            if next_state==3:
                stateAction_value[current_state, current_action] += 0.01*(
                            -1 - stateAction_value[current_state, current_action])
                break

            next_action = choose_action()
            stateAction_value[current_state, current_action] += 0.01*(
                        -1 + stateAction_value[next_state, next_action] - stateAction_value[current_state, current_action])
            current_state = next_state
            current_action = next_action
    state_value.append(epsilon * stateAction_value[0, 1] + (1 - epsilon) * stateAction_value[0, 0]) # Compute state value using state-action values

stateValue_plot = plt.subplot()
stateValue_plot.plot(EPSILON_RANGE,state_value,'k')
stateValue_plot.set_xlabel('Probability of right action')
stateValue_plot.set_ylabel('Value of starting state')
stateValue_plot.set_xticks(np.arange(0,1.1,0.1))
stateValue_plot.set_ylim((-100,-10))

# METHOD 2

# State values be solved by simulataneously solving bellman equations for state values
# If p is the probability of taking right action then the bellman equations are:
# V0 = p*(-1 + V1) + (1-p)*(-1+V0) ==> p*V0+1-p*V1 = 0
# V1 = p*(-1+V0) + (1-p)*(-1+V2) ==> V1-p*V0-(1-p)*V2+1 = 0
# V2 = p*(-1 + 0) + (1-p)*(-1+V1) ==> V2 -(1-p)*V1 + 1 = 0
bellman = False
if bellman:
    state_value = []
    EPSILON_RANGE = np.arange(0.02,1,0.02)
    for epsilon in EPSILON_RANGE:
        p = epsilon
        A = np.array([[p,-p,0],[-p,1,p-1],[0,p-1,1]])
        C = np.array([-1,-1,-1]).transpose() 
        V = np.dot(np.linalg.inv(A),C)
        state_value.append(V[0])
    stateValue_plot = plt.subplot()
    stateValue_plot.plot(EPSILON_RANGE,state_value,'k')
    stateValue_plot.set_xlabel('Probability of right action')
    stateValue_plot.set_ylabel('Value of starting state')
    stateValue_plot.set_xticks(np.arange(0,1.1,0.1))
    stateValue_plot.set_ylim((-100,-10))
        
        

