** nStep TD method with different n and alfa values for random walk: Example 7.1**
_Implementation_

Ran the n-step TD algorithm for several n-step values and alfa values. Plotted the RMSE averages across first 10 episodes and 100 such runs.

_Results_

Plotted the RMSE values for each n-step value versus alfa.

(i)  n-step methods that lie inbetween MC and TD(0) methods can perform better than either of them. 

(ii) Note that the n-value depends on the number of states in the random walk. A smaller number of states would probably lead to a lower          optimal n and vice versa for larger number of states.
    Aptly intermediate n-step value of 4 is most suited for this random walk involving 19 states at an alfa value ~ 0.4.
