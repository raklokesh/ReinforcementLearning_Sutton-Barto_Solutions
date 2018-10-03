# Finding expected return from each state of a blackjack game using monte carlo simulations.
# Used first MC method to find the average expected returns. Refer to algorithm box in section 5.1 RL Book.

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle

class player():
    def __init__(self):
        self.cards = pick_cards(2)
        self.stick_threshold = 20
        self.usable_ace = 0

class dealer():
    def __init__(self):
        self.cards = pick_cards(2)
        self.stick_threshold = 17
        self.usable_ace = 0

def decide(cards,threshold):
    usable_ace=0
    if 1 in cards:
        other_sum=np.sum(np.delete(cards,np.random.choice(np.flatnonzero(cards == 1))))
        include_sum_11=11+other_sum
        if include_sum_11 > 21:
            decision_sum=np.sum(cards)
        else:
            decision_sum=include_sum_11
            usable_ace=1

        return decision_sum, choose_action(decision_sum,threshold), usable_ace
    else:
        decision_sum=np.sum(cards)
        return decision_sum, choose_action(decision_sum,threshold), usable_ace

def choose_action(decision_sum,threshold):
    if decision_sum < threshold:
        action = 'hit'
    elif decision_sum in np.arange(threshold, 22):
        action = 'stick'
    else:
        action = 'bust'

    return action


def pick_cards(n):
    return np.random.choice(deck,n)

def decide_winner(player_sum,dealer_sum, action_player,action_dealer):
    if action_dealer == 'stick' and action_player == 'stick':
        if player_sum>dealer_sum:
            game_results.append(1)
        elif dealer_sum>player_sum:
            game_results.append(-1)
        else:
            game_results.append(0)
    elif action_player == 'stick' and action_dealer == 'bust':
        game_results.append(1)
    else:
        game_results.append(-1)

deck=np.arange(1,10)
deck=np.append(deck,[10,10,10,10])
deck=np.repeat(deck,4)
state_values=np.zeros((2,10,21))

Returns=[[[[] for i in range(21)] for i in range(10)] for i in range(2)] # storing returns depending on  usability of ace, dealers first card and player cardsum. [2 X 10 X 21 dimension list]

game_results=[]
Games=500000

player=player()
dealer=dealer()

# Generating the episode portion of the algorithm
for Game_No in range(Games):
    if Game_No in np.arange(0,Games,Games/10):
        print("Finished {} games".format(Game_No))

    rewards=[]
    states=[]

    player.__init__()
    dealer.__init__()
    usable_ace_player = 0
    usable_ace_dealer = 0

    player_sum_choice, action_player, usable_ace_player = decide(player.cards, player.stick_threshold)
    rewards.append(0)
    states.append(player_sum_choice)

    while action_player=='hit':
        old_action=action_player
        new_card=pick_cards(1)
        player.cards=np.append(player.cards,new_card)

        player_sum_choice, action_player, usable_ace_player=decide(player.cards,player.stick_threshold)
        if action_player == 'hit':
            rewards.append(0)
            states.append(player_sum_choice)

    dealer_sum_choice, action_dealer,usable_ace_dealer = decide(dealer.cards, dealer.stick_threshold)

    if action_player != 'bust':
        dealer_played = True
        while action_dealer == 'hit':
            new_card = pick_cards(1)
            dealer.cards = np.append(dealer.cards, new_card)
            dealer_sum_choice,action_dealer,usable_ace_dealer = decide(dealer.cards, dealer.stick_threshold)

    decide_winner(player_sum_choice,dealer_sum_choice,action_player,action_dealer)
    states.append(player_sum_choice)
    rewards.append(game_results[Game_No])

    # Finding return portion of the algorithm
    G=0 # The return after last state change is 0 since that is the terminal state
    for step in np.arange(1,len(rewards)+1):
       G = G + rewards[-step] # Expected future return from that state
       if states[-step] not in states[0:-step] and states[-step]<22: # We are only updating returns for first visit to state
            Returns[usable_ace_player][dealer.cards[0]-1][states[-step]-1]+=[G] # Storing the expected return for that state


for k in range(2):
    for j in range(10):
        for i in range(21):
            if not not Returns[k][j][i]:
                state_values[k][j][i] = np.mean(Returns[k][j][i])

# Obtaining plots shown in the book for sum of cards between 12 to 21
fig1 = plt.figure()
ax = fig1.gca(projection='3d')
ax.set_title('Non usable ace')
X=np.arange(1,11)
Y=np.arange(12,22)
Y,X=np.meshgrid(Y,X)
Z=np.array(state_values[:1,:,11:21])
Z=np.reshape(Z,(10,10))
ax.plot_wireframe(X,Y,Z)
ax.set_xticks(np.arange(1,10,1))
ax.set_yticks(np.arange(12,22,1))
ax.set_zticks(np.arange(-1,1.1,0.2))
ax.set_zlim([-1,1])
ax.set_xlabel('Dealers first card')
ax.set_ylabel('Sum of cards')
ax.set_zlabel('Average expected return')

plt.savefig("NonUsableAce.png")

fig2 = plt.figure()
ax = fig2.gca(projection='3d')
ax.set_title('Usable ace')
X=np.arange(1,11)
Y=np.arange(12,22)
Y,X=np.meshgrid(Y,X)
Z=np.array(state_values[1:,:,11:21])
Z=np.reshape(Z,(10,10))
ax.plot_wireframe(X,Y,Z)
ax.set_xticks(np.arange(1,10,1))
ax.set_yticks(np.arange(12,22,1))
ax.set_zticks(np.arange(-1,1.1,0.2))
ax.set_zlim([-1,1])
ax.set_xlabel('Dealers first card')
ax.set_ylabel('Sum of cards')
ax.set_zlabel('Average expected return')
plt.savefig("UsableAce.png")

# Obtaining plots for other state values between 1 and 12
fig3 = plt.figure()
ax = fig3.gca(projection='3d')
ax.set_title('Non usable ace')
X=np.arange(1,11)
Y=np.arange(1,22)
Y,X=np.meshgrid(Y,X)
Z=np.array(state_values[:1,:,:])
Z=np.reshape(Z,(10,21))
ax.plot_wireframe(X,Y,Z)
ax.set_xticks(np.arange(1,10,1))
ax.set_yticks(np.arange(1,22,1))
ax.set_zticks(np.arange(-1,1.1,0.2))
ax.set_zlim([-1,1])
ax.set_xlabel('Dealers first card')
ax.set_ylabel('Sum of cards')
ax.set_zlabel('Average expected return')

fig4 = plt.figure()
ax = fig4.gca(projection='3d')
ax.set_title('Usable ace')
X=np.arange(1,11)
Y=np.arange(1,22)
Y,X=np.meshgrid(Y,X)
Z=np.array(state_values[1:,:,:])
Z=np.reshape(Z,(10,21))
ax.plot_wireframe(X,Y,Z)
ax.set_xticks(np.arange(1,10,1))
ax.set_yticks(np.arange(1,22,1))
ax.set_zticks(np.arange(-1,1.1,0.2))
ax.set_zlim([-1,1])
ax.set_xlabel('Dealers first card')
ax.set_ylabel('Sum of cards')
ax.set_zlabel('Average expected return')

plt.show()
