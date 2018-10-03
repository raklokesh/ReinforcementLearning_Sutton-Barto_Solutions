import numpy as np
import matplotlib.pyplot as plt

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
    if 1 in cards:
        other_sum=np.sum(np.delete(cards,np.random.choice(np.flatnonzero(cards == 1))))
        include_sum_11=11+other_sum
        if include_sum_11 > 21:
            decision_sum=np.sum(cards)
        else:
            decision_sum=include_sum_11

        return decision_sum,choose_action(decision_sum,threshold)
    else:
        decision_sum=np.sum(cards)
        return decision_sum,choose_action(decision_sum,threshold)

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
state_values=np.zeros(21)

Returns=[[] for i in range(21)]


game_results=[]
Games=10000

player=player()
dealer=dealer()


for Game_No in range(Games):
    if Game_No in np.arange(0,Games,1000):
        print("Finished {} games".format(Game_No))

    rewards=[]
    states=[]

    player.__init__()
    dealer.__init__()
    dealer_played=False

    player_sum_choice, action_player = decide(player.cards, player.stick_threshold)
    states.append(player_sum_choice)

    game_ended = False
    while action_player=='hit':
        old_action=action_player

        new_card=pick_cards(1)
        player.cards=np.append(player.cards,new_card)

        player_sum_choice,action_player=decide(player.cards,player.stick_threshold)

        if old_action == 'hit' and action_player == 'hit':
            rewards.append(0)
            states.append(player_sum_choice)

    dealer_sum_choice, action_dealer = decide(dealer.cards, dealer.stick_threshold)

    if action_player != 'bust':
        dealer_played = True
        while action_dealer == 'hit':
            new_card = pick_cards(1)
            dealer.cards = np.append(dealer.cards, new_card)
            dealer_sum_choice,action_dealer = decide(dealer.cards, dealer.stick_threshold)

    decide_winner(player_sum_choice,dealer_sum_choice,action_player,action_dealer)
    states.append(player_sum_choice)
    rewards.append(game_results[Game_No])

    G=0 # The return after last state change is 0 since that is the terminal state
    for step in np.arange(1,len(rewards)+1):
       G = G + rewards[-step] # Expected future return from that state
       Returns[states[-step-1]-1]+=[G] # Storing the expected return for that state


for i in range(21):
    if not not Returns[i]:
        state_values[i] = np.mean(Returns[i])


Value_plot=plt.subplot()
Value_plot.plot(np.arange(12,22,1),state_values[11:21],'r--')
Value_plot.set_yticks(np.arange(-1,1.1,0.2))
Value_plot.set_xticks(np.arange(12,22,1))
Value_plot.set_ylabel('Average expected return (State values) ')
Value_plot.set_xlabel('States ')

plt.savefig("State_Values" + ".png", bbox_inches="tight")
