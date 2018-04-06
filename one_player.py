from pygame.locals import *
from random import randint
import pygame
import time
 
class Apple:
    x = 0
    y = 0
    xstep = 52
    ystep = 50
 
    def __init__(self,x,y):
        self.x = x * self.xstep
        self.y = y * self.ystep
 
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y)) 
 
 
class Player:
    x = [0]
    y = [0]
    xstep = 52
    ystep = 50
    direction = 0
    length = 3
    moved = False
    speed = 1
 
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self, length):
       self.length = length
       for i in range(0,2000):
           self.x.append(-100)
           self.y.append(-100)
 
       # initial positions, no collision.
       self.x[1] = 1*52
       self.x[2] = 2*52
 
    def update(self):
        
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
            #print("Update")
            self.moved = False
            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
 
            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.xstep
            if self.direction == 1:
                self.x[0] = self.x[0] - self.xstep
            if self.direction == 2:
                self.y[0] = self.y[0] - self.ystep
            if self.direction == 3:
                self.y[0] = self.y[0] + self.ystep
 
            self.updateCount = 0
 
 
    def moveRight(self):
        if self.direction != 1 and not self.moved:
            #print("R: direction: " + str(self.direction))
            self.direction = 0
            self.moved = True
 
    def moveLeft(self):
        if self.direction != 0 and not self.moved:
            #print("L: direction: " + str(self.direction))
            self.direction = 1
            self.moved = True
 
    def moveUp(self):
        if self.direction != 3 and not self.moved:
            #print("U: direction: " + str(self.direction))
            self.direction = 2
            self.moved = True
 
    def moveDown(self):
        if self.direction != 2 and not self.moved:
            #print("D: direction: " + str(self.direction))
            self.direction = 3
            self.moved = True
 
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 
 
class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False
 
class App:
 
    windowWidth = 1404
    windowHeight = 600
    player = 0
    apple = 0
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.player = Player(3) 
        self.apple = Apple(5,5)
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.image.load("block.jpg").convert()
        self._apple_surf = pygame.image.load("apple.jpg").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        self.player.update()
 
        # does snake eat apple?
        for i in range(0,self.player.length):
            if self.game.isCollision(self.apple.x,self.apple.y,self.player.x[i], self.player.y[i],44):
                self.apple.x = randint(2,26) * 52
                self.apple.y = randint(2,10) * 50
                self.player.length = self.player.length + 1
 
 
        # does snake collide with itself?
        for i in range(2,self.player.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],40):
                print("You lose!")
                exit(0)

        if self.player.x[0] < 0:
            print("You lose!")
            exit(0)

        if self.player.x[0] + 52 > self.windowWidth:
            print("You lose!")
            exit(0)

        if self.player.y[0] + 50 > self.windowHeight:
            print("You lose!")
            exit(0)

        if self.player.y[0] < 0:
            print("You lose!")
            exit(0)
        
        
 
        pass
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 
 
            if (keys[K_RIGHT]):
                self.player.moveRight()
 
            if (keys[K_LEFT]):
                self.player.moveLeft()
 
            if (keys[K_UP]):
                self.player.moveUp()
 
            if (keys[K_DOWN]):
                self.player.moveDown()
 
            if (keys[K_ESCAPE]):
                self._running = False
            
            event = pygame.event.get()
            if event:
                if event[0].type == pygame.QUIT:
                    self._running = False
 
            self.on_loop()
            self.on_render()
 
            time.sleep (5.0 / 1000.0 * self.player.speed);
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
