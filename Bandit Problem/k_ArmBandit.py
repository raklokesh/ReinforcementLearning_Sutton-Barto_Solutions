# Solution to 10-arm bandit problem using sample average method for determining value function
# Can solve using epsilon-greedy method or Upper Confidence Bound estimation
import numpy as np
import matplotlib.pyplot as plt

bandit_reward = [0.20, -0.8, 1.5, 0.4, 1.2,
                 -1.5, -0.1, -1, 0.8, -0.4]
epsilon = 0.5  # epsilon value for epsilon greedy method
c = 2  # degree of exploration for UCB method

def determine_reward(action):
    reward = np.random.normal(bandit_reward[action],StdDev) # reward for the action based on a normal distribution with bandit reward mean and stddev
    return reward


class agent:
    def __init__(self, epsilon):
        self.epsilon = epsilon
        self.action_chosen = np.zeros(len(bandit_reward))  # No of times the action was chosen
        self.action_value = np.zeros(len(bandit_reward))  # Value of each action at a given time instant

    def update_value(self, reward, action):
        self.action_chosen[action] += 1
        self.action_value[action] = (self.action_value[action] * (self.action_chosen[action] - 1) + reward) / \
                                    self.action_chosen[action]

    def choose_action(self, t):
        if method == 'epsilon':
            rand = np.random.random()
            if rand < epsilon:
                action = np.random.randint(len(bandit_reward))
                return action
            else:
                action = np.random.choice(np.flatnonzero(self.action_value == self.action_value.max()))
                return action
        else:
            self.UCB_action_value = self.action_value + c * np.sqrt(
                np.log(t + 2) / self.action_chosen)  # computing the upper confidence bound adjusted action value
            action = np.random.choice(np.flatnonzero(
                self.UCB_action_value == self.UCB_action_value.max()))  # choosing an action from actions having max of upper confidence bound adjusted action value
            return action

if __name__ == '__main__':

    StdDev=1.0
    NTrials=1000# no of trials in each experiment
    NExperiments=1000
    action_history = np.zeros(NTrials)
    reward_history = np.zeros(NTrials)
    reward_accumulation=np.zeros(NTrials)
    action_proportion_history_all=np.zeros((NTrials,len(bandit_reward)))
    reward_history_all=np.zeros(NTrials)
    reward_accumulation_all=np.zeros(NTrials)
    method = 'epsilon' # select epsilon or UCB method for choosing action

    for experiment in range(NExperiments):
        print("Running experiment number {}".format(experiment))
        action_proportion_history = []
        reward_history = np.zeros(NTrials)
        Player = agent(epsilon)
        for trial in range(NTrials):
            action=Player.choose_action(trial)
            reward=determine_reward(action)
            action_history[trial]=action
            reward_history[trial]=reward
            reward_accumulation[trial] = np.sum(reward_history)
            Player.update_value(reward,action)
            action_proportion_history.append(Player.action_chosen/(trial+1))

            #print("the action taken is {} and the reward is {}".format(action,reward))

        reward_accumulation_all+=reward_accumulation
        reward_history_all+=reward_history
        action_proportion_history_all+=action_proportion_history

    action_prop_hist_avg = action_proportion_history_all / NExperiments
    reward_hist_avg = reward_history_all/NExperiments
    reward_accumulation_avg=reward_accumulation_all/NExperiments

    for i in range(len(bandit_reward)):
        plt1 =plt.subplot(311)
        plt1.plot(action_prop_hist_avg[:,i],label='Bandit %s' % (i+1))

    plt2 = plt.subplot(312)
    plt2.plot(reward_hist_avg, label='Average reward')

    plt3 = plt.subplot(313)
    plt3.plot(reward_accumulation_avg, label='Accum reward')

    plt1.set_ylim([0,1])
    plt1.set_xlabel("Trials")
    plt1.set_ylabel("Average proportion of picked actions")
    plt1.legend()
    plt2.set_ylim([0, 2])
    plt2.set_xlabel("Trials")
    plt2.set_ylabel("Average reward")
    plt3.set_ylim([0, 1500])
    plt3.set_xlabel("Trials")
    plt3.set_ylabel("Accumulated reward")

    fig=plt.gcf()
    fig.set_size_inches(15,10)
    plt.show()

    if method == 'epsilon':
        plt.savefig("Action_Proportion_epsilon={}".format(epsilon)+".png", bbox_inches="tight")
    else:
        plt.savefig("Action_Proportion_UCB_c={}".format(c) + ".png", bbox_inches="tight")
