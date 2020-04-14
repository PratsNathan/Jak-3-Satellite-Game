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
SPEED = 2
CIRCLE_RADIUS = 70
ENEMY_SIZE = 40
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pause = False
over = False
myFont = pygame.font.SysFont("monospace", 25 , bold = True)

# ---------- Resources (Images & Sounds) ----------

if getattr(sys, 'frozen', False):
    current_path = os.path.dirname(sys.executable)
else:
    current_path = os.path.dirname(os.path.realpath(__file__))

# Background Images
background_image_Start = pygame.image.load(os.path.join(current_path,"Start.jpg")).convert()
background_image_Pause =  pygame.image.load(os.path.join(current_path,"Pause.jpg")).convert()
background_image_Game_Over = pygame.image.load(os.path.join(current_path,"Over.jpg")).convert()
background_image_In_Game =  pygame.image.load(os.path.join(current_path,"InGame.png")).convert()

# Sounds
Re5HealingSoundEffect = pygame.mixer.Sound('Re5HealingSoundEffect.wav')
Halo3Deaths1 = pygame.mixer.Sound('Halo3Deaths1.wav')

# PS2 images
button_circle_red_tiny = pygame.image.load('button_circle_red_tiny.png').convert()
button_square_pink_tiny = pygame.image.load('button_square_pink_tiny.png').convert()
button_triangle_green_tiny = pygame.image.load('button_triangle_green_tiny.png').convert()
button_cross_blue_tiny = pygame.image.load('button_cross_blue_tiny.png').convert()

