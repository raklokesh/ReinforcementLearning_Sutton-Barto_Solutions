import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as anim
import ffmpeg

def init_episode():
    start_state = np.array([-0.6+np.random.random()/5,0])
    start_action = np.random.choice(ACTIONS)
    episode_state = False

    return start_state,start_action,episode_state

class tiling:
    def __init__(self,x_tiles,y_tiles,x_bound,y_bound):
        self.tile_width = (x_bound[1]-x_bound[0])/x_tiles
        self.tile_height = (y_bound[1]-y_bound[0])/y_tiles
        self.x_bounds = np.arange(x_bound[0],x_bound[1]+0.1,self.tile_width)
        self.y_bounds = np.arange(y_bound[0], y_bound[1]+0.1, self.tile_height)
        self.tile_values = np.zeros((len(ACTIONS),x_tiles,y_tiles),dtype=float)

    def determine_tileValues(self,state):
        x_location = np.argmin(state[0]>self.x_bounds)-1
        y_location = np.argmin(state[1]>self.y_bounds)-1

        return self.tile_values[:,x_location,y_location]

    def update_tileValues(self,increment):
        x_location = np.argmin(current_state[0]>self.x_bounds)-1
        y_location = np.argmin(current_state[1]>self.y_bounds)-1
        self.tile_values[np.where(ACTIONS==current_action)[0][0],x_location,y_location] += increment


def choose_action():
    e = np.random.random()
    action_values = np.array([0, 0, 0], dtype=float)
    if e<0:
        action = np.random.choice(ACTIONS)
    else:
        for I,tiling in enumerate(tiling_list):
            action_values+=tiling.determine_tileValues(next_state)

        action =  ACTIONS[np.random.choice(np.flatnonzero(action_values == max(action_values)))]

    return action,np.max(action_values)

def update_actionValues():
    value_increment = ALFA*(reward + GAMMA * action_value2 - action_value1)
    for I, tiling in enumerate(tiling_list):
        tiling.update_tileValues(value_increment)


def current_stateActionValue():
    action_values = np.array([0, 0, 0], dtype=float)
    for I, tiling in enumerate(tiling_list):
        action_values += tiling.determine_tileValues(current_state)

    return action_values[np.where(ACTIONS == current_action)[0][0]]


ACTIONS = np.array([-1,0,1])
TILINGS = 8
TILES = 8
ALFA = 0.1/8
GAMMA = 0.9
EPISODES = 1000
position_bound = np.array([-1.2,0.5])
velocity_bound = np.array([-0.07, 0.07])
tile_offsetX = (position_bound[1]-position_bound[0])/TILINGS/TILES
tile_offsetY =  (velocity_bound[1]-velocity_bound[0])/TILINGS/TILES
tiling_list = []


for i in range(TILINGS):
    tile = tiling(TILES,TILES,position_bound+(i)*1*tile_offsetX,velocity_bound+(i)*3*tile_offsetY)
    tiling_list.append(tile)

episode_steps = []
episode_positions = []
for episode in range(EPISODES):
    if episode in np.arange(0,EPISODES,EPISODES/10):
        print('running episode : {}'.format(episode))
    current_state, current_action, episode_end = init_episode()
    step = 0
    state_memory = []
    while not episode_end and step<8000:
        next_state = np.array([current_state[0]+current_state[1],current_state[1]+0.001*current_action-0.0025*np.cos(3*current_state[0])])
        action_value1 = current_stateActionValue()
        reward = -1
        if next_state[0]<=position_bound[0]:
            next_state[1] = 0
            next_state[0] = current_state[0]
        elif next_state[0]>=position_bound[1]:
            episode_end = True
            action_value2 = 0
            update_actionValues()
            episode_steps.append(step)
            break
        if abs(next_state[1])>velocity_bound[1]:
            next_state[1] = next_state[1]/abs(next_state[1])*velocity_bound[1]

        next_action,action_value2 = choose_action()

        update_actionValues()

        current_state = next_state
        current_action = next_action

        state_memory.append(current_state[0])

        step += 1

    if episode in np.arange(0,EPISODES,EPISODES/50):
        episode_positions.append(state_memory)
    # plt.figure(EPISODES*2+episode+1)
    # state_plot = plt.subplot()
    # state_plot.plot(state_memory)

    if episode==999:# in np.arange(0,EPISODES,EPISODES/10):
        cost_to_go = np.zeros((100, 100))

        for i in range(100):
            for j in range(100):
                state = np.array([position_bound[0] + i * 1.7 / 100, velocity_bound[0] + j * 0.14 / 100])
                action_values = np.array([0, 0, 0], dtype=float)
                for I, tiling in enumerate(tiling_list):
                    action_values += tiling.determine_tileValues(state)
                cost_to_go[i, j] = -max(action_values)

        fig1 = plt.figure(episode)
        ax = fig1.gca(projection='3d')
        X = np.arange(position_bound[0], position_bound[1], 1.7 / 100)
        Y = np.arange(velocity_bound[0], velocity_bound[1], 0.14 / 100)
        Y, X = np.meshgrid(Y, X)
        Z = np.array(cost_to_go)
        Z = np.reshape(Z, (100, 100))
        ax.plot_surface(X, Y, Z,shade=False,edgecolor='k',linewidth=0.5)
        ax.set_xlabel('Position')
        ax.set_ylabel('Velocity')
        ax.set_zlabel('maximum cost to go')

if False:
    fig2= plt.figure()
    stepEpisode_plot = plt.subplot()
    stepEpisode_plot.plot(episode_steps)

episode = 49
if True:
    x_car = np.array(episode_positions[episode])
    y_car = np.sin(3*x_car)
    x_road = np.linspace(position_bound[0], position_bound[1], 100)
    y_road = np.sin(3*x_road)
    fig, ax = plt.subplots()
    ln, = plt.plot([],[], 'ro')
    plt.plot(x_road, y_road, 'k')

    def update(frame):
        x = x_car[frame]
        y = y_car[frame]
        ln.set_data(x,y)
        return ln,


    Writer = anim.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

    ani = anim.FuncAnimation(fig, update, frames=len(episode_positions[episode]), interval=10, blit=True)
    ani.save('Episode1000_Animation.mp4', writer = writer)
    plt.show()

