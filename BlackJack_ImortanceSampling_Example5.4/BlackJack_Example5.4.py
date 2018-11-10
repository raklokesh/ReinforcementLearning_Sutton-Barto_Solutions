import numpy as np
import matplotlib.pyplot as plt
import pickle

def decide(cards,threshold, policy, playing):

    usable_ace=0
    if 1 in cards:
        other_sum=np.sum(np.delete(cards,np.random.choice(np.flatnonzero(cards == 1.0))))
        include_sum_11=11+other_sum
        if include_sum_11 > 21:
            decision_sum=np.sum(cards)
        else:
            decision_sum=include_sum_11
            usable_ace = 1
    else:
        decision_sum=np.sum(cards)

    action_prob = 1
    if policy == 'T':
        bust,action = choose_action(decision_sum, threshold)
    elif playing:
        bust,targ_policy_action = choose_action(decision_sum, threshold)
        if not bust:
            e = np.random.random()
            if e>0.5:
                action =  'hit'
            else:
                action = 'stick'
            if action == targ_policy_action:
                action_prob = 1
            else:
                action_prob = 0
        else:
            action = 'none'
    else:
        bust,action = choose_action(decision_sum, threshold)

    return decision_sum,bust,action,action_prob,usable_ace

def choose_action(decision_sum,threshold):
    bust = False
    if decision_sum < threshold:
        action = 'hit'
    elif decision_sum in np.arange(threshold, 22):
        action = 'stick'
    else:
        action = 'none'
        bust = True

    return bust,action

def decide_winner(player_sum,dealer_sum,bust_player,bust_dealer):
    if bust_player:
        return -1
    elif bust_dealer:
        return 1
    else:
        if player_sum>dealer_sum:
            return 1
        elif dealer_sum>player_sum:
            return -1
        else:
            return -1

def run_games(policy):
    game_results = []
    Returns = np.zeros(Games)
    ImpSampRatio_AllGames = np.zeros(Games)

    for Game_No in range(Games):

        #if Game_No in np.arange(0,Games,Games/10):
           # print("Finished {} games".format(Game_No))

        rewards = []
        states = []
        ImpSamp_Ratio = 1
        target_policy_probs = []
        player_cards = np.array([1,2])
        dealer_cards = np.array([2,np.random.choice(deck,1)])

        playing = True
        bust_player = False
        bust_dealer = False

        player_sum_choice,bust_player,action_player,targ_action_prob, usable_ace_player  = decide(player_cards,player_threshold, policy,playing)
        rewards.append(0)
        states.append(player_sum_choice)
        ImpSamp_Ratio = ImpSamp_Ratio * targ_action_prob / 0.5

        while action_player == 'hit' and not bust_player:
            new_card = np.random.choice(deck,1)
            player_cards = np.append(player_cards, new_card)

            player_sum_choice, bust_player, action_player,targ_action_prob ,usable_ace_player = decide(player_cards, player_threshold, policy,playing)

            if action_player == 'hit' and not bust_player:
                rewards.append(0)
                states.append(player_sum_choice)
                ImpSamp_Ratio = ImpSamp_Ratio * targ_action_prob/0.5
            elif action_player == 'stick':
                ImpSamp_Ratio = ImpSamp_Ratio * targ_action_prob /0.5


        playing = False
        dealer_sum_choice, bust_dealer, action_dealer,_,usable_ace_dealer = decide(dealer_cards, dealer_threshold,policy,playing)

        if not bust_player:
            while action_dealer == 'hit' and not bust_dealer:
                new_card = np.random.choice(deck,1)
                dealer_cards = np.append(dealer_cards, new_card)
                dealer_sum_choice,bust_dealer,action_dealer,_,usable_ace_dealer = decide(dealer_cards, dealer_threshold,policy,playing)

        Returns[Game_No] = decide_winner(player_sum_choice,dealer_sum_choice,bust_player,bust_dealer)
        rewards.append(Returns[Game_No])
        states.append(player_sum_choice)
        ImpSampRatio_AllGames[Game_No] = ImpSamp_Ratio

    return Returns,ImpSampRatio_AllGames

deck=np.arange(1,10)
deck=np.append(deck,[10,10,10,10])
player_threshold = 20
dealer_threshold = 17

Games = 1000
true_state_value = -0.27726

runs = 1000

policy = 'T' # Running under target policy 'T' and averaging returns else under behavior policy and importance sampling to average returns
for run in range(runs):
    if run in np.arange(0,runs,runs/10):
        print('Run number {}'.format(run))
    if policy == 'T':
        Game_returns, ImpSampRatios = run_games(policy)
        if run == 0:
            MSE_avg_TPolicy = (np.cumsum(Game_returns)/np.arange(1,Games+1)-true_state_value)**2
        else:
            MSE_avg_TPolicy = MSE_avg_TPolicy + (np.cumsum(Game_returns)/np.arange(1,Games+1)-true_state_value)**2
    else:
        Game_returns,ImpSampRatios = run_games(policy)
        if run == 0:
            MSE_avg_OIS = (np.cumsum(Game_returns*ImpSampRatios)/np.arange(1,Games+1)-true_state_value)**2
            with np.errstate(divide='ignore', invalid='ignore'):
                MSE = (np.cumsum(Game_returns*ImpSampRatios) / np.cumsum(ImpSampRatios) - true_state_value) ** 2
            MSE[np.flatnonzero(np.isnan(MSE))] = 0
            MSE_avg_WIS = MSE
        else:
            MSE_avg_OIS = MSE_avg_OIS + (np.cumsum(Game_returns*ImpSampRatios)/np.arange(1,Games+1)-true_state_value)**2
            with np.errstate(divide='ignore', invalid='ignore'):
                MSE = (np.cumsum(Game_returns*ImpSampRatios) / np.cumsum(ImpSampRatios) - true_state_value) ** 2
            MSE[np.flatnonzero(np.isnan(MSE))] = 0
            MSE_avg_WIS = MSE_avg_WIS + MSE

if policy  == 'T':
    MSE_avg_TPolicy = MSE_avg_TPolicy / runs
else:
    MSE_avg_OIS = MSE_avg_OIS/runs
    MSE_avg_WIS = MSE_avg_WIS/runs
    MSE_results = np.array([MSE_avg_OIS,MSE_avg_WIS])

# f = open('MSE_Results.pckl', 'wb')
# pickle.dump(MSE_results, f)
# f.close()

# Use pickle to load data
# f = open('MSE_Results.pckl', 'rb')
# MSE_results = pickle.load(f)
# MSE_results = np.array([MSE_results[0,:],MSE_results[1,:],MSE_avg_TPolicy])

plot = False
if plot:
    plt.figure(2)
    MSE_plot = plt.subplot()
    MSE_plot.semilogx(np.arange(1,Games+1),MSE_results[0,:],'g', label = 'Ordinary Imp Samp')
    MSE_plot.semilogx(np.arange(1,Games+1),MSE_results[1,:],'r', label = 'Weighted Imp Samp')
    MSE_plot.semilogx(np.arange(1, Games + 1), MSE_results[2, :], 'b', label = 'Target Policy')
    MSE_plot.set_xlabel('Episodes')
    MSE_plot.set_ylabel('Mean Square Error Average (1000 runs)')
    MSE_plot.legend()
    MSE_plot.set_ylim([0,5])













