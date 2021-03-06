from pygame.locals import *
from random import randint
import pygame
import time
import socket
 
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
    x = []
    y = []
    xstep = 52
    ystep = 50
    direction = 0
    length = 3
    moved = False
    speed = 1
    number = 1
 
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self, length, number):
       self.length = length
       self.number = number
       if number % 2 != 0:
           self.x = [0]
       else:
           self.x = [18 * 52]

       if number > 2: 
           self.y = [8 * 52]
       else:
           self.y = [0]

       self.direction = ((number % 2) + 1) % 2 
       for i in range(0,2000):
           self.x.append(-100)
           self.y.append(-100)
    
       # initial positions, no collision.
       self.x[1] = self.x[0] + 52
       self.x[2] = self.x[1] + 52
 
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

    def oppositeDirection(self, d1, d2):
        if d1 == 0 and d2 == 1:
            return True

        if d1 == 1 and d2 == 0:
            return True

        if d1 == 2 and d2 == 3:
            return True

        if d1 == 3 and d2 == 2:
            return True

        return False
        
 
class App:
 
    windowWidth = 1404
    windowHeight = 600
    player = 0
    apple = 0
    local = False
    IP = '169.231.100.251'
    PORT = 12345
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.players = [Player(3, 1), Player(3, 2)] 
        self.apple = Apple(5,5)
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.image.load("block.bmp").convert()
        self._apple_surf = pygame.image.load("apple.bmp").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self, player):
        if not self._running:
            return
        player.update()
 
        # does snake eat apple?
        for i in range(0,player.length):
            if self.game.isCollision(self.apple.x,self.apple.y,player.x[i], player.y[i],44):
                self.apple.x = randint(2,26) * 52
                self.apple.y = randint(2,10) * 50
                player.length = player.length + 1
 
 
        # does snake collide with itself?
        for i in range(2,player.length):
            if self.game.isCollision(player.x[0],player.y[0],player.x[i], player.y[i],40):
               print("Player " + str(player.number) + " loses!")
               self._running = False

        #does snake leave screen
        if player.x[0] < 0:
            print("Player " + str(player.number) + " loses!")
            self._running = False

        if player.x[0] + 52 > self.windowWidth:
            print("Player " + str(player.number) + " loses!")
            self._running = False

        if player.y[0] + 50 > self.windowHeight:
           print("Player " + str(player.number) + " loses!")
           self._running = False

        if player.y[0] < 0:
           print("Player " + str(player.number) + " loses!")
           self._running = False

        #does snake collide with any other snake
        for p in self.players:
            if p.number == player.number:
                continue
            for i in range(0, p.length):
                if self.game.isCollision(player.x[0], player.y[0], p.x[i], p.y[i], 49):
                    self._running = False
                    if i == 0 and self.game.oppositeDirection(p.direction, player.direction):
                        print("Its a draw!")
                        return
                    else:
                        print("Player " + str(player.number) + " loses!")
                    
        
        
 
        pass
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        for player in self.players:
            player.draw(self._display_surf, self._image_surf)
        #self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        s = socket.socket()
        s.bind((self.IP, self.PORT))
        s.listen(5)
        c, addr = s.accept()
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 
            dir = c.recv(10)
            dir = dir.decode()
            c.send("ack".encode())
            self.players[1].direction = int(dir)
            #for playing locally
            if (keys[K_d] and local):
                self.players[1].moveRight()
 
            if (keys[K_a] and local):
                self.players[1].moveLeft()
 
            if (keys[K_w] and local):
                self.players[1].moveUp()
 
            if (keys[K_s] and local):
                self.players[1].moveDown()
 
            if (keys[K_RIGHT]):
                self.players[0].moveRight()
 
            if (keys[K_LEFT]):
                self.players[0].moveLeft()
 
            if (keys[K_UP]):
                self.players[0].moveUp()
 
            if (keys[K_DOWN]):
                self.players[0].moveDown()
 
            if (keys[K_ESCAPE]):
                self._running = False
            
            event = pygame.event.get()
            if event:
                if event[0].type == pygame.QUIT:
                    self._running = False
 
            for player in self.players:
                self.on_loop(player)
            self.on_render()
 
            time.sleep (5.0 / 1000.0 )
        self.on_cleanup()
        c.send("done".encode())
        c.close()
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
