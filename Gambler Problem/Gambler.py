import numpy as np
import copy
import matplotlib.pyplot as plt

Gambler_goal_money = 100
States= np.arange(1,Gambler_goal_money)
Ph=0.4 #(probability of a head)
Sweep_number = 0
delta = 1

class Gambler:
    def __init__(self):
        self.Initial_State_value = np.zeros(Gambler_goal_money+1)
        self.Updated_State_value = np.zeros(Gambler_goal_money+1)
        self.State_value_memory=np.zeros(Gambler_goal_money+1)
        self.optimal_action=np.zeros(Gambler_goal_money)

def Determine_Action_value (State,Action,State_values):
    if State+Action==100:
        reward=1
    else:
        reward=0

    action_value= Ph*(reward+State_values[State+Action])+(1-Ph)*(State_values[State-Action])
    return action_value


Gambler = Gambler()
while delta > 0.1:
    for i in States:
        Actions = np.arange(1,np.min([i, Gambler_goal_money - i]) + 1)
        action_value=[]
        for j in Actions:
            print("{} and {}".format(i,j))
            action_value.append(Determine_Action_value(i, j, Gambler.Updated_State_value))
        optimal_state_value=action_value[np.random.choice(np.flatnonzero(action_value==np.max(action_value)))]
        Gambler.Updated_State_value[i]=optimal_state_value
        Gambler.optimal_action[i]=Actions[np.random.choice(np.flatnonzero(action_value==np.max(action_value)))]
    delta=np.sum(np.abs(Gambler.Initial_State_value-Gambler.Updated_State_value))
    Gambler.Initial_State_value = copy.copy(Gambler.Updated_State_value)
    Gambler.State_value_memory=np.vstack((Gambler.State_value_memory,Gambler.Updated_State_value))
    Sweep_number += 1

# plotting the update of the value fucntions with sweeps
for i in range(1,Sweep_number):
    Value_plot=plt.subplot()
    Value_plot.plot(Gambler.State_value_memory[i,1:99],label='Sweep number %s' % (i))

plt.figure(1)
Value_plot.set_yticks(np.arange(0,1.1,0.2))
Value_plot.set_xlabel("States")
Value_plot.set_ylabel("State Values")
Value_plot.set_xticks([1,25,50,75,99])
Value_plot.legend()

fig=plt.gcf()
fig.set_size_inches(10,7)
plt.show()

plt.savefig("State_value_updates"+ ".png", bbox_inches="tight")

# plotting optimal policy
plt.figure(2)
Optimal_action_plot=plt.subplot()
Optimal_action_plot.plot(Gambler.optimal_action)
Optimal_action_plot.set_xlabel("States")
Optimal_action_plot.set_ylabel("Optimal Action")
Optimal_action_plot.set_xticks([1, 25, 50, 75, 99])

fig1=plt.gcf()
fig1.set_size_inches(10,7)
plt.show()
plt.savefig("Optimal Stakes" + ".png", bbox_inches="tight")
