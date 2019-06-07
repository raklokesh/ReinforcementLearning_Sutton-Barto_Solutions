import numpy as np
import matplotlib.pyplot as plt

class simulation:
    def __init__(self,action_num,method):
        self.action_num = action_num
        self._method = method
        self.ACTIONS = [[0,1],[i for i in range(action_num)]]
        if self._method == 'Q':
            self.Q_values = [[0.0, 0.0], [0.0 for i in range(action_num)]]
        else:
            self.Q1_values = [[0.0,0.0],[0.0 for i in range(action_num)]]
            self.Q2_values = [[0.0, 0.0], [0.0 for i in range(action_num)]]

    def choose_action(self,state):
        e = np.random.random()
        if e < EPSILON:
            action = np.random.choice(self.ACTIONS[state])
        else:
            if self._method == 'Q':
                action = np.random.choice(np.flatnonzero(self.Q_values[state] == np.max(self.Q_values[state])))
            else:
                action_values = np.array(self.Q1_values[state])+np.array(self.Q2_values[state])
                action = np.random.choice(np.flatnonzero(action_values == np.max(action_values)))

        return action

    def determine_transition(self,cur_state,action):
        next_state = None
        ended = True
        if cur_state == 0:
            reward = 0
            if action == 0:
                next_state = 1
                ended = False
        if cur_state == 1:
            reward = np.random.normal(-0.1, 1)
        return next_state,reward,ended

    def update_QValues(self,curr_state,action,reward,next_state):
        if self._method == 'Q':
            if next_state == None:
                self.Q_values[curr_state][action] += ALFA * (reward - self.Q_values[curr_state][action])
            else:
                max_nextQValue = np.max(self.Q_values[next_state])
                self.Q_values[curr_state][action] += ALFA * (
                            reward + GAMMA * max_nextQValue - self.Q_values[curr_state][action])
        else:
            e = np.random.random()
            if e<0.5:
                if next_state == None:
                    self.Q1_values[curr_state][action]+=ALFA*(reward-self.Q1_values[curr_state][action])
                else:
                    max_nextQValue = self.Q2_values[next_state][np.argmax(self.Q1_values[next_state])]
                    self.Q1_values[curr_state][action] += ALFA * (reward + GAMMA*max_nextQValue- self.Q1_values[curr_state][action])
            else:
                if next_state == None:
                    self.Q2_values[curr_state][action]+=ALFA*(reward-self.Q2_values[curr_state][action])
                else:
                    max_nextQValue = self.Q1_values[next_state][np.argmax(self.Q2_values[next_state])]
                    self.Q2_values[curr_state][action] += ALFA * (reward + GAMMA*max_nextQValue- self.Q2_values[curr_state][action])

    def run_simulation(self):
        episode_direction = []
        for episode in range(EPISODES):
            curr_state = 0
            while True:
                action = self.choose_action(curr_state)
                next_state, reward, episode_ended= self.determine_transition(curr_state, action)
                self.update_QValues(curr_state,action,reward,next_state)

                if episode_ended:
                    episode_direction.append(1 if curr_state == 1 else 0)
                    break

                curr_state = next_state
        return 100*np.divide(np.cumsum(episode_direction),np.arange(1,EPISODES+1))


EPSILON = 0.1
B_ACTION_CHOICE = [1,2,5,10,100]
ALFA = 0.1
GAMMA = 1
EPISODES = 300
RUNS = 10000
Percentage_left_actions = np.zeros((len(B_ACTION_CHOICE),EPISODES))
method = 'DQ' # Use Q if using just Q and use 'DQ' if using Double-Q
for run in range(RUNS):
    if run in np.arange(0,RUNS,RUNS/10):
        print('Run number = {}'.format(run))
    for i,action_num in enumerate(B_ACTION_CHOICE):
        Sim = simulation(action_num,method)
        Percentage_left_actions[i,:]+=Sim.run_simulation()

Percentage_left_actions/=RUNS

fig = plt.figure(figsize=(8,10))
Actions_Plot = plt.subplot()
for i,action_choice in enumerate(B_ACTION_CHOICE):
    Actions_Plot.plot(np.arange(1,EPISODES+1),Percentage_left_actions[i],label = '{}'.format(action_choice))
Actions_Plot.set_xticks([1,100,200,300])
Actions_Plot.set_yticks([0,5,25,50,75,100])
Actions_Plot.set_ylabel('% left actions from A')
Actions_Plot.set_xlabel('Episodes')
Actions_Plot.legend(title = 'Number of actions in B')