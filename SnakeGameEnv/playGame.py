from SnakeGameEnv.SnakeGame import SnakeGame

s = SnakeGame(5)
s.check()

while 1:
    s.render()
    print(s.direction)
    try:
        a = int(input(""))
    except ValueError:
        pass
    reward = s.takeStep(handle=a)
    print(s.renderState(s.getState()))
    if reward==-1:
        print("FAILURE!!!!!")
        break

s.saveGameVideo("game.avi")