	
# tested on     
# gym==0.26.2
# gym-notices==0.0.8
 
#gymnasium==0.27.0
#gymnasium-notices==0.0.1
 
# classical gym 
import gymnasium as gym
# instead of gym, import gymnasium 
#import gymnasium as gym
import numpy as np
import time
 
 
# create environment
env=gym.make('CartPole-v1',render_mode='human')

# simulate the environment
episodeNumber=5
timeSteps=100
 
 
for episodeIndex in range(episodeNumber):
    initial_state=env.reset()
    print(episodeIndex)
    env.render()
    appendedObservations=[]
    for timeIndex in range(timeSteps):
        print(timeIndex)
        random_action=env.action_space.sample()
        observation, reward, terminated, truncated, info =env.step(random_action)
        appendedObservations.append(observation)
        time.sleep(0.1)
        if (terminated):
            time.sleep(1)
            break
env.close()   