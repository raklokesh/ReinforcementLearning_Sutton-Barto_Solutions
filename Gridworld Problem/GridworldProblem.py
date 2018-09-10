# Using value iteration to solve the gridworld problem given in Sutton's RL book.
# Testing the effects of choosing random policy or optimal policy
import numpy as np
import matplotlib.pyplot as plt
import copy as copy

WorldSize=5

class GridWorld:
    def __init__(self):
        self.Updated_Grid = np.zeros((WorldSize, WorldSize))
        self.Initial_Grid = np.zeros((WorldSize, WorldSize))
        self.Final_Grid=[]

    def determine_new_state(self,i,j,action):
        if action=='N':
            if i==0:
                NewState=[i,j]
                reward=-1
            else:
                NewState=[i-1,j]
                reward=0
        elif action=='S':
            if i==WorldSize-1:
                NewState=[i,j]
                reward=-1
            else:
                NewState=[i+1,j]
                reward=0
        elif action=='W':
            if j==0:
                NewState=[i,j]
                reward=-1
            else:
                NewState=[i,j-1]
                reward=0
        elif action=='E':
            if j==WorldSize-1:
                NewState=[i,j]
                reward=-1
            else:
                NewState=[i,j+1]
                reward=0
        if i==0 and j==1:# irrespective of the action, new state and reward are always the same for this state
            NewState=[4,1]
            reward=10
        if i==0 and j==3:# irrespective of the action, new state and reward are always the same for this state
            NewState=[2,3]
            reward=5

        return (NewState,reward)




if __name__ == '__main__':

    actions = ['N', 'S', 'E', 'W']
    action_prob = {'N': 0.25, 'S': 0.25, 'E': 0.25, 'W': 0.25}
    action_value = {'N': 0, 'S': 0, 'E': 0, 'W': 0}
    discount = 0.9
    random = False # Random or optimal policy
    converged = False

    Grid=GridWorld()

    UpdateNo=0
    while converged==False:
        print("Update number {}".format(UpdateNo))
        UpdateNo+=1
        Grid.Updated_Grid=np.zeros((WorldSize, WorldSize))
        for i in range(WorldSize):
            for j in range(WorldSize):
                action_value=[]
                for action in actions:
                    [NewState,reward]=Grid.determine_new_state(i,j,action)
                    if random==True:
                        Grid.Updated_Grid[i, j]+= action_prob[action] * (reward + discount * Grid.Initial_Grid[NewState[0], NewState[1]])
                    else:
                        action_value.append(reward + discount * Grid.Initial_Grid[NewState[0], NewState[1]])
                if random==False:
                    Grid.Updated_Grid[i,j]=action_value[np.random.choice(np.flatnonzero(action_value==np.max(action_value)))]

        if np.sum(np.abs(Grid.Updated_Grid - Grid.Initial_Grid))<0.0001:
            converged=True
            Grid.Final_Grid= copy.copy(Grid.Updated_Grid)
        else:
            Grid.Initial_Grid= copy.copy(Grid.Updated_Grid)

    # Can verify results using bellman's equations. Below are the equations for some of the cells in the first row:
    # Cell 1 : 0.55*V11=0.225*V12+0.225*V21-0.5
    # Cell 2 : 4*V12=3.6*V52+40
    # Cell 3 : 3.1*V13=0.9*V12+0.9*V14+0.9*V23-1
    # In fact the state values can be obtained by solving the set of linear equations,
    # obtained by writing bellman equation for all cells as shown above


    plt.figure()
    Grid_plot=plt.subplot()
    for i in range(WorldSize):
        for j in range(WorldSize):
            value=str(np.round(Grid.Final_Grid[i,j],1))
            Grid_plot.text(j+0.5,5-i-0.5,value,ha='center',va='center')

    Grid_plot.grid(color='k')
    Grid_plot.axis('scaled')
    Grid_plot.axis([0, 5, 0, 5])
    Grid_plot.set_yticklabels([])
    Grid_plot.set_xticklabels([])

    fig1=plt.gcf()
    fig1.set_size_inches(10,7)

    plt.savefig("GridWorld_StateValues_Optimal.png")
