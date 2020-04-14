# ---------- Packages and Inits ----------
import pygame, random, math, sys, os, pickle, time
from tkinter import *
from pygame.locals import *
from random import choice
pygame.init()

# ---------- Settings ----------

SCREEN_WIDTH  = 1920
SCREEN_HEIGHT = 1080
FPS = 60
CIRCLE_RADIUS = 70
ENEMY_SIZE = 40
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
SPEED = 2

# ---------- Resources (Images & Sounds) ----------

if getattr(sys, 'frozen', False):
    current_path = os.path.dirname(sys.executable)
else:
    current_path = os.path.dirname(os.path.realpath(__file__))

# PS2 images
button_circle_red_tiny = pygame.image.load('button_circle_red_tiny.png').convert()
button_square_pink_tiny = pygame.image.load('button_square_pink_tiny.png').convert()
button_triangle_green_tiny = pygame.image.load('button_triangle_green_tiny.png').convert()
button_cross_blue_tiny = pygame.image.load('button_cross_blue_tiny.png').convert()

# ---------- Resources (Colors) ----------
BLACK  = (000,000,000)
WHITE  = (255,255,255)

# ---------- Classes ----------
class Enemies:

    def __init__( self, x, y, size=ENEMY_SIZE, thick=0, color=BLACK, speed=2, position="top"):

        self.rect = button_circle_red_tiny.get_rect()

        if ( x == 0 and y == 0 ):
            self.randomise()

        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed
        self.calcDirection()
        self.position = position
        
    def calcDirection( self ):
        self.x_float = 1.0 * self.rect.centerx
        self.y_float = 1.0 * self.rect.centery

        # Determine direction vector from (x,y) to the centre of the screen
        self.position_vector = pygame.math.Vector2( self.x_float, self.y_float )
        self.velocity_vector = pygame.math.Vector2( SCREEN_WIDTH/2 - self.x_float, SCREEN_HEIGHT/2 - self.y_float )
        self.velocity_vector = self.velocity_vector.normalize()

    def update( self ):
        x_delta = self.speed * self.velocity_vector[0]
        y_delta = self.speed * self.velocity_vector[1]
        self.x_float += x_delta
        self.y_float += y_delta
        self.rect.centerx = int( self.x_float )
        self.rect.centery = int( self.y_float )

    def draw( self, screen):
        if self.position == "right":
            screen.blit(button_circle_red_tiny, self.rect )
        elif self.position == "left":
            screen.blit(button_square_pink_tiny, self.rect )
        elif self.position == "top":
            screen.blit(button_triangle_green_tiny, self.rect )
        else:
            screen.blit(button_cross_blue_tiny, self.rect )
            
    def reachedPoint( self, x, y ):
        return self.rect.collidepoint( x, y )

    def randomise( self ):
        self.rect.centerx = SCREEN_WIDTH//2
        self.rect.centery = SCREEN_HEIGHT//2
        side = random.randint( 0, 4 )
        if ( side == 0 ):
            self.rect.centery = SCREEN_HEIGHT
            self.position= "bot"
        elif ( side == 1 ):
            self.rect.centery = 0
            self.position= "top"
        elif ( side == 2 ):
            self.rect.centerx = 420
            self.position= "left"
        else:
            self.rect.centerx = SCREEN_WIDTH - 420
            self.position= "right"
        self.calcDirection()

class Circle:

    def __init__(self, x, y, radius=CIRCLE_RADIUS, thick=7, color=BLACK, speed=SPEED, position="top"):

        self.rect = pygame.Rect(0, 0, 2*radius, 2*radius)

        self.rect.centerx = x
        self.rect.centery = y
        self.radius = radius
        self.thick = thick
        self.color = color
        self.speed = speed
        self.position = position

        if speed >= 0:
            self.directionX = 'right'
            self.direction = 'up'
        else:
            self.directionX = 'left'
            self.direction = 'down'

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius, self.thick)

    def swing(self):
        if self.position == "top":
            self.rect.y -= self.speed
            if self.rect.top <= 0  and self.direction == 'up':
                self.direction = 'down'
                self.speed = -self.speed
            elif self.rect.bottom >= int(SCREEN_HEIGHT/2) - self.radius  and self.direction == 'down':
                self.direction = 'up'
                self.speed = -self.speed

        if self.position == "bot":
            self.rect.y -= self.speed
            if self.rect.top <= int(SCREEN_HEIGHT/2) + self.radius  and self.direction == 'up':
                self.direction = 'down'
                self.speed = -self.speed
            elif self.rect.bottom >= SCREEN_HEIGHT and self.direction == 'down':
                self.direction = 'up'
                self.speed = -self.speed
        
        if self.position == "left":
            self.rect.x -= self.speed
            if self.rect.right >= int(SCREEN_WIDTH/2) - self.radius and self.directionX == 'left':
                self.directionX = 'right'
                self.speed = -self.speed
            elif self.rect.left <= 420 and self.directionX == 'right':
                self.directionX = 'left'
                self.speed = -self.speed

        if self.position == "right":
            self.rect.x -= self.speed
            if self.rect.left <= int(SCREEN_WIDTH/2) + self.radius  and self.directionX == 'right':
                self.directionX = 'left'
                self.speed = -self.speed
            elif self.rect.right >= SCREEN_WIDTH - 420 and self.directionX == 'left':
                self.directionX = 'right'
                self.speed = -self.speed

# ---------- Main ----------

def main():

    # Settings
    screen_rect = screen.get_rect()
    game_over = False
    interval = 400
    simultaneity = 4
    pygame.time.set_timer(USEREVENT+1, interval)

   # We create an empty list of enemies, as we want them to drop randomly
    all_enemies = []

    # Start with 4 circles
    all_circles = [
        Circle ( screen_rect.centerx                   , screen_rect.centery - 2*CIRCLE_RADIUS , position = "top"  ),
        Circle ( screen_rect.centerx                   , screen_rect.centery + 2*CIRCLE_RADIUS , position = "bot"  ),
        Circle ( screen_rect.centerx + 2*CIRCLE_RADIUS , screen_rect.centery                   , position = "right"),
        Circle ( screen_rect.centerx - 2*CIRCLE_RADIUS , screen_rect.centery                   , position = "left" )]

    while not game_over:

        screen.fill(WHITE)

        # Circles
        for c in all_circles:
            c.draw(screen)     # Place circles on the screen
            c.swing()          # Move circles from center to edges, and from edges to center, back and forth

        # Enemies
        for e in all_enemies:
            e.draw(screen)          # Place enemies on the screen
            e.update()              # Move enemies from the edges of the screen towards the center

            if ( e.reachedPoint( SCREEN_WIDTH//2, SCREEN_HEIGHT//2 ) ): # If the enemy reaches the middle, you lose a lifepoint and a new enemy is generated
                all_enemies.remove(e)
        
        # Scoring and lifepoints systems
        for event in pygame.event.get():
            
            if event.type == USEREVENT+1 and len(all_enemies) < simultaneity:
                
                all_enemies.append(Enemies(int(SCREEN_WIDTH/2), 0, color = BLACK, position = "top"))
                appended_enemies = [e for e in all_enemies if e.y_float == 0] # Create a filtered list with all enemies at top
                for e in appended_enemies:
                    e.randomise()
       
        pygame.display.update()
        clock.tick(FPS)
            
main()