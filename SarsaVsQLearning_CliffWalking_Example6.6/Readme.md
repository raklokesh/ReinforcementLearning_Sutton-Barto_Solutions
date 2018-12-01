**Comparing Q-Learning and Sarsa on the cliff walking example: Example 6.6**

** Important**
1. On some of the episodes the Sarsa algorithm led to end of episode Q-value extimates that caused back and forth oscillation between two states.
   Thus, when running the full greedy optimal algorithm I set the upper limit for the time steps in the episode as 20. 
2. I couldnt obtain the sum of rewards per episode plot as shown in the book using a single episode. 
   I tried averaging the sum of rewards across 1000 runs to obtain a plot similar the lines were not as smooth and I am not sure if a smoothing was required to generate those plots.
    
