**Using SARSA TD algorithm to find optimal trajectory for the Windy Gridworld : Example 6.5**

The state of the agent is specified in the x,y coordinate frame positioned at the lower left corner of the grid. 
Thus the agent starts in the state [0,3] and the goal state is [7,3]. 

**Important**
1. Note that we need to constrain movement of the agent inside the grid.This is not explicitly stated in the Example.
2. Thus, for any action that leads to agent moving outside the grid in the x or y directions leaves the coordinate 
   in that particular direction unchanged.
   
**Plots**
1. The first plot is the one shown in the book as well where we are plotting episode number vs the cumulated time step across episodes
2. Another way to visualize the result is to plot time-steps taken in each episode. This is the second plot and we note that the 
   number of steps per episode converges to an average value of around 17.
3. The third plot i.e. grid plot is obtained by running the optimal learnt policy and plotting the state-transitions on the grid.


