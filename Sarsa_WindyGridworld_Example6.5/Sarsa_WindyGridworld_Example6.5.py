import numpy as np
import matplotlib.pyplot as plt

def determine_action(state,policy):
    if policy == 'e':
        e = np.random.random()
    else:
        e = 0.5

    if e <0.1:
        action = np.random.choice(actions)
    else:
        choices = state_action_values[state[0],state[1],:]
        action = np.random.choice(np.flatnonzero(choices == np.max(choices)))
    return action

def determine_state(state,action):
    new_state = state + np.array(action_movement[action]) + np.array([0,perturbation[state[0]]])
    if new_state[0]>9:
        new_state[0] = 9
    elif new_state[0]<0:
        new_state[0] = 0
    elif new_state[1]>6:
        new_state[1] = 6
    elif new_state[1]<0:
        new_state[1]=0

    return new_state

def update_QValues(state1,state2,action1):
    action2 = determine_action(state2,'e')

    state_action_values[state1[0],state1[1],action1] = state_action_values[state1[0],state1[1],action1] + alfa*(-1 + state_action_values[state2[0],state2[1],action2] -
                                                                                                                state_action_values[state1[0],state1[1],action1])
    return action2

alfa = 0.5
actions = [0,1,2,3]
action_movement = [[0,1],[1,0],[0,-1],[-1,0]]
state_action_values = np.zeros((10,7,4))
perturbation = [0,0,0,1,1,1,2,2,1,0]

current_state = np.array([0,3])
action = determine_action(current_state,'e')
steps = 8000
episode = 0
episode_step = np.zeros(steps)
steps_episode = 0
episode_steps = []
for time_step in range(steps):
    old_state = current_state
    current_state= determine_state(old_state,action)
    action = update_QValues(old_state,current_state,action)
    episode_step[time_step] = episode
    time_step+=1
    steps_episode+=1
    if (current_state == [7,3]).all():
        current_state = np.array([0, 3])
        episode_steps.append(steps_episode)
        steps_episode = 0
        episode+=1

# Running the optimal policy on the gridworld
current_state = np.array([0,3])
x_pos = []
y_pos = []
while not (current_state == np.array([7,3])).all():
    x_pos.append(current_state[0])
    y_pos.append(current_state[1])
    action = determine_action(current_state, 'o')
    current_state = determine_state(current_state,action)
x_pos.append(current_state[0])
y_pos.append(current_state[1])

plt.figure(1,figsize= (8,6))
Episode_step_plot = plt.subplot()
Episode_step_plot.plot(np.arange(steps),episode_step,color = 'xkcd:red')
Episode_step_plot.set_ylabel('Episodes')
Episode_step_plot.set_xlabel('Time steps')
Episode_step_plot.set_xticks(np.arange(0,steps+1,1000))
Episode_step_plot.set_yticks(np.array([0,50,100,150,170]))

plt.savefig('EpisodesVStimestepsPlot.png')

plt.figure(2,figsize= (8,6))
Steps_episode_plot = plt.subplot()
Steps_episode_plot.plot(np.arange(len(episode_steps)),episode_steps,color = 'xkcd:blue')
Steps_episode_plot.set_ylabel('Time steps in episode')
Steps_episode_plot.set_xlabel('Episode number')
Steps_episode_plot.set_xticks(np.arange(0,len(episode_steps)+1,10))
Steps_episode_plot.set_yticks(np.arange(0,np.max(episode_steps)+1,200))

plt.savefig('StepsInEpisodePlot.png')

plt.figure(3,figsize= (10,6))
Grid_Optimal_Trajectory = plt.subplot()
Grid_Optimal_Trajectory.plot(x_pos,y_pos,color = 'xkcd:blue')
Grid_Optimal_Trajectory.grid(color='k')
Grid_Optimal_Trajectory.axis('scaled')
Grid_Optimal_Trajectory.set_xticks(np.arange(-0.5,10,1))
Grid_Optimal_Trajectory.set_yticks(np.arange(-0.5,7,1))
Grid_Optimal_Trajectory.set_xticklabels([])
Grid_Optimal_Trajectory.set_yticklabels([])

plt.savefig('OptimalTrajectory.png')