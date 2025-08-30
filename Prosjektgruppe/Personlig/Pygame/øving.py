import pygame as pg

pg.init()
screen_width = 800
screen_height = 600
screen = pg.display.set_mode((screen_width, screen_height))
clock = pg.time.Clock()
running = True
x, y = 400, 300
speed = 5

radius = 20


class Ball:
    def __init__(self, x, y, auto_move = False):
        self.x = x
        self.y = y
        self.speed = 10
        self.radius = 20
        self.auto_move = auto_move
        self.reverse = [1,1]
        
    def move(self, keys):
        if not self.auto_move:
            if keys[pg.K_LEFT] and self.x - self.radius > 0:
                self.x -= self.speed
            if keys[pg.K_RIGHT] and self.x + self.radius < screen_width:
                self.x += self.speed
            if keys[pg.K_UP] and self.y - self.radius > 0:
                self.y -= self.speed
            if keys[pg.K_DOWN] and self.y + self.radius < screen_height:
                self.y += self.speed
        else:
            if self.x + self.radius > screen_width or self.x - self.radius < 0:
                self.reverse[0] *= -1
            if self.y + self.radius > screen_height or self.y - self.radius < 0:
                self.reverse[1] *= -1
            self.x += self.speed * self.reverse[0]
            self.y += self.speed * self.reverse[1]
    def draw(self, screen):
        sirkel_surface = pg.Surface((self.radius*2, self.radius*2), pg.SRCALPHA)
        pg.draw.circle(sirkel_surface, (0, 255, 0), (self.radius, self.radius), self.radius)
        screen.blit(sirkel_surface, (self.x - self.radius, self.y - self.radius))
    def håndter_kollisjon(self, x_retning, y_orgin, y_retning):
        #print(x_retning, y_retning, self.x + self.radius)
        if self.x < x_retning + self.radius and self.y-self.radius > y_orgin and self.y-self.radius < y_retning:
            self.reverse[0] *= -1
            #self.reverse[1] *= -1
class Rekkert:
    def __init__(self,x, y, høyde = 200, bredde = 10):
        self.x = x
        self.y = y
        self.høyde = høyde
        self.bredde = bredde
        self.speed = 10
    def draw(self, srceen):
        pg.draw.rect(screen, (255, 255, 255), (self.x, self.y,self.bredde, self.høyde))
        
    def beveg(self, keys):
        if keys[pg.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pg.K_DOWN] and self.y + self.høyde < screen_height:
            self.y += self.speed
            
ball = Ball(x, y, True)
rekkert = Rekkert(10, 10 )
rekkerter = []
rekkerter.append(rekkert)
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
   
    bg = pg.Surface((800, 600))
    bg.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    
    #Håndter kollisjon
    ball.move(pg.key.get_pressed())
    for rekkert in rekkerter:
        ball.håndter_kollisjon(rekkert.x+rekkert.bredde,rekkert.y, rekkert.y+rekkert.høyde)
    
    
    ball.draw(screen)
    rekkert.draw(screen)
    rekkert.beveg(pg.key.get_pressed())
    pg.display.update()
    
    pg.time.Clock().tick(60)
    