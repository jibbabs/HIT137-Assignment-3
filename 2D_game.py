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

# Import random for random numbers
import random

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
pygame.display.set_caption("Robot Defender")
walkState = 0
walkRight = [pygame.image.load('sprites\walkright1.png'), pygame.image.load('sprites\walkright2.png'), pygame.image.load('sprites\walkright3.png'), pygame.image.load('sprites\walkright4.png'), pygame.image.load('sprites\walkright5.png')]
walkLeft = [pygame.image.load('sprites\walkleft1.png'), pygame.image.load('sprites\walkleft2.png'), pygame.image.load('sprites\walkleft3.png'), pygame.image.load('sprites\walkleft4.png'), pygame.image.load('sprites\walkleft5.png')]
bg = pygame.image.load('sprites\image.png')
char = pygame.image.load('sprites\standing.png')
animationState = pygame.image.load("sprites\standing.png")

clock = pygame.time.Clock()

# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y , width, height):
        super(Player, self).__init__()
        self.x = 40
        self.y = SCREEN_HEIGHT - 80
        self.width = width
        self.height = height
        self.velocity = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.shooting = False

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
      
        if pressed_keys[K_LEFT] and self.x > self.velocity:
            self.x -= self.velocity
            self.left = True
            self.right = False
            self.standing = False
        
        elif pressed_keys[K_RIGHT] and self.x < 800 - self.width - self.velocity:
            self.x += self.velocity
            self.left = False
            self.right = True
            self.standing = False
        else:
            self.standing = True
            self.walkCount = 0
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.shooting = True
            if self.left:
                facing = -1
            else:
                facing = 1
            if len(bullets) < 5:
                bullets.append(projectile(round(self.x + self.width//2), round (self.y + self.height//2), 6, (0,0,0), facing))
                
            
        
        if pressed_keys[K_UP]and self.y >= 400:
                self.y -= self.velocity
                self.left = False
                self.right = True
                
        if pressed_keys[K_DOWN] and self.y <= SCREEN_HEIGHT - 80:
                self.y += self.velocity 
                self.left = False
                self.right = True
        
        if not(self.isJump): 
         if keys[pygame.K_SPACE]:
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

        # Keep player on the screen
        
    def charAnimation(self, screen):
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
                screen.blit(walkLeft[(self.walkCount//3)], (self.x,self.y))
                self.walkCount += 1                           # image is shown 3 times every animation
            elif self.right:
                screen.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))
                   
        

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
        
# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


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


# Setup for sounds, defaults are good
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Create our 'player'
player = Player(300, 410, 64, 64)

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
#pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
#pygame.mixer.music.play(loops=-1)

# Load all our sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

# Set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)

# Variable to keep our main loop running
def drawGameWindow():
    screen.blit(bg,(0,0))
    player.charAnimation(screen)
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.update()

run = True
bullets = []
#main loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    
    for bullet in bullets:
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
    pressed_keys = pygame.key.get_pressed()
    pressed_mouse = pygame.mouse.get_pressed()
    player.update(pressed_keys)

    # Update the position of our enemies and clouds
    enemies.update()
    clouds.update()


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
    drawGameWindow()
    # Ensure we maintain a 30 frames per second rate
    clock.tick(30)

# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()