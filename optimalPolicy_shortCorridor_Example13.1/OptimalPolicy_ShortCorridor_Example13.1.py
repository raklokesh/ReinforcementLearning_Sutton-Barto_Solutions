import numpy as np
import matplotlib.pyplot as plt
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
    state_value.append(epsilon * stateAction_value[0, 1] + (1 - epsilon) * stateAction_value[0, 0])

stateValue_plot = plt.subplot()
stateValue_plot.plot(EPSILON_RANGE,state_value,'k')
stateValue_plot.set_xlabel('Probability of right action')
stateValue_plot.set_ylabel('Value of starting state')
stateValue_plot.set_xticks(np.arange(0,1.1,0.1))
stateValue_plot.set_ylim((-100,-10))