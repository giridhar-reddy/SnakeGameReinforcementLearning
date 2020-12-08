from keras.models import load_model
from SnakeGameEnv.SnakeGame import SnakeGame
import numpy as np

model = load_model("model.h5")

while input("start new game(y/n)?")=="y":
    game = SnakeGame(6)
    r = 0
    r_sum = 0
    steps = 0
    while r > -1:
        state, fStates = game.getStateTrain()
        a = np.argmax(model.predict(state))
        state = game.getState()
        r = game.takeStep(handle=a - 1)
        print(game.renderState(game.getState()))
        if r == 2:
            break
        r_sum += r

    print(len(game.snake))
    print(game.totalSteps)
    game.saveGameVideo("AIgraphicgame.mp4")
    del (game)