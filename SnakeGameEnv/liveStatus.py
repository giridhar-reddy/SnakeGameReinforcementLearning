import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import os

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

def animate(i):
    step_data = open(r'C:\Users\karamvenkatsaigiridh\Desktop\projects\SnakeGame\SnakeGameEnv\steps.txt','r').read()
    lines = step_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    ax1.clear()
    ax1.plot(xs, ys)
    ax1.set_title("steps")

    reward_data = open(r'C:\Users\karamvenkatsaigiridh\Desktop\projects\SnakeGame\SnakeGameEnv\rewards.txt', 'r').read()
    lines = reward_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    ax2.clear()
    ax2.plot(xs, ys)
    ax2.set_title("rewards")

    dist_data = open(r'C:\Users\karamvenkatsaigiridh\Desktop\projects\SnakeGame\SnakeGameEnv\dist.txt', 'r').read()
    lines = dist_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    sortedTuples = sorted([(a,b) for a,b in zip(xs,ys)] , key = lambda x: int(x[0]))
    xs = [x[0] for x in sortedTuples]
    ys = [x[1] for x in sortedTuples]
    ax3.clear()
    ax3.plot(xs, ys)
    ax3.set_title("reward distribution")

    eps_data = open(r'C:\Users\karamvenkatsaigiridh\Desktop\projects\SnakeGame\SnakeGameEnv\eps.txt', 'r').read()
    lines = eps_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    ax4.clear()
    ax4.plot(xs, ys)
    ax4.set_title("epsilon")

    plt.legend


while not (os.path.exists("rewards.txt") and os.path.exists("eps.txt") and os.path.exists("steps.txt") and os.path.exists("dist.txt")):
    time.sleep(5)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()