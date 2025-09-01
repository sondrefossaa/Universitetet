'''
Install Pygame
1. Open Terminal or Command Center
2. "pip install pygame"

Install VS Code
1. Google "vs code"
2. Follow download instructions
'''
# Get pieces of code for system and pygame
import sys, pygame
import math
# Initialize pygame so we get access to the pieces of code
pygame.init()

# Create the game window
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Mitt spill')

# Create the game clock
clock = pygame.time.Clock()

# Create the game loop
running = True # While this variable (boolean) is true, the game runs
while running:
    # Events - We check what the player inputs to the game
    for event in pygame.event.get(): # Check if player exits the game
        if event.type == pygame.QUIT:
            running = False
    
    # Updates - Movement, collisions, etc

    # Drawing - Updating the screen
    #pygame.draw.circle(screen, pygame.Color(255,255,255),(width/2,height/2), 10)
    
    #pygame.draw.rect(screen, pygame.Color(255,255,255), )   
    screen.fill(pygame.Color(255,0,0),(0,0,width,height))
    pygame.draw.rect(screen, pygame.Color(0,0,255), (0,0,width/2,height/2))
    pygame.draw.circle(screen, pygame.Color(255,255,255),(width/4, height/4),50)
    rad = 50
    centerx = width/4
    centery = height/4
    triangle_width = 10
    triangle_height = 30
    
    #pygame.draw.polygon(screen,pygame.Color(255,255,255),([centerx-triangle_width, centery + rad],[centerx+triangle_width, centery + rad],[centerx, centery + rad+triangle_height]))
    diff = 360/12
    for i in range(12):
        offset = i*diff
        offsetx = offset
        offsety = offset
        centerx = width/4
        centery = height/4
        triangle_width = 10
        triangle_height = 30
        pygame.draw.polygon(screen,pygame.Color(255,255,255),([centerx-triangle_width, centery + rad],[centerx+triangle_width, centery + rad],[centerx, centery + rad+triangle_height]))
import pygame, math

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

width, height = screen.get_size()
centerx = width // 2
centery = height // 2

triangle_width = 10
triangle_height = 30
rad = 100  # circle radius

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # draw 12 triangles around the circle
    for i in range(12):
        angle = math.radians(i * 30)  # 360/12 = 30 degrees per step
        # center point of triangle base
        bx = centerx + rad * math.cos(angle)
        by = centery + rad * math.sin(angle)

        # direction perpendicular to radius (for triangle base width)
        perp_angle = angle + math.pi / 2
        dx = triangle_width * math.cos(perp_angle)
        dy = triangle_width * math.sin(perp_angle)

        # triangle points
        p1 = (bx - dx, by - dy)  # left base
        p2 = (bx + dx, by + dy)  # right base
        tipx = centerx + (rad + triangle_height) * math.cos(angle)
        tipy = centery + (rad + triangle_height) * math.sin(angle)
        p3 = (tipx, tipy)  # tip outward

        pygame.draw.polygon(screen, (255, 255, 255), [p1, p2, p3])
    # We use pygame.draw to draw the shapes

    pygame.display.flip() # This updates the screen (double buffer, front/back)
    clock.tick(60) # The game updates at 60 frames per second

# When we exit the loop, the game ends and the program closes
pygame.quit()
sys.exit()