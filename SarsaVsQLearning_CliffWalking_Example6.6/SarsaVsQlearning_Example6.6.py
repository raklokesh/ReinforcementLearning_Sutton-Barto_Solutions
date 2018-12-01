import numpy as np
import matplotlib.pyplot as plt

def run_episodes(algo):
    def determine_action(state, policy):
        if policy == 'e':
            e = np.random.random()
        else:
            e = 0.5

        if e < 0.1:
            action = np.random.choice(actions)
        else:
            choices = state_action_values[state[0], state[1], :]
            action = np.random.choice(np.flatnonzero(choices == np.max(choices)))
        return action

    def determine_state(state, action):
        new_state = state + np.array(action_movement[action])
        terminated = False
        reward = -1
        if new_state[1] == 0 and new_state[0] in np.arange(1, 11):
            reward = -100
            new_state = np.array([0,0])
        elif (new_state == np.array([11, 0])).all():
            terminated = True
        else:
            if new_state[0] > 11:
                new_state[0] = 11
            elif new_state[0] < 0:
                new_state[0] = 0
            elif new_state[1] > 3:
                new_state[1] = 3
            elif new_state[1] < 0:
                new_state[1] = 0
        return new_state, reward, terminated

    def update_QValues(state1, state2, action1, reward):
        if algo == 'Q':
            action2 = determine_action(state2, 'o')
        else:
            action2 = determine_action(state2, 'e')


        state_action_values[state1[0], state1[1], action1] = state_action_values[
                                                                 state1[0], state1[1], action1] + alfa * (
                                                                         reward + state_action_values[
                                                                     state2[0], state2[1], action2] -
                                                                         state_action_values[
                                                                             state1[0], state1[1], action1])

        return action2

    actions = [0, 1, 2, 3]
    action_movement = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    episode_reward = np.zeros(Episodes)
    state_action_values = np.zeros((12, 4, 4))
    for episode in range(Episodes):
        terminated = False
        current_state = np.array([0,0])
        if not algo=='Q':
            action = determine_action(current_state,'e')
        #time_step = 0
        while not terminated:
            old_state = current_state
            if algo == 'Q':
                action = determine_action(current_state, 'e')
            current_state,reward,terminated = determine_state(old_state, action)
            if algo == 'Q':
                _ = update_QValues(old_state, current_state,action,reward)
            else:
                action= update_QValues(old_state, current_state, action, reward)
            episode_reward[episode]+=reward

            #time_step+=1
            #if time_step>70:
                #terminated = True


    # Running the optimal policy on the gridworld
    current_state = np.array([0,0])
    x_pos = []
    y_pos = []
    terminated = False
    optimal_reward = 0
    time_step = 0
    while not terminated:
        x_pos.append(current_state[0])
        y_pos.append(current_state[1])
        action = determine_action(current_state, 'o')
        current_state,reward,terminated= determine_state(current_state,action)
        optimal_reward +=reward
        time_step+=1
        if time_step>20:
            terminated = True
    x_pos.append(current_state[0])
    y_pos.append(current_state[1])


    return episode_reward,np.array([x_pos,y_pos])

alfa = 0.5
Episodes = 500
runs = 1
QLearning_reward_avg=np.zeros(Episodes)
Sarsa_reward_avg=np.zeros(Episodes)
for run in range(runs):
    if run in np.arange(0, runs, runs / 10):
        print('running {}'.format(run))
    Sarsa_reward,Sarsa_optimal_path = run_episodes('S')
    QLearning_reward,QLearning_optimal_path = run_episodes('Q')
    Sarsa_reward_avg+=Sarsa_reward
    QLearning_reward_avg+=QLearning_reward

QLearning_reward_avg/=runs
Sarsa_reward_avg/=runs


plt.figure(1,figsize= (8,6))
Reward_sum_plot = plt.subplot()
Reward_sum_plot.plot(np.arange(Episodes), QLearning_reward_avg, color ='xkcd:red', label = 'Q Learning')
Reward_sum_plot.plot(np.arange(Episodes), Sarsa_reward_avg, color ='xkcd:blue', label = 'Sarsa')
Reward_sum_plot.set_ylabel('Sum of rewards')
Reward_sum_plot.set_xlabel('Episode')
Reward_sum_plot.set_xticks(np.arange(0,501,100))
Reward_sum_plot.set_ylim((-100,-20))
Reward_sum_plot.legend()

plt.figure(3,figsize= (10,6))
Grid_Optimal_Trajectory = plt.subplot()
Grid_Optimal_Trajectory.grid(color='k')
Grid_Optimal_Trajectory.axis('scaled')
Grid_Optimal_Trajectory.plot(QLearning_optimal_path[0,:],QLearning_optimal_path[1,:],color = 'xkcd:red',label = 'Q Learning')
Grid_Optimal_Trajectory.plot(Sarsa_optimal_path[0,:]-0.05,Sarsa_optimal_path[1,:],color = 'xkcd:blue',label = 'Sarsa')
Grid_Optimal_Trajectory.set_xticks(np.arange(-0.5,12,1))
Grid_Optimal_Trajectory.set_yticks(np.arange(-0.5,4,1))
Grid_Optimal_Trajectory.set_xticklabels([])
Grid_Optimal_Trajectory.set_yticklabels([])
Grid_Optimal_Trajectory.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05))
