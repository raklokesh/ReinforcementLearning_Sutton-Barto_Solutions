import numpy as np


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
        action = 'h'
    elif decision_sum in np.arange(threshold, 22):
        action = 's'
    else:
        action = 'e'

    return action


def pick_cards(n):
    return np.random.choice(deck,n)

def decide_winner(player_sum,dealer_sum, check_stop):
    if check_stop == 'c':
        if dealer_sum == 21 or player_sum > 21:
            game_results.append(-1)
            return True
        elif player_sum == 21 or dealer_sum > 21:
            game_results.append(1)
            return True
        else:
            return False
    elif check_stop == 's':
        if player_sum>dealer_sum:
            game_results.append(1)
        elif player_sum<dealer_sum:
            game_results.append(-1)
        else:
            game_results.append(0)
        return True
    else:
        game_results.append(0)
        return True

deck=np.arange(1,10)
deck=np.append(deck,[10,10,10,10])
deck=np.repeat(deck,4)
game_results=[]
Games=100

player=player()
dealer=dealer()


for Game_No in range(Games):

    player.__init__()
    dealer.__init__()

    player_sum_choice, action_player = decide(player.cards, player.stick_threshold)
    dealer_sum_choice, action_dealer = decide(dealer.cards, dealer.stick_threshold)


    game_ended = False
    while not game_ended:
        if action_player == 'h':
            new_card=pick_cards(1)
            player.cards=np.append(player.cards,new_card)
        if action_dealer == 'h':
            new_card = pick_cards(1)
            dealer.cards = np.append(dealer.cards, new_card)
        player_sum_choice,action_player=decide(player.cards,player.stick_threshold)
        dealer_sum_choice,action_dealer = decide(dealer.cards, dealer.stick_threshold)
        if (action_dealer=='s' and action_player=='s') or (action_dealer=='e' and action_player=='e'):
            game_ended=decide_winner(player_sum_choice,dealer_sum_choice,action_dealer)
        else:
            game_ended = decide_winner(player_sum_choice, dealer_sum_choice, 'c')







