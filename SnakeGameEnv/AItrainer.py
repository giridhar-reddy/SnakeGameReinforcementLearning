import numpy as np
from keras.models import Sequential
from keras.layers import Dense,InputLayer
from SnakeGameEnv.SnakeGame import SnakeGame
from collections import Counter
import os
from keras.models import load_model

def refreshTrainMap(trainMap):
    maxProb = max([a for a,b in trainMap.items()]+[0])
    if maxProb<0.5:
        trainMap = dict({(a,b/maxProb) for a,b in trainMap.items()})
    return trainMap
square=6

model = Sequential()
model.add(Dense(2*square*square+8,input_shape=(square*square+6,)))
model.add(Dense(square*square+8, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(3, activation='linear'))
model.compile(loss='mse', optimizer='adam', metrics=['mae'])

# paramters
y = 0.9
epsMain = 0.5
decay_eps = 100000
decay_train = 100000
num_episodes = 50000
statusBreak = 100
performanceWindow = 100
epsMap = dict()
trainMap = dict()

train_decay_factor = 1 - (1 / decay_train)
eps_decay_factor = 1 - (1 / decay_eps)
r_avg_list = []
s_avg_list = []
epstrack = []
runningSampler = []
sampleVec = {}

model = load_model("model.h5")

# os.remove("dist.txt")
if os.path.exists("rewards.txt"):
    os.remove("rewards.txt")
if os.path.exists("eps.txt"):
    os.remove("eps.txt")
if os.path.exists("steps.txt"):
    os.remove("steps.txt")

for i in range(num_episodes):
    # initialise game
    game = SnakeGame(square)
    print("episode:{}".format(str(i)))

    # save dashboard metrics
    if (i+1) % statusBreak == 0:
        print("Average reward:{}".format(np.mean(r_avg_list[-performanceWindow:])))
        with open("rewards.txt",'a') as rf:
            rf.write("{},{}\n".format(i,np.mean(r_avg_list[-performanceWindow:])))
        print("Average steps taken:{}".format(np.mean(s_avg_list[-performanceWindow:])))
        with open("steps.txt",'a') as sf:
            sf.write("{},{}\n".format(i,np.mean(s_avg_list[-performanceWindow:])))
        print("Average eps:{}".format(np.mean(epstrack[-performanceWindow:])))
        with open("eps.txt",'a') as ef:
            ef.write("{},{}\n".format(i,np.mean(epstrack[-performanceWindow:])))
        map = dict(Counter(r_avg_list[-performanceWindow:]))
        repr = "\n".join(["{},{}".format(k,v) for k,v in map.items()])
        with open("dist.txt",'w') as df:
            df.write(repr)
        print("Episode {} of {}".format(i + 1, num_episodes))
        model.save("model.h5")

    # update sampler
    trainMap = refreshTrainMap(trainMap)
    print(trainMap)
    print(epsMap)

    # play game
    r = 0
    steps = 0
    while r>-1:
        # set epsilon
        eps = epsMap.get(len(game.snake),epsMain)
        eps *= eps_decay_factor
        epsMap[len(game.snake)] = eps

        # get next step
        if np.random.random() < eps:
            a = np.random.randint(0, 2)
        else:
            state,fStates = game.getStateTrain()
            a = np.argmax(model.predict(state))

        # take step
        state = game.getState()
        runningSampler.append(1+len(game.snake))
        r = game.takeStep(handle=a-1)
        if r==2:
            break

        # read train probability
        trainprob = trainMap.get(len(game.snake), 1)
        trainprob *= train_decay_factor
        trainMap[len(game.snake)] = trainprob

        # train
        if np.random.random()<trainprob:
            new_s = game.getState()
            if r>-1:
                target = r + y * np.max(model.predict(new_s))
            else:
                target = r
            target_vec = model.predict(state)[0]
            target_vec[a] = target
            model.fit(state, target_vec.reshape(-1, 3), epochs=1, verbose=0)

    r_avg_list.append(len(game.snake))
    s_avg_list.append(game.totalSteps)
    epstrack.append(eps)
    # game.saveGameVideo("gameEpoch6x6/{}.avi".format(i%100))
    del(game)
print(r_avg_list)
print(s_avg_list)
