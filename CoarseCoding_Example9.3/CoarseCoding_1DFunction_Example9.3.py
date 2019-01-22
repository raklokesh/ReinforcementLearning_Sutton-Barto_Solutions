import numpy as np
import matplotlib.pyplot as plt

def determine_featureRanges(l):
    centre_locations = np.arange(2,100,2)
    start,end = [i-l/2 for i in centre_locations],[i+l/2 for i in centre_locations]

    return start,end

def retrieve_funcValue(x):
    if x<20 or x>80:
        y = 0
    elif x<30:
        y = (x-20)*0.1
    elif x>70:
        y = 1 - (x - 70)*0.1
    else:
        y =1

    return y

def determine_gradientVector(x):
    vector = np.zeros(len(start_interval))
    start = np.argmax(end_interval>x)
    end = np.argmax(start_interval>x)

    if end < start:
        end = len(start_interval)

    for i in np.arange(start,end):
        vector[i] = 1

    return vector

def determine_featureVectors():
    vectors = np.zeros((len(STATE_RANGE),len(start_interval)))
    for index,x in enumerate(STATE_RANGE):
        vector = determine_gradientVector(x)
        vectors[index,:] = vector

    return vectors


STATE_RANGE = np.arange(0,100.5,0.5)
FEATURE_LENGTH = 25
start_interval,end_interval = determine_featureRanges(FEATURE_LENGTH)
feature_vectors = determine_featureVectors()
weights = np.zeros(len(start_interval))
state_values = np.zeros(len(STATE_RANGE))

EPISODES = 10001
save_episodes = [10,40,160,640,2560,10000]
state_values_episodes = []
for episode in range(EPISODES):
    state = np.random.choice(STATE_RANGE)
    target_value = retrieve_funcValue(state)

    grad_vector = feature_vectors[np.where(STATE_RANGE == state)[0][0],:]
    n = np.sum(grad_vector)
    increment_vector = 0.2/n*(target_value - state_values[np.where(STATE_RANGE==state)])*grad_vector

    weights = [weights[i] + increment_vector[i] for i in range(len(weights))]

    state_values = np.dot(feature_vectors,weights)

    if episode in save_episodes:
        state_values_episodes.append(state_values)

true_funcValues = np.zeros(len(STATE_RANGE))
for i,state in enumerate(STATE_RANGE):
    true_funcValues[i] = retrieve_funcValue(state)

window = 4
new_stateValues = []
for values in state_values_episodes:
    new_stateValues.append([np.sum(values[i:min(i+window,len(values))])/window for i in np.arange(0,len(values))])

plt.figure(figsize= (6,16))
for plot_no in range(len(new_stateValues)):
    Function_apprx = plt.subplot(len(new_stateValues),1,plot_no+1)
    Function_apprx.plot(STATE_RANGE, true_funcValues,'-r',alpha = 0.5)
    Function_apprx.plot(STATE_RANGE,new_stateValues[plot_no])
    Function_apprx.set_ylim((0,1.2))
plt.savefig('FuncApprxPlot_feature_width = {}.png'.format(FEATURE_LENGTH))


