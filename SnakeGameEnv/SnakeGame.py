import copy
import numpy as np
import random
import cv2
import moviepy.editor as mpe

class SnakeGame():
    def check(self):
        print(self.n)

    def __init__(self,n):
        self.n = n
        self.head = (random.randint(0,self.n-1),random.randint(0,self.n-1))
        self.direction = (-1,0)
        for each in range(random.randint(0,3)):
            dx, dy = self.direction
            dyn = -1 * dx
            dxn = dy
            self.direction = (dxn, dyn)
        self.snake = []
        size = (64 * self.n, 64 * self.n, 3)
        self.img = np.ones(size, np.float64) * 255
        self.readSprites()
        self.addFood()
        self.steps = 0
        self.totalSteps = 0
        self.vidImages = []
        self.renderImage()

    # add new food
    def addFood(self):
        x = random.randint(0,self.n-1)
        y = random.randint(0,self.n-1)
        if (x,y) not in self.snake and (x,y) != self.head:
            self.food = (x,y)
            self.renderElement(x,y,4,None)
        else:
            self.addFood()

    def render(self):
        for i in range(self.n):
            line = "|"
            for j in range(self.n):
                if (i,j) in self.snake:
                    line = line + "o"
                elif (i,j)==self.head:
                    line = line + "x"
                elif (i,j)==self.food:
                    line = line + "+"
                else:
                    line = line + " "
            line = line + "|"
            print(line)

    def tupleSubtraction(self,t1,t2):
        return (((t1[0]-t2[0]+1)%self.n)-1,((t1[1]-t2[1]+1)%self.n)-1)

    def tupleAddition(self,t1,t2):
        return (((t1[0]+t2[0]+1)%self.n)-1,((t1[1]+t2[1]+1)%self.n)-1)

    def readSprites(self):
        sprites = cv2.imread("snhxZ.jpg",cv2.IMREAD_UNCHANGED)
        # print((sprites.shape))
        # up down left right
        self.headSprite = [sprites[0:64,192:256],sprites[64:128,256:320],sprites[64:128,192:256],sprites[0:64,256:320]]
        # up left
        self.bodySprite = [sprites[64:128,128:192],sprites[0:64,64:128]]
        # ne nw sw se
        self.turnSprite = [sprites[128:192,128:192],sprites[64:128,0:64],sprites[0:64,0:64],sprites[0:64,128:192]]
        # up down left right
        self.tailSprite = [sprites[192:256,256:320],sprites[128:192,192:256],sprites[128:192,256:320],sprites[192:256,192:256]]

        self.foodSprite = sprites[192:256,0:64]
        self.nullSprite = sprites[192:256,64:128]

    def renderElement(self,i,j,type,dir):
        self.img[i * 64:(i + 1) * 64, j * 64:(j + 1) * 64] = np.ones((64,64,3),np.float64) * 255
        idx = 0
        if type == 1:
            if dir == (-1,0):
                idx = 0
            elif dir == (1,0):
                idx = 1
            elif dir == (0,-1):
                idx = 2
            elif dir == (0,1):
                idx = 3
            self.img[i*64:(i+1)*64,j*64:(j+1)*64] = self.headSprite[idx]
        elif type == 2:
            if dir == (-1,-1):
                idx = 0
            elif dir == (-1,1):
                idx = 1
            elif dir == (1,1):
                idx = 2
            elif dir == (1,-1):
                idx = 3
            self.img[i * 64:(i + 1) * 64, j * 64:(j + 1) * 64] = self.turnSprite[idx]
        elif type == 3:
            if dir == (-1,0):
                idx = 0
            elif dir == (1,0):
                idx = 1
            elif dir == (0,-1):
                idx = 2
            elif dir == (0,1):
                idx = 3
            self.img[i * 64:(i + 1) * 64, j * 64:(j + 1) * 64] = self.tailSprite[idx]
        elif type == 4:
            self.img[i * 64:(i + 1) * 64, j * 64:(j + 1) * 64] = self.foodSprite
        elif type == 5:
            if dir == (1,0):
                idx = 1
            elif dir == (0,1):
                idx = 0
            self.img[i * 64:(i + 1) * 64, j * 64:(j + 1) * 64] = self.bodySprite[idx]

    def renderImage(self):
        size = (64*self.n, 64*self.n, 3)
        self.img = np.ones(size, np.float64)*255

        # render head
        dir = self.direction
        i,j=self.head
        self.renderElement(i,j,1,dir)

        #render body
        prev = self.head
        for id in range(len(self.snake)-1):
            i,j = self.snake[id]
            next = self.snake[id+1]
            if next[1]==prev[1]:
                self.renderElement(i,j,5,(0,1))
            elif next[0]==prev[0]:
                self.renderElement(i,j,5,(1,0))
            else:
                self.renderElement(i,j,2,self.tupleAddition(prev,self.tupleSubtraction(next,(i*2,j*2))))
            prev = (i,j)

        #render tail
        try:
            i,j = self.snake[-1]
            dir = self.tupleSubtraction(self.snake[-1] , prev)
            self.renderElement(i,j,3,dir)
        except IndexError:
            pass

        #render food
        i,j=self.food
        self.renderElement(i,j,4,None)

        img = copy.deepcopy(self.img)
        self.vidImages.append(img.astype(np.uint8))

    def saveGameVideo(self,loc):
        size = (64*self.n, 64*self.n)
        out = cv2.VideoWriter(loc, cv2.VideoWriter_fourcc(*'MJPG'), 2, size)
        for img in self.vidImages:
            rimg = cv2.resize(img, size, interpolation  = cv2.INTER_NEAREST)
            out.write(rimg)
        out.release()
        game_clip = mpe.VideoFileClip(loc)
        audio_background = mpe.AudioFileClip('bgm.wav')
        audio_loop = mpe.afx.audio_loop(audio_background, duration=game_clip.duration)

        new_audioclip = mpe.CompositeAudioClip([audio_loop])
        final_clip = game_clip.set_audio(new_audioclip)
        # final_clip.write_videofile(loc)

    def renderState(self,state):
        state = state.flatten()
        for i in range(self.n):
            line = "|"
            for j in range(self.n):
                if (i,j)==(state[self.n*self.n],state[self.n*self.n+1]):
                    line = line + "x"
                elif (i,j)==(state[self.n*self.n+4],state[self.n*self.n+5]):
                    line = line + "+"
                elif state[self.n*i+j] == 1:
                    line = line + "o"
                else:
                    line = line + " "
            line = line + "|"
            print(line)

    def addTuples(self,a,b):
        return (a[0]+b[0],a[1]+b[1])

    def checkLimits(self,a):
        return a[0]<0 or a[0]>(self.n-1) or a[1]<0 or a[1]>(self.n-1)

    def updateLimits(self,a):
        return (a[0]%self.n, a[1]%self.n)

    def takeStep(self, handle=None):
        self.steps = self.steps + 1
        self.totalSteps = self.totalSteps + 1
        if handle!=None and handle!=0:
            dx, dy = self.direction
            dyn = -1 * dx * handle
            dxn = dy * handle
            self.direction = (dxn,dyn)
        newHead = self.addTuples(self.direction,self.head)
        newHead = self.updateLimits(newHead)
        if newHead in self.snake[:-1] or self.checkLimits(newHead):
            return -1
        if newHead==self.food:
            if len(self.snake) > ((self.n) * (self.n)) - 3:
                print("GAME OVER!!!!")
                return 2
            self.snake.insert(0,self.head)
            self.head = newHead
            self.addFood()
            # reward = (len(self.snake)+1)/self.steps
            reward = 1
            self.steps = 0
            self.renderImage()
            return reward
        else:
            self.snake.insert(0, self.head)
            self.snake.pop()
            self.head = newHead
            self.renderImage()
            return -0.0001

    def getFutureState(self,handle=None):
        game = copy.deepcopy(self)
        fState = game.getState()
        fReward = game.takeStep(handle=handle)
        return fState,fReward

    def futureStateVector(self):
        vec = []
        for i in [-1,0,1]:
            r,s = self.getFutureState(handle=i)
            vec.append((r,s))
        return vec

    def getState(self):
        n = self.n
        try:
            tail = self.snake[-1]
        except IndexError:
            tail = self.head
        direction = self.direction
        head = self.head
        food = self.food
        snake = copy.deepcopy(self.snake)
        while direction != (-1, 0):
            dx, dy = direction
            dyn = -1 * dx
            dxn = dy
            direction = (dxn, dyn)
            for i in range(len(snake)):
                bodyx,bodyy = snake[i]
                snake[i] = (bodyy,n-1-bodyx)
            dx,dy = head
            head = (dy,n-1-dx)
            dx, dy = tail
            tail = (dy, n - 1 - dx)
            dx,dy = food
            food = (dy,n-1-dx)
        grid = np.zeros((n, n))
        for biti, bitj in snake:
            grid[biti, bitj] = 1
        state = np.append(grid.flatten(),[head[0],head[1],tail[0],tail[1],food[0],food[1]])
        return np.array([state])

    def getStateTrain(self):
        return self.getState(),self.futureStateVector()