# ---------- Resources (Colors) ----------
RED    = (255,000,000)
BLUE   = (000,000,255)
YELLOW = (255,255,000)
GREEN  = (000,128,000)
BLACK  = (000,000,000)
WHITE  = (255,255,255)
LIGHT_GREEN = (144,238,144)
LIGHT_RED = (255,0,128)

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

    def set_speed( self, difficulty):
        if   difficulty == 1 : self.speed = 2
        elif difficulty == 2 : self.speed = 2.25
        elif difficulty == 3 : self.speed = 2.5
        elif difficulty == 4 : self.speed = 2.75
        elif difficulty == 5 : self.speed = 3
        elif difficulty == 6 : self.speed = 3.25
        return self.speed

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
    
    def isCollision(self, enemyX, enemyY, circleX, circleY):
        distance = math.sqrt((math.pow(enemyX-circleX,2))+(math.pow(enemyY-circleY,2)))
        if distance < (CIRCLE_RADIUS+ENEMY_SIZE//2): 
            return True
        else:
            return False

# ---------- Other Functions ----------

""" Difficulty sets 4 variables :
        enemy speed (in enemy class)
        interval between enemy drops 
        maximum number of enemies drop in a row from the same lane 
        simultaneity (drops at the same time from different lanes)"""

def set_difficulty(score):  
    if   score < 25 : difficulty = 1
    elif score < 50 : difficulty = 2
    elif score < 100: difficulty = 3
    elif score < 250: difficulty = 4
    elif score < 500: difficulty = 5
    else:             difficulty = 6

    return difficulty

def set_interval(difficulty):
    if   difficulty == 1 : interval = 400
    elif difficulty == 2 : interval = 250
    elif difficulty == 3 : interval = 200
    elif difficulty == 4 : interval = 150
    elif difficulty == 5 : interval = 100
    elif difficulty == 6 : interval = 75

    return interval

def set_simultaneity(difficulty):
    if   difficulty == 1 : simultaneity = 3
    elif difficulty == 2 : simultaneity = 4
    elif difficulty == 3 : simultaneity = 5
    else                 : simultaneity = 6

    return simultaneity

# ---------- Welcome screen / Pause / Game Over ----------

def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def game_intro():

    intro = True
    
    # Music
    pygame.mixer.music.load('in_game.ogg')
    pygame.mixer.music.play()

    over == False

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            

        screen.blit(background_image_Start, [0, 0])

        button("Go !",700,700,100,50,GREEN,LIGHT_GREEN,main)
        button("Quit",1200,700,100,50,RED,LIGHT_RED,quit_game)

        print_myself = myFont.render("A game developed by : Nathan PRATS", 1, WHITE)
        screen.blit(print_myself, (10, 1050))

        pygame.display.update()
        clock.tick(15)

def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False

def paused():

    pygame.mixer.music.pause()
    screen.blit(background_image_Pause, [0, 0])
    largeText = pygame.font.SysFont("comicsansms",50)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = (380,200)
    screen.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: 
                    unpause()

                if event.key == pygame.K_a:
                    pygame.quit()
                        
        button("Continue",150,300,100,50,GREEN,LIGHT_GREEN,unpause)
        button("Quit",500,300,100,50,RED,LIGHT_RED,quit_game)

        pygame.display.update()
        clock.tick(15) 

def quit_game():
    pygame.quit()

# ---------- Main ----------

def main():

    global pause

    # Settings
    screen_rect = screen.get_rect()
    game_over = False
    score = 0
    lifes = 5
    difficulty = set_difficulty(score)
    interval = set_interval(difficulty)
    pygame.time.set_timer(USEREVENT+1, interval)

    # We create an empty list of enemies, as we want them to drop randomly
    all_enemies = []

    # Music
    music_end = pygame.USEREVENT+2
    pygame.mixer.music.set_endevent(music_end)
    pygame.mixer.music.load('in_game.ogg')
    pygame.mixer.music.play()

    # Start with 4 circles
    all_circles = [
        Circle ( screen_rect.centerx                   , screen_rect.centery - 2*CIRCLE_RADIUS , position = "top"  ),
        Circle ( screen_rect.centerx                   , screen_rect.centery + 2*CIRCLE_RADIUS , position = "bot"  ),
        Circle ( screen_rect.centerx + 2*CIRCLE_RADIUS , screen_rect.centery                   , position = "right"),
        Circle ( screen_rect.centerx - 2*CIRCLE_RADIUS , screen_rect.centery                   , position = "left" )]

    while not game_over:

        screen.blit(background_image_In_Game, [0, 0]) 

        # Variables
        difficulty = set_difficulty(score)
        interval = set_interval(difficulty)
        simultaneity = set_simultaneity(difficulty)

        # Circles
        for c in all_circles:
            c.draw(screen)     # Place circles on the screen
            c.swing()          # Move circles from center to edges, and from edges to center, back and forth

        # Enemies
        for e in all_enemies:
            e.draw(screen)          # Place enemies on the screen
            e.set_speed(difficulty) # Set speed difficulty for enemies
            e.update()              # Move enemies from the edges of the screen towards the center

            if ( e.reachedPoint( SCREEN_WIDTH//2, SCREEN_HEIGHT//2 ) ): # If the enemy reaches the middle, you lose a lifepoint and a new enemy is generated
                lifes -=1
                all_enemies.remove(e)

        # Scoring and lifepoints systems
        for event in pygame.event.get():

            # Music 
            if event.type == music_end:
                pygame.mixer.music.load('Halo3OneFinalEffort.mp3')
                pygame.mixer.music.play()

            # Allow Pause and Quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                if event.key == pygame.K_a:
                    quit_game()

            # Cheats
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g: 
                    pygame.mixer.Sound.play(Re5HealingSoundEffect)
                    lifes += 5
                if event.key == pygame.K_t: 
                    score -= 100

            if event.type == USEREVENT+1 and len(all_enemies) < simultaneity:
                
                all_enemies.append(Enemies(int(SCREEN_WIDTH/2), 0, color = YELLOW, position = "top"))
                appended_enemies = [e for e in all_enemies if e.y_float == 0] # Create a filtered list with all enemies at top
                for e in appended_enemies:
                    e.randomise()
        
            for c in all_circles:

                if event.type == pygame.KEYDOWN:

                    # LEFT
                    if event.key == pygame.K_LEFT and c.position == "left":
                        hits = [e for e in all_enemies if c.isCollision(e.rect.centerx,e.rect.centery,c.rect.centerx,c.rect.centery)]
                        if not hits:
                            lifes -=1
                        for e in hits:
                            if len(hits) == 1: 
                                score +=1
                            if len(hits) == 2: 
                                score +=5/len(hits)
                            if len(hits) == 3: 
                                score +=10/len(hits)
                            all_enemies.remove(e)
                    
                    # RIGHT
                    if event.key == pygame.K_RIGHT and c.position == "right":
                        hits = [e for e in all_enemies if c.isCollision(e.rect.centerx,e.rect.centery,c.rect.centerx,c.rect.centery)]
                        if not hits:
                            lifes -=1
                        for e in hits:
                            if len(hits) == 1: 
                                score +=1
                            if len(hits) == 2: 
                                score +=5/len(hits)
                            if len(hits) == 3: 
                                score +=10/len(hits)
                            all_enemies.remove(e)
                    
                    # TOP
                    if event.key == pygame.K_UP and c.position == "top":
                        hits = [e for e in all_enemies if c.isCollision(e.rect.centerx,e.rect.centery,c.rect.centerx,c.rect.centery)]
                        if not hits:
                            lifes -=1
                        for e in hits:
                            if len(hits) == 1: 
                                score +=1
                            if len(hits) == 2: 
                                score +=5/len(hits)
                            if len(hits) == 3: 
                                score +=10/len(hits)
                            all_enemies.remove(e)
                    
                    # BOT
                    if event.key == pygame.K_DOWN and c.position == "bot":
                        hits = [e for e in all_enemies if c.isCollision(e.rect.centerx,e.rect.centery,c.rect.centerx,c.rect.centery)]
                        if not hits:
                            lifes -=1
                        for e in hits:
                            if len(hits) == 1: 
                                score +=1
                            if len(hits) == 2: 
                                score +=5/len(hits)
                            if len(hits) == 3: 
                                score +=10/len(hits)
                            all_enemies.remove(e)

        # Game Over condition
        if lifes < 0:
            pygame.mixer.Sound.play(Halo3Deaths1)
            you_lose()
            
        next_level = 25
        if difficulty == 2 : next_level = 50
        elif difficulty == 3 : next_level = 100
        elif difficulty == 4 : next_level = 250
        elif difficulty == 5 : next_level = 500
        elif difficulty == 6 : next_level = 1000
        
        # Score / Lifes / Number of Enemies / Next Level
        place_text = SCREEN_WIDTH-250
        print_lifes = myFont.render("Lifes:" + str(round(lifes)), 1, BLACK)
        screen.blit(print_lifes, (place_text, 10))

        print_score = myFont.render("Score:" + str(round(score)), 1, BLACK)
        screen.blit(print_score, (place_text, 50))

        print_next_level = myFont.render("Next Level:" + str(round(next_level)), 1, BLACK)
        screen.blit(print_next_level, (place_text, 90))

        pygame.display.update()
        clock.tick(FPS)
            
    
def you_lose():

    global over
    over = True

    pygame.mixer.music.load(os.path.join(current_path,"Re5DreamyLoops.mp3"))
    pygame.mixer.music.play(-1)

    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(background_image_Game_Over, [0, 0])

        y = SCREEN_HEIGHT-100
        button("Retry !",1200,y,100,50,GREEN,LIGHT_GREEN,main)
        button("Menu",1350,y,100,50,BLUE,LIGHT_GREEN,game_intro)
        button("Quit",1500,y,100,50,RED,LIGHT_RED,quit_game)

        print_myself = myFont.render("A game developed by : Nathan PRATS", 1, WHITE)
        screen.blit(print_myself, (10, 1050))

        pygame.display.update()
        clock.tick(15)

game_intro()