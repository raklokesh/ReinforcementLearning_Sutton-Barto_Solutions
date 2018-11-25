**Comparing Temporal Difference method to Monte Carlo with batch updating: Example 6.4 (You are the predictor)**

1. The TD method converges to the better estimate for state values VA = VB = 0.75. 
2. MC method yields a state value of 0 for VA which might be a good estimate for current data but will most likely yield higher errors for future data. Especially when the the following episode occurs **A 0 B 1**
