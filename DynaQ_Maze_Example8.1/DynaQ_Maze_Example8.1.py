import numpy as np
import matplotlib.pyplot as plt

def choose_action(state):
    choice_values = Q_values[state[0],state[1],:]
    e = np.random.random()
    if e<EPSILON:
        action = np.random.choice(ACTIONS)
    else:
        action = np.random.choice(np.flatnonzero(choice_values == np.max(choice_values)))

    return action

def determine_transitions(state,action):
    terminated = False
    reward = 0
    new_state = state + np.array(ACTION_MOVE[action])
    if new_state[0] == 5 and new_state[1] == 8:
        reward = 1
        terminated = True
    elif new_state[0]==-1 or new_state[0]==6:
        new_state = state
    elif new_state[1] == -1 or new_state[1] == 9:
        new_state = state

    for I in OBSTACLES:
        if new_state[0] == I[0] and new_state[1] == I[1]:
            new_state = state

    return new_state,reward,terminated

def update_model_list(state_list,state,action):
    if len(state_list)==0:
        state_list.append([state,[action]])
    else:
        state_exists = False
        for index,I in enumerate(state_list):
            if I[0][0] == state[0] and I[0][1] == state[1]:
                state_exists = True
                if action not in I[1]:
                    state_list[index][1].append(action)
        if not state_exists:
            state_list.append([state, [action]])

    return state_list

def update_Qvalues(state1,action,reward,state2):
    choice_values = Q_values[state2[0], state2[1], :]
    max_action = np.random.choice(np.flatnonzero(choice_values == np.max(choice_values)))
    Q_values[state1[0],state1[1],action]+=ALFA*(reward+GAMMA*Q_values[state2[0],state2[1],max_action] - Q_values[state1[0],state1[1],action])


def run_experiments():
    experiment_steps = np.zeros(EPISODES)

    for experiment in range(EXPERIMENTS):
        if experiment in np.arange(0,EXPERIMENTS,EXPERIMENTS/6):
            print('Running experiment {}'.format(experiment))
        steps_episode = np.zeros(EPISODES)
        global Q_values
        Q_values = np.zeros((6,9,4))
        visited_states_list = []
        for episode in range(EPISODES):
            current_state = np.array([3,0])
            terminated = False
            step = 0
            while not terminated:
                action = choose_action(current_state)

                new_state,reward,terminated = determine_transitions(current_state,action)


                visited_states_list = update_model_list(visited_states_list,current_state,action)

                update_Qvalues(current_state,action,reward,new_state)

                current_state = new_state

                for i in range(PLANNING_STEPS):
                    random_choice = np.random.choice(np.arange(len(visited_states_list)))
                    random_state = visited_states_list[random_choice][0]
                    random_action = np.random.choice(visited_states_list[random_choice][1])
                    _new_state,_reward,_ = determine_transitions(random_state,random_action)
                    update_Qvalues(random_state,random_action,_reward,_new_state)

                step+=1


            steps_episode[episode] = step

        experiment_steps+=steps_episode

    experiment_steps/=EXPERIMENTS
    return experiment_steps

EPSILON = 0.1
ALFA = 0.1
GAMMA = 0.95
ACTIONS = np.array([0,1,2,3])
PLANNING_STEPS_CHOICE = [0,5,50]
ACTION_MOVE = [[0, 1], [-1, 0], [0, -1], [1, 0]]

OBSTACLES = [[2,2],[3,2],[4,2],[1,5],[3,7],[4,7],[5,7]]

EXPERIMENTS = 30
EPISODES = 50

experiment_results = np.zeros((3,EPISODES))

for i,PLANNING_STEPS in enumerate(PLANNING_STEPS_CHOICE):
    print('Runnin planning steps = {}'.format(PLANNING_STEPS))
    experiment_results[i,:] = run_experiments()

plt.figure(figsize=(10,8))
Steps_episode_Plot = plt.subplot()
for i,n in enumerate(PLANNING_STEPS_CHOICE):
    Steps_episode_Plot.plot(np.arange(EPISODES),experiment_results[i,:],label = '{}'.format(n))
Steps_episode_Plot.set_xlabel('Episodes')
Steps_episode_Plot.set_ylabel('Steps per episode')
Steps_episode_Plot.set_ylim((0,800))
Steps_episode_Plot.set_yticks([14,200,400,600,800])
Steps_episode_Plot.set_xticks([2,10,20,30,40,50])
Steps_episode_Plot.legend(title = 'Planning steps (n)')
