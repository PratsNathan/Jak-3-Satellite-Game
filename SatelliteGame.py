# ---------- Packages and Inits ----------
import pygame
from pygame.locals import *
pygame.init()

# ---------- Settings ----------

SCREEN_WIDTH  = 1920
SCREEN_HEIGHT = 1080
FPS = 60
CIRCLE_RADIUS = 70
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
SPEED = 2

# ---------- Resources (Colors) ----------
BLACK  = (000,000,000)
WHITE  = (255,255,255)

# ---------- Classes ----------

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
       
        pygame.display.update()
        clock.tick(FPS)
            
main()