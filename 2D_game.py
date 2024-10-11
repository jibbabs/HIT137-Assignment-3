#The game should include the following, but not limited to:
#• Player class (movements, speed, jump, health, lives) - Methods
#• Projectile Class (movements, speed, damage) – Methods
#• Enemy Class (……………….) – Methods
#• Collectible Class (health boost, extra life, etc.,)
#• Level Design (3 Levels), Add boss enemy at the end.
#• A Scoring system based on enemies defeated, and collectibles
#collected, health bar for players, and enemies.
#• Implement a game over screen with the option to restart.

# Import the pygame module
import pygame
import pathlib
from pathlib import Path
import sys
import math
from pygame.locals import *
import os
import random
pygame.init()
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
x = 0
y = SCREEN_HEIGHT - 25

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Robot Defender")

char = pygame.image.load('sprites\standing.png')
animationState = pygame.image.load("sprites\standing.png")
bar_width = 200
bar_height = 20
font = pygame.font.Font(None, 36)
SCROLL_THRESH = 100
screen_scroll = 0
LEVEL_WIDTH = 100
bg_scroll = 0
level = 1
#bgX = 0
#bgX2 = bg.get_width()
x = 20
y = 450


clock = pygame.time.Clock()

# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y , width, height):
        super(Player, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 8
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.shooting = False
        self.max_health = 100
        self.current_health = self.max_health
        self.max_lives = 5
        self.current_lives = self.max_lives
        self.bar_width = 200
        self.bar_height = 20
        self.livesfont = pygame.font.Font(None, 36)
        self.walkRight = [pygame.image.load('sprites\walkright1.png'), pygame.image.load('sprites\walkright2.png'), pygame.image.load('sprites\walkright3.png'), pygame.image.load('sprites\walkright4.png'), pygame.image.load('sprites\walkright5.png')]
        self.walkLeft = [pygame.image.load('sprites\walkleft1.png'), pygame.image.load('sprites\walkleft2.png'), pygame.image.load('sprites\walkleft3.png'), pygame.image.load('sprites\walkleft4.png'), pygame.image.load('sprites\walkleft5.png')]
        self.rect = (self.x - 5 ,self.y + 25,self.width-24,self.height -30)
        self.levelstart = True
        self.dimensions = pygame.image.load('sprites\standing.png')
        
        
    # Move the sprite based on keypresses
    def update(self, pressed_keys, pressed_mouse):
        global bulletCount
        if pressed_keys[K_LEFT] and self.x > self.velocity:
            self.x -= self.velocity
            self.left = True
            self.right = False
            self.standing = False
            
            #print(self.x)
        elif pressed_keys[K_RIGHT] and self.x < 800 - self.width - self.velocity:
            self.x += self.velocity
            self.left = False
            self.right = True
            self.standing = False
            
            
        else:
            self.standing = True
            self.walkCount = 0
        self.rect = (self.x - 5 ,self.y + 25,self.width-24,self.height -30)
        pygame.draw.rect(screen, (255,0,0),self.rect, 2) # NEW - Draws rect
          
        if bulletCount > 0:
                bulletCount += 1
        if bulletCount > 3:
                bulletCount = 0
               
        if  pressed_mouse[0] and bulletCount == 0:
            self.shooting = True
                    
            if self.left:
                facing = -1
            else:
                facing = 1
            if len(bullets) < 5:
                bullets.append(projectile(round(self.x + self.width//2), round (self.y + self.height//2), 6, (0,0,0), facing))
                
            bulletCount = 1
                
        if pressed_keys[K_UP]and self.y >= 400:
                self.y -= self.velocity
                self.left = False
                self.right = True
                
        if pressed_keys[K_DOWN] and self.y <= SCREEN_HEIGHT - 80:
                self.y += self.velocity 
                self.left = False
                self.right = True
        
        if not(self.isJump): 
         if pressed_keys[pygame.K_SPACE]:
            self.isJump = True
            self.right = False
            self.left = False
            self.walkCount = 0
             
        else:
            if self.jumpCount >= -10:
                self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5
                self.jumpCount -= 1
            else: 
                self.jumpCount = 10
                self.isJump = False  
                
        #Update scroll based on the player position
        if self.x > SCROLL_THRESH:
            self.levelstart = False
            global screen_scroll
            screen_scroll = 0
        #print(screen_scroll)
        if self.levelstart == False:
            
            if self.x > SCREEN_WIDTH - SCROLL_THRESH - self.velocity:
                self.x -= self.velocity
                screen_scroll = -self.velocity
               
            
            if self.x <= SCROLL_THRESH + self.velocity:
                self.x += self.velocity
                screen_scroll = self.velocity
               
         
            #print(screen_scroll)
            #print(player.x)
        
            return screen_scroll
        
    def draw(self, screen):
        if self.walkCount + 1 >= 15:
            self.walkCount = 0
            
        if (self.shooting):
            if self.left:  
                screen.blit(pygame.image.load('sprites\shootingleft.png'), (self.x -30,self.y))
                self.shooting = False

            else:
                screen.blit(pygame.image.load('sprites\shootingright.png'), (self.x,self.y))
                self.shooting = False
            
        elif not(self.standing):
            if self.left:  # If we are facing left
                screen.blit(self.walkLeft[(self.walkCount//3)], (self.x,self.y))
                self.walkCount += 1                           # image is shown 3 times every animation
            elif self.right:
                screen.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(self.walkRight[0], (self.x, self.y))
            else:
                screen.blit(self.walkLeft[0], (self.x, self.y))
                
    def UI (self, screen):
        # Draw health bar background
        pygame.draw.rect(screen, (100,0,0), (50, 50, bar_width, bar_height))

        # Calculate the width of the current health
        health_ratio = player.current_health / player.max_health
        current_bar_width = bar_width * health_ratio
        
        # Draw current health
        pygame.draw.rect(screen, (0,128,0), (50, 50, current_bar_width, bar_height))
        

        # Display lives
        lives_text = font.render(f"Lives: {player.current_lives}", True, (0, 0, 0))
        screen.blit(lives_text, (50, 100))      
        

class projectile (object):
    def __init__(self, x, y, radius, colour, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.facing = facing
        self.velocity = 12 * facing
    
    def draw (self, screen):
        pygame.draw.circle (screen, self.colour, (self.x, self.y), self.radius)

class collectible (pygame.sprite.Sprite):
    battery_img = pygame.image.load('sprites\health_battery.png').convert_alpha()
    life_img = pygame.image.load('sprites\life.png').convert_alpha()
    gunUpgrade_img = pygame.image.load('sprites\gun_upgrade.png')
    
    global item_boxes
    item_boxes = {
        'Battery': battery_img ,
        'Life': life_img ,
        'Gun_upgrade':gunUpgrade_img 
         }
    
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x 
        self.y = y
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        pygame.draw.rect(screen, (0,100,0),self.rect,1)
        
    def update(self):
        
        #Move with level
        pygame.draw.rect(screen, (0,100,0),self.rect,1)
        if levelOneBG.bgX < 0 and levelOneBG.bgX > -currentLevelWidth:
            if player.x > SCROLL_THRESH + player.velocity:
                self.rect.x += screen_scroll - (screen_scroll//2)
                self.x += screen_scroll - (screen_scroll//2)
                
        #Check if player picks up collectible
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Battery':
                if player.current_health < player.max_health:
                    player.current_health += 20
                
                
            if self.item_type == 'Life':
                if player.current_lives < player.max_lives:
                    player.current_lives += 1
            self.kill()
      

class enemy(pygame.sprite.Sprite):
    
    def __init__(self,enemy_type, x, y, width, height, start, end, speed):
        
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.walkCount = 0
        self.velocity = speed
        self.path = [self.start, self.end]
        self.hitbox = (self.x - 10 ,self.y - 3,self.width,self.height)
        self.enemy_type = enemy_type
        self.rect = self.hitbox
        self.timer = 10
        
        
    def update(self, screen):
    #Level 1 A Type enemy Animation
        if self.enemy_type == 'Level1a':
            self.walkRight = [pygame.image.load('sprites\enemyWR1.png'), pygame.image.load('sprites\enemyWR2.png'), pygame.image.load('sprites\enemyWR3.png'), pygame.image.load('sprites\enemyWR4.png'), pygame.image.load('sprites\enemyWR5.png'), pygame.image.load('sprites\enemyWR6.png')]
            self.walkLeft = [pygame.image.load('sprites\enemyWL1.png'), pygame.image.load('sprites\enemyWL2.png'), pygame.image.load('sprites\enemyWL3.png'), pygame.image.load('sprites\enemyWL4.png'), pygame.image.load('sprites\enemyWL5.png'), pygame.image.load('sprites\enemyWL6.png')]
            if self.walkCount + 1 >= 12:
                self.walkCount = 0
                
            if self.velocity > 0:
                screen.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
                
            else:                
                screen.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
   
            
            
        #Level 1 B Type enemy Animation
        if self.enemy_type == 'Level1b':
            self.walkRight = [pygame.image.load('sprites\enemyWR1.png'), pygame.image.load('sprites\enemyWR2.png'), pygame.image.load('sprites\enemyWR3.png'), pygame.image.load('sprites\enemyWR4.png'), pygame.image.load('sprites\enemyWR5.png'), pygame.image.load('sprites\enemyWR6.png')]
            self.walkLeft = [pygame.image.load('sprites\enemyWL1.png'), pygame.image.load('sprites\enemyWL2.png'), pygame.image.load('sprites\enemyWL3.png'), pygame.image.load('sprites\enemyWL4.png'), pygame.image.load('sprites\enemyWL5.png'), pygame.image.load('sprites\enemyWL6.png')]
            
            if self.walkCount + 1 >= 12:
                self.walkCount = 0
                
            if self.velocity > 0:
                screen.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
                
            else:                
                screen.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            
            self.hitbox = (self.x - 5 ,self.y + 20,self.width,self.height)
            pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)
            
    def move(self):
        #Level 1 a Type enemy Movement
        if self.enemy_type == 'Level1a':
            #Set path for the enemy and adjust with screen scrolling
            if self.path[0] <= self.start and levelOneBG.bgX <= 0 and levelOneBG.bgX > -currentLevelWidth:
                self.path[0] = self.path[0] + screen_scroll
                self.path[1] = self.path[1] + screen_scroll
               
            if self.path[0] > self.start:
                self.path[0] = self.start
                
            if self.path[1] > self.end:
                self.path[1] = self.end
            
            #Enemy movement   
            if self.velocity > 0:
                
                if self.x + self.velocity < self.path[1]:
                    self.x += self.velocity
                    
                    if levelOneBG.bgX > -currentLevelWidth and levelOneBG.bgX < 0:
                        self.x += screen_scroll
                        
                #Turns enemy around
                else:
                    self.velocity = self.velocity * -1 
                    self.walkCount = 0
            else:
                if self.x - self.velocity > self.path[0]:
                    self.x += self.velocity 
                    
                    if levelOneBG.bgX > -currentLevelWidth and levelOneBG.bgX < 0:
                        self.x += screen_scroll
                        
                #Turns enemy around
                else:
                    self.velocity = self.velocity * -1 
                    self.walkCount = 0
            pass
            
            #Collision detection with player
            self.hitbox = (self.x - 5 ,self.y + 20,self.width,self.height)
            pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)
            
            if self.hitbox[1] - self.height < player.rect[1] + player.rect[3] and self.hitbox[1] + self.height > player.rect[1]:
                if self.hitbox[0] + self.width > player.rect[0] and self.hitbox[0] - self.width < player.rect[0] + player.rect[2]:
                    self.timer -= 1
                    print(self.timer)
                    if self.timer <= 0:
                       player.current_health -= 5
                       self.timer = 10
                       
        
        #Level 1 b Type enemy Movement
        if self.enemy_type == 'Level1b':
            #Set path for the enemy and adjust with screen scrolling
            if self.path[0] <= self.start and levelOneBG.bgX <= 0 and levelOneBG.bgX > -currentLevelWidth:
                self.path[0] = self.path[0] + screen_scroll
                self.path[1] = self.path[1] + screen_scroll
               
            if self.path[0] > self.start:
                self.path[0] = self.start
                
            if self.path[1] > self.end:
                self.path[1] = self.end
            
            #Enemy movement   
            if self.velocity > 0:
                
                if self.x + self.velocity < self.path[1]:
                    self.x += self.velocity
                    
                    if levelOneBG.bgX > -currentLevelWidth and levelOneBG.bgX < 0:
                        self.x += screen_scroll
                        
                #Turns enemy around
                else:
                    self.velocity = self.velocity * -1 
                    self.walkCount = 0
            else:
                if self.x - self.velocity > self.path[0]:
                    self.x += self.velocity 
                    
                    if levelOneBG.bgX > -currentLevelWidth and levelOneBG.bgX < 0:
                        self.x += screen_scroll
                        
                #Turns enemy around
                else:
                    self.velocity = self.velocity * -1 
                    self.walkCount = 0
            pass
           
    def hit(self):
        print("Hit!")
        self.kill
        

# Define the cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
            
class level1BG():
    def __init__(self):
        self.bg = pygame.image.load('sprites\image.png')
        self.bgX = 0
        self.bgX2 = self.bg.get_width()
        screen.blit(self.bg, (self.bgX + 1, 0))  
        screen.blit(self.bg, (self.bgX2, 0))
        self.current_Level_Width = 1000
        global currentLevelWidth
        currentLevelWidth = self.current_Level_Width
        
    def update(self, screen):
            
            
            if self.bgX <= 0 and self.bgX >= -self.current_Level_Width and player.x >= SCROLL_THRESH + player.velocity:
                self.bgX += screen_scroll
                self.bgX2 = self.bgX + self.bg.get_width()
                screen.blit(self.bg, (self.bgX , 0))  
                screen.blit(self.bg, (self.bgX2, 0))
            
            if self.bgX >=0:
                self.bgX = 0 
                
            if self.bgX <= -self.current_Level_Width:
                self.bgX = -self.current_Level_Width
        
    
            
                
              
# Setup for sounds, defaults are good
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()



# Create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)


# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
#pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
#pygame.mixer.music.play(loops=-1)

# Load all our sound files
# Sound sources: Jon Fincher
#move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
#move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
#collision_sound = pygame.mixer.Sound("Collision.ogg")

# Set the base volume for all sounds
#move_up_sound.set_volume(0.5)
#move_down_sound.set_volume(0.5)
#collision_sound.set_volume(0.5)

enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
collectibles_group = pygame.sprite.Group()

item_box = collectible('Life', 600, SCREEN_HEIGHT - 150)
collectibles_group.add(item_box)
item_box2 = collectible('Battery', 500, SCREEN_HEIGHT - 50)
collectibles_group.add(item_box2)

player = Player(110, 450, 64, 64)

robotEnemy1 = enemy('Level1a', 450, SCREEN_HEIGHT - 150, 30, 40, 400, 500, 1) 
robotEnemy2 = enemy('Level1b', 1500, SCREEN_HEIGHT - 200, 30, 40, 600, 700, 1) 
robotEnemy3 = enemy('Level1a', 1800, SCREEN_HEIGHT - 100, 64, 64, 1500, 1800, 1) 
robotEnemy4 = enemy('Level1b', 1200, SCREEN_HEIGHT - 100, 64, 64, 1000, 1100, 8) 
enemy_group.add(robotEnemy1)
enemy_group.add(robotEnemy2)
enemy_group.add(robotEnemy3)
enemy_group.add(robotEnemy4)

levelOneBG = level1BG()
bulletCount = 0

def drawBG():
    levelOneBG.update(screen)

    pygame.draw.rect(screen, (95,102,112), (0, 450, 800, 350))

def drawGameWindow():
    
    
    pressed_keys = pygame.key.get_pressed()
    pressed_mouse = pygame.mouse.get_pressed()
    player.update(pressed_keys, pressed_mouse)
    player.draw(screen)
    player.UI(screen)
    
 
    for enemy in enemy_group:
        enemy.update(screen)
        enemy.move()
        
    collectibles_group.update()
    collectibles_group.draw(screen)
    
    for items in collectibles_group:
        items.update()
    
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.update()
    
speed = 60
bullets = []
enemies = []

run = True
#main loop
while run:
    drawBG()
    drawGameWindow()
    pressed_keys = pygame.key.get_pressed()
    pressed_mouse = pygame.mouse.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    #Checking if bullet is in enemy hitbox
    for enemy in enemy_group:
        for bullet in bullets:
            if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
                if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                    enemy.hit()
                    bullets.pop(bullets.index(bullet))
                    
            if bullet.x < 800 and bullet.x > 0:
                bullet.x += bullet.velocity
            else:
                bullets.pop(bullets.index(bullet))
                
    # Did the user hit a key?
    if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
        if event.key == K_ESCAPE:
                run = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            run = False

        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Should we add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud, and add it to our sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # Get the set of keys pressed and check for user input
    
    

    # Check if any enemies have collided with the player
    #if pygame.sprite.spritecollideany(player, enemies):
        # If so, remove the player
        #player.kill()

        # Stop any moving sounds and play the collision sound
        #move_up_sound.stop()
        #move_down_sound.stop()
        #collision_sound.play()

        # Stop the loop
        #running = False

    # Flip everything to the display
    pygame.display.update()
    
    # Ensure we maintain a 30 frames per second rate
    clock.tick(30)

# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()