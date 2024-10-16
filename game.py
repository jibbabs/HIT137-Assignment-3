#Group Name: CAS003
#Group Members:
#[Alex Tarrant] - [S255441]
#[Jason Yun] - [S364369]
#GitHub Repository: https://github.com/yourusername/yourrepository

#Sprites courtesy of CRAFTPIX.NET
# Import the pygame module and math
import pygame
import math
from pygame.locals import *
print("WELCOME TO JOHN JONE: CITY DEFENDER")
#Initialize pygame and mixer for soundtrack
pygame.init()
pygame.mixer.init()  

#Soundtrack by Evgeny Bardyuzha from Pixabay
soundtrack = pygame.mixer.music.load("password-infinity-123276.mp3")

pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.2)

#Sound Effect by mrfriends from Pixabay
gunshot = pygame.mixer.Sound("pistol-shot-233473.mp3")
gunshot.set_volume(0.2)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Define starting position for player on screen
startPos = (110,480)

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("JOHN JONE: CITY DEFENDER")

#Create the highscore variable
highScore = 0

#Define game constants
font = pygame.font.Font(None, 36)
SCROLL_THRESH = 100
screen_scroll = 0
LEVEL_WIDTH = 100
bg_scroll = 0

global finishLevelText
finishLevelText = False

#Create lists for several game objects
speed = 60
bullets = []
enemyBullets = []
enemies = []

#Create game clock
clock = pygame.time.Clock()

# Define the Player object 
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y , width, height, ):
        super(Player, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 4
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.shooting = False
        self.max_health = 20
        self.current_health = self.max_health
        self.max_lives = 2
        self.current_lives = self.max_lives
        self.bar_width = 200
        self.bar_height = 20
        self.livesfont = pygame.font.Font(None, 36)
        self.walkRight = [pygame.image.load('sprites\walkright1.png'), pygame.image.load('sprites\walkright2.png'), pygame.image.load('sprites\walkright3.png'), pygame.image.load('sprites\walkright4.png'), pygame.image.load('sprites\walkright5.png'),pygame.image.load('sprites\walkright6.png'),pygame.image.load('sprites\walkright7.png'),pygame.image.load('sprites\walkright8.png')]
        self.walkLeft = [pygame.image.load('sprites\walkleft1.png'), pygame.image.load('sprites\walkleft2.png'), pygame.image.load('sprites\walkleft3.png'), pygame.image.load('sprites\walkleft4.png'), pygame.image.load('sprites\walkleft5.png'), pygame.image.load('sprites\walkleft6.png'), pygame.image.load('sprites\walkleft7.png'), pygame.image.load('sprites\walkleft8.png')]
        self.rect = (self.x,self.y,self.width,self.height)
        self.levelstart = True
        self.dimensions = pygame.image.load('sprites\standing.png')
        self.gunLvl = 0
        self.bulletLim = 10
        self.bulletSpeed = 7
        self.shotTimer = 0
        self.shotSpeed = 25
        self.bulletSize = 3
        self.bulletDmg = 3
        self.playerDead = False
        self.bar_width = 200
        self.bar_height = 20
        self.score = 0
        
        
        
    # Move the sprite based on keypresses
    def update(self, pressed_keys, pressed_mouse):
        global bulletCount
        global undercollision
        global uppercollision
        global leftcollision
        global rightcollision
        global highScore
        self.bulletColour = collectible.bulletColours[self.gunLvl]
        
        if self.score > highScore:
            highScore = self.score
        
        if pressed_keys[K_LEFT] and self.x > self.velocity and self.playerDead != True:
            self.x -= self.velocity
            self.left = True
            self.right = False
            self.standing = False
            leftcollision = False
            
            
        elif pressed_keys[K_RIGHT] and self.x < 800 - self.width - self.velocity and self.playerDead != True:
            self.x += self.velocity
            self.left = False
            self.right = True
            self.standing = False
            rightcollision = False
            
            
        else:
            self.standing = True
            self.walkCount = 0
            
            
        self.rect = (self.x - 5 ,self.y  ,self.width-24,self.height - 20)
        
          
        if bulletCount > 0:
                bulletCount += 1
        if bulletCount > 3:
                bulletCount = 0
        
        if self.shotTimer <= 0:       
            if  pressed_mouse[0] and bulletCount == 0:
                self.shooting = True
                        
                if self.left:
                    facing = -1
                else:
                    facing = 1
                if self.shotTimer <= 0:
                    if len(bullets) < self.bulletLim:
                        bullets.append(projectile(round(self.x + 65 *facing), round (self.y + 19 ), self.bulletSize, self.bulletColour, facing, self.bulletSpeed))
                        self.shotTimer = self.shotSpeed
                        gunshot.play()
                       
        else:
            self.shotTimer -= 1    
            bulletCount = 1
                
        if pressed_keys[K_UP]and self.y >= 400  and self.playerDead != True:
                self.y -= self.velocity
                self.left = False
                self.right = True
                uppercollision = False
                
        if pressed_keys[K_DOWN] and self.y <= SCREEN_HEIGHT - 80  and self.playerDead != True:
                self.y += self.velocity 
                self.left = False
                self.right = True
                undercollision = False
        
        
             
                
        #Determine amount of screen scroll based on the player position
        if self.x > SCROLL_THRESH:
            self.levelstart = False
            global screen_scroll
            screen_scroll = 0
       
        if self.levelstart == False:
            
            if self.x > SCREEN_WIDTH - SCROLL_THRESH - self.velocity - 400:
                self.x -= self.velocity
                screen_scroll = -self.velocity
               
            
            if self.x <= SCROLL_THRESH + self.velocity:
                self.x += self.velocity
                screen_scroll = self.velocity
        
            return screen_scroll
   
    #Draw player on screen  and animation 
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
            if self.left:  
                screen.blit(self.walkLeft[(self.walkCount//2)], (self.x,self.y))
                self.walkCount += 1                          
            elif self.right:
                screen.blit(self.walkRight[self.walkCount//2], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(self.walkRight[0], (self.x, self.y))
            else:
                screen.blit(self.walkRight[0], (self.x, self.y))
    
    #User Interface           
    def UI (self, screen):
        #Draw health bar background
        pygame.draw.rect(screen, (100,0,0), (50, 50, self.bar_width, self.bar_height))

        #Calculate the width of the current health
        health_ratio = self.current_health / self.max_health
        current_bar_width = self.bar_width * health_ratio
        
        #Draw current health
        pygame.draw.rect(screen, (0,128,0), (50, 50, current_bar_width, self.bar_height))
        

        #Display lives
        lives_text = font.render(f"LIVES: {self.current_lives}", True, (0, 0, 0))
        screen.blit(lives_text, (50, 80))      
        
        #Display score
        score_text = font.render(f"SCORE: {self.score}", True, (0, 0, 0))
        screen.blit(score_text, (SCREEN_WIDTH - 200, 50))   
        
        #Display gun level
        score_text = font.render(f"GUN LVL: {self.gunLvl}", True, (0, 0, 0))
        screen.blit(score_text, (SCREEN_WIDTH - 200, 80))   
    
    #Function for player damage 
    def hit(self):
        if self.current_health > 0:
            self.current_health -= 5
            
        if self.current_health <= 0 and self.current_lives > 0:
            self.current_lives -= 1
            self.x, self.y = startPos
            self.current_health = self.max_health
                

    #Function for if player dies    
    def die(self):
        global menu
        global gameRun
        global restart
        gameover_text = font.render("GAME OVER", True, (237, 237, 237))
        gameover_text2 = font.render("Press BACKSPACE to return to menu", True, (237, 237, 237))
        gameover_text3 = font.render("or press SPACE to restart", True, (237, 237, 237))
        pygame.draw.rect(screen, (100,100,100), (150, 280, 475, 140))
        screen.blit(gameover_text, (315, SCREEN_HEIGHT/2))
        screen.blit(gameover_text2, (175, SCREEN_HEIGHT/2 + 35))
        screen.blit(gameover_text3, (240, SCREEN_HEIGHT/2 + 70))
        self.playerDead = True
        if pressed_keys[K_BACKSPACE]: 
            menu = True   
            gameRun = False 
            
           
        if pressed_keys[K_SPACE]:
            player.current_health = player.max_health
            player.current_lives = player.max_lives
            restart = True
            
#Class for game projectiles, such as bullets
class projectile (object):
    def __init__(self, x, y, radius, colour, facing, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.facing = facing
        self.velocity = speed * facing
    
    def draw (self, screen):
        pygame.draw.circle (screen, self.colour, (self.x, self.y), self.radius)
        
#Class for game collectibles, such as health and upgrades
class collectible (pygame.sprite.Sprite):
    medpack_img = pygame.image.load('sprites\medpack.png').convert_alpha()
    life_img = pygame.image.load('sprites\life.png').convert_alpha()
    gunUpgrade_img = pygame.image.load('sprites\gun_upgrade.png')
    bulletColours = [
        (237,215,36), #Yellow
        (20,237,34), #Green
        (45,65,237), #Blue
        (237,30,187), #Purple
        (237,2,6), #Red
        ]
    
    item_boxes = {
        'Medpack': medpack_img ,
        'Life': life_img ,
        'Gun_upgrade':gunUpgrade_img 
         }
    
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x 
        self.y = y
        self.item_type = item_type
        self.image = collectible.item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        #pygame.draw.rect(screen, (0,100,0),self.rect,1)
       
    #Update collectible position on screen when screen moves    
    def update(self):
        
        #Move with level
        if currentLevel.bgX < 0 and currentLevel.bgX > -currentLevel.current_Level_Width:
            if player.x > SCROLL_THRESH + player.velocity:
                self.rect.x += screen_scroll - (screen_scroll//2)
                self.x += screen_scroll - (screen_scroll//2)
                
        #Check if player picks up collectible
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Medpack':
                if player.current_health < player.max_health:
                    player.current_health += 5
                if player.current_health > player.max_health:
                    player.current_health = player.max_health
            self.kill()        
          
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Gun_upgrade':
                if player.gunLvl < 4:
                    player.gunLvl += 1
                player.bulletLim += 1
                player.bulletSpeed += 1
                player.shotSpeed -= 2
                player.bulletSize += 1
                player.bulletDmg += 1
                
            self.kill()        
                
#Class for game obstacles in the environment
class obstacle (pygame.sprite.Sprite):
    burntCar = pygame.image.load('sprites\car1.png').convert_alpha()
    rustyCar = pygame.image.load('sprites\car2.png').convert_alpha()
    scooter = pygame.image.load('sprites\scooter.png').convert_alpha()
    millitary_v = pygame.image.load('sprites\millitaryvehicle.png').convert_alpha()
    jeep = pygame.image.load('sprites\jeep.png').convert_alpha()
    tank = pygame.image.load('sprites\mtank.png').convert_alpha()
    
    rubbish_img1 = pygame.image.load('sprites\grubbish.png').convert_alpha()
    rubbish_img2 = pygame.image.load('sprites\grubbish2.png').convert_alpha()
    rubbish_img3 = pygame.image.load('sprites\grubbish3.png').convert_alpha()
    rubbish_img4 = pygame.image.load('sprites\grubbish4.png').convert_alpha()
    street_lamp = pygame.image.load('sprites\streetlamp.png').convert_alpha()
    level1_text1 = font.render("Use the ARROW KEYS to move.", True, (255, 255, 255))
    level1_text2 = font.render("Press LEFT MOUSE BUTTON to shoot", True, (255, 255, 255))
    level1_text3 = font.render("Destroy all ENEMIES to proceed. Goodluck..", True, (255, 255, 255))
    next_leveltxt = font.render("Nice work. Press ENTER to proceed to next level.", True, (255, 255, 255))
    
    global world_Obstacles
    world_Obstacles = {
        'Burnt_car': burntCar ,
        'Rusty_car': rustyCar ,
        'Scooter': scooter ,
        'Millitary vehicle': millitary_v,
        'Jeep': jeep,
        'Tank': tank,
        'Rubbish1': rubbish_img1 ,
        'Rubbish2': rubbish_img2 ,
        'Rubbish3': rubbish_img3 ,
        'Rubbish4': rubbish_img4 ,
        'streetlamp': street_lamp ,
        'Level1text': level1_text1 ,
        'Level1text2': level1_text2,
        'Level1text3': level1_text3,
        'nextLevelText': next_leveltxt
         }
    
    def __init__(self, obs_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x 
        self.y = y
        self.obs_type = obs_type
        self.image = world_Obstacles[self.obs_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        self.behind = True
        
    def update(self):
        
        #Obstacles move with level
        if currentLevel.bgX < 0 and currentLevel.bgX > -currentLevel.current_Level_Width:
            if player.x > SCROLL_THRESH + player.velocity:
                self.rect.x += screen_scroll/2
                self.x += screen_scroll /2
         
#Class for game enemies with multiple enemy types                   
class enemy(pygame.sprite.Sprite):
    def __init__(self,enemy_type, x, y, xadj, yadj, width, height, start, end):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.x = x
        self.y = y
        self.xadj = xadj
        self.yadj = yadj
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.walkCount = 0
        self.path = [self.start, self.end]
        self.ebullets = []
        self.hitbox = (self.x - 10 ,self.y - 3,self.width,self.height)
        self.enemy_type = enemy_type
        self.rect = self.hitbox
        self.timerMax = 20
        self.timer = self.timerMax
        self.spriteCollision = False
        self.aggro = False
        self.left = False
        self.right = False
        self.enemySel = self.enemy_type
        if self.enemy_type == 'enemyA':
            self.enemyA()
        if self.enemy_type == 'enemyB':
            self.enemyB()
        if self.enemy_type == 'enemyBoss':
            self.enemyBoss() 
        
    def enemyA(self):
        self.velocity = 1
        self.walkRight = [pygame.image.load('sprites\enemyWR1.png'), pygame.image.load('sprites\enemyWR2.png'), pygame.image.load('sprites\enemyWR3.png'), pygame.image.load('sprites\enemyWR4.png'), pygame.image.load('sprites\enemyWR5.png'), pygame.image.load('sprites\enemyWR6.png')]
        self.walkLeft = [pygame.image.load('sprites\enemyWL1.png'), pygame.image.load('sprites\enemyWL2.png'), pygame.image.load('sprites\enemyWL3.png'), pygame.image.load('sprites\enemyWL4.png'), pygame.image.load('sprites\enemyWL5.png'), pygame.image.load('sprites\enemyWL6.png')]
        self.shootingR = pygame.image.load('sprites\shooting.png')
        self.shootingL = pygame.image.load('sprites\shootingL.png')
        self.facing = 1
        self.bulletLim = 2
        self.bulletColour = (234,237,211)
        self.range = 350
        self.bulletSpeed = 4
        self.health = 10
        self.currentHealth = self.health
        self.bar_width = 50
        self.bar_height = 3
        self.healthx = -10
        self.healthy = -15
        self.bulletx = 20
        self.bullety = 18
        self.followR = False
        self.followL = False
        
        self.shotPause = 20
        self.shotTimer = self.shotPause
        
    def enemyB(self):
        self.velocity = 3
        self.walkRight = [pygame.image.load('sprites\enemyBWR1.png'), pygame.image.load('sprites\enemyBWR2.png'), pygame.image.load('sprites\enemyBWR3.png'), pygame.image.load('sprites\enemyBWR4.png'), pygame.image.load('sprites\enemyBWR5.png'), pygame.image.load('sprites\enemyBWR6.png')]
        self.walkLeft = [pygame.image.load('sprites\enemyBWL1.png'), pygame.image.load('sprites\enemyBWL2.png'), pygame.image.load('sprites\enemyBWL3.png'), pygame.image.load('sprites\enemyBWL4.png'), pygame.image.load('sprites\enemyBWL5.png'), pygame.image.load('sprites\enemyBWL6.png')]
        self.shootingR = pygame.image.load('sprites\shootingB.png')
        self.shootingL = pygame.image.load('sprites\shootingBL.png')
        self.facing = 1
        self.bulletLim = 2
        self.bulletColour = (234,237,211)
        self.range = 500
        self.bulletSpeed = 4
        self.health = 6
        self.currentHealth = self.health
        self.bar_width = 50
        self.bar_height = 3
        self.healthx = -10
        self.healthy = -15
        self.bulletx = 20
        self.bullety = 18
        self.followR = False
        self.followL = False
        self.timerMax = 50
        self.timer = self.timerMax
        self.shotPause = 20
        self.shotTimer = self.shotPause
        
    def enemyBoss(self):
        self.velocity = 1
        self.walkLeft = [pygame.image.load('sprites\ebossLW.png'), pygame.image.load('sprites\ebossLW2.png'), pygame.image.load('sprites\ebossLW.png'),pygame.image.load('sprites\ebossLW2.png'),pygame.image.load('sprites\ebossLW.png'),pygame.image.load('sprites\ebossLW2.png'), ]
        self.walkRight = [pygame.image.load('sprites\ebossLW.png'), pygame.image.load('sprites\ebossLW2.png'), pygame.image.load('sprites\ebossLW.png'),pygame.image.load('sprites\ebossLW2.png'),pygame.image.load('sprites\ebossLW.png'),pygame.image.load('sprites\ebossLW2.png'), ]
        self.shootingR = pygame.image.load('sprites\ebossshooting.png')
        self.shootingL = pygame.image.load('sprites\ebossLW.png')
        self.facing = 1
        self.bulletLim = 6
        self.bulletColour = (9,242,194)
        self.range = 600
        self.bulletSpeed = 6
        self.health = 200
        self.currentHealth = self.health
        self.bar_width = 120
        self.bar_height = 10
        self.healthx = 5
        self.healthy = -25
        self.bulletx = 20
        self.bullety = 18
        self.followR = False
        self.followL = False
        
        self.shotPause = 20
        self.shotTimer = self.shotPause   
              
    def update(self, screen):
        #Pauses enemy movement if shooting
        if self.shotTimer < self.shotPause:
            if self.followR == True:
                screen.blit(self.shootingR, (self.x, self.y))
                
            else:
                screen.blit(self.shootingL, (self.x, self.y))
                
        #Enemy following player animation
        else:     
            if self.followR == True or self.followL == True:
                if self.followR == True: 
                    screen.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                    self.walkCount += 1
                
                
                if self.followL == True:   
                    screen.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                    self.walkCount += 1
                    
            else:  
                if self.velocity > 0:
                    screen.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                    self.walkCount += 1
                    
                    
                if self.velocity < 0 :            
                    screen.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                    self.walkCount += 1
            
        if self.walkCount >= 18:
            self.walkCount = 0   
              
       
        if player.x > self.x:
                self.facing = 1
        else:
            self.facing = -1
        
        #Enemy shooting   
        self.bulletx = self.bulletx * self.facing
        if self.shotTimer == self.shotPause:
            if player.x < self.x + self.range and player.x > self.x - self.range:
                if self.enemy_type == 'enemyA':
                    if len(self.ebullets) < self.bulletLim:
                        self.ebullets.append(projectile(round((self.x + 30 * self.facing ) + self.bulletx), round (self.y + self.bullety), 4, self.bulletColour, self.facing, self.bulletSpeed))
                        self.shotTimer -= 1
                       
                if self.enemy_type == 'enemyBoss':
                    if len(self.ebullets) < self.bulletLim: 
                        self.ebullets.append(projectile(round((self.x + (self.width/2)) ), round (self.y + 30), 4, self.bulletColour, self.facing, self.bulletSpeed))
                        self.ebullets.append(projectile(round((self.x + (self.width/2)) -30), round (self.y + 30), 4, self.bulletColour, self.facing, self.bulletSpeed))
                        self.shotTimer -= 1
        else:
            self.shotTimer -= 1
            
        if self.shotTimer <= 0:
            self.shotTimer = self.shotPause
        
        #Draw enemy health bar background
        pygame.draw.rect(screen, (100,0,0), (self.x + self.healthx, self.y + self.healthy, self.bar_width, self.bar_height))

        #Calculate the width of the current health
        health_ratio = self.currentHealth / self.health
        current_bar_width = self.bar_width * health_ratio
        
        #Draw current enemy health
        pygame.draw.rect(screen, (0,128,0), (self.x + self.healthx, self.y + self.healthy, current_bar_width, self.bar_height))
         
            
    def move(self):
         #Enemy movement to follow player if player in range
        if self.shotTimer == self.shotPause:
            if player.x < self.x + self.range and player.x > self.x - self.range:  
                self.distX = self.x - player.x 
                self.distY = self.y - player.y
                self.totDist = math.sqrt(self.distX**2 + self.distY**2)
                
                if self.velocity > 0:
                    if self.totDist >= self.velocity and self.totDist != 0:
                        self.distX = self.distX/self.totDist
                        self.distY = self.distY/self.totDist
                        self.x = self.x - (self.distX * self.velocity) 
                        self.y = self.y - (self.distY * self.velocity)
                        self.hitbox = (self.x + self.xadj,self.y + self.yadj,self.width,self.height)
                        
                        
                if self.velocity < 0:
                    
                    if self.totDist >= self.velocity and self.totDist != 0:
                        self.distX = self.distX/self.totDist
                        self.distY = self.distY/self.totDist
                        self.x = self.x + (self.distX * self.velocity) 
                        self.y = self.y + (self.distY * self.velocity)
                        self.hitbox = (self.x + self.xadj,self.y + self.yadj,self.width,self.height)
                    
                if player.x < self.x:
                    self.followL = True
                    self.followR = False
                    
                if player.x > self.x:
                    self.followR = True
                    self.followL = False
                   
                
                if currentLevel.bgX > -currentLevel.current_Level_Width and currentLevel.bgX < 0:
                    self.x += screen_scroll
                
                
                if self.walkCount >= 18:
                    self.walkCount = 0
                
            else:   
                #Set path for the enemy and adjust with screen scrolling
                if self.path[0] <= self.start and currentLevel.bgX <= 0 and currentLevel.bgX > -currentLevel.current_Level_Width:
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
                        
                        if currentLevel.bgX > -currentLevel.current_Level_Width and currentLevel.bgX < 0:
                            self.x += screen_scroll
                            
                    #Turns enemy around
                    else:
                        self.velocity = self.velocity * -1 
                        self.walkCount = 0
                else:
                    if self.x - self.velocity > self.path[0]:
                        self.x += self.velocity 
                        
                        if currentLevel.bgX > -currentLevel.current_Level_Width and currentLevel.bgX < 0:
                            self.x += screen_scroll
                            
                    #Turns enemy around
                    else:
                        self.velocity = self.velocity * -1 
                        self.walkCount = 0
                        
                
                self.followR = False
                self.followL = False
                pass
                
                
        else:
            self.x += screen_scroll
            
        self.hitbox = (self.x + self.xadj,self.y + self.yadj,self.width,self.height)
        
        #Collision detection with player  
        if self.hitbox[1] - self.height < player.rect[1] + player.rect[3] and self.hitbox[1] + self.height > player.rect[1]:
            if self.hitbox[0] + self.width > player.rect[0] and self.hitbox[0] - self.width < player.rect[0] + player.rect[2]:
                self.timer -= 1
                if self.enemy_type == 'enemyB':
                    self.shotTimer = self.shotPause
                if self.timer <= 0:
                    player.hit()
                    self.timer = self.timerMax
        if self.walkCount >= 18:
                self.walkCount = 0  
                              
    #Enemy damage from bullet
    def hit(self):
        
        self.currentHealth -= player.bulletDmg
 
        if self.currentHealth  <= 0:
            if self.enemy_type == 'enemyA':
                player.score += 10
                
            if self.enemy_type == 'enemyB':
                player.score += 25
                item_drop = collectible('Gun_upgrade', self.x + 50, self.y + 30)
                collectibles_group.add(item_drop)
                
            if self.enemy_type == 'enemyBoss':
                player.score += 1000
            self.kill()
        pass
        
#Define groups for all game objects
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
collectibles_group = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
obstacles_group2 = pygame.sprite.Group()

#Class which defines which level is loaded
class levelLoad():  
    def __init__(self, level):

        self.levelList = [self.levelOne, self.levelTwo, self.levelThree]
        self.runLevel = level
        self.setLevel = self.levelList[self.runLevel]  
    
    #Level 1   
    def levelOne(self):
        self.bg = pygame.image.load('sprites\level1BG.png')
        self.ground = pygame.image.load('sprites\lvl1Road.png')
        self.bgX = 0
        self.bgX2 = self.bg.get_width()
        self.bgX3 = self.bgX2 + self.bg.get_width()
        self.groundX = 0
        self.groundX2 =  self.ground.get_width()
        
        
        
        item_box1 = collectible('Medpack', 1300, SCREEN_HEIGHT - 60)
        collectibles_group.add(item_box1)

        burntCar = obstacle('Burnt_car', 400, SCREEN_HEIGHT - 200)
        rustyCar = obstacle('Rusty_car', 1300, SCREEN_HEIGHT - 230)
        car = obstacle('Scooter', 1800, SCREEN_HEIGHT - 200)
        millitary_v = obstacle('Millitary vehicle', 0, SCREEN_HEIGHT - 200)
        
        tank = obstacle('Tank', 2150, SCREEN_HEIGHT - 190)
        
        rubbish1 = obstacle('Rubbish1', 560, SCREEN_HEIGHT - 60)
        rubbish2 = obstacle('Rubbish2', 840, SCREEN_HEIGHT - 120)
        rubbish3 = obstacle('Rubbish3', 1700, SCREEN_HEIGHT - 50)
        rubbish4 = obstacle('Rubbish4', 1200, SCREEN_HEIGHT - 50)
        rubbish5 = obstacle('Rubbish2', 2100, SCREEN_HEIGHT - 110)
        
        text1 = obstacle('Level1text', 300, 350)
        text2 = obstacle('Level1text2', 1100, 350)
        text3 = obstacle('Level1text3', 1800, 350)
        
        streetLamp1 = obstacle('streetlamp', 400, SCREEN_HEIGHT - 358)
        streetLamp2 = obstacle('streetlamp', 1000, SCREEN_HEIGHT - 358)
        streetLamp3 = obstacle('streetlamp', 1600, SCREEN_HEIGHT - 358)
        streetLamp4 = obstacle('streetlamp', 2200, SCREEN_HEIGHT - 358)
        
        robotEnemy1 = enemy('enemyA', 1600, SCREEN_HEIGHT - 150, 0, 10, 30, 40, 1600, 1800) 
        robotEnemy2 = enemy('enemyA', 2000, SCREEN_HEIGHT - 90, 0, 10, 30, 40, 1500, 2100)
        robotEnemy3 = enemy('enemyB', 2050, SCREEN_HEIGHT - 150, 0, 10, 30, 40, 1500, 2100)  
        robotEnemy4 = enemy('enemyA', 2200, SCREEN_HEIGHT - 150, 0, 10, 30, 40, 1500, 2100)  
        robotEnemy5 = enemy('enemyB', 1200, SCREEN_HEIGHT - 150, 0, 10, 30, 40, 1200, 1500) 
        
        self.enemyList = [robotEnemy1,robotEnemy2,robotEnemy3, robotEnemy4, robotEnemy5]   
        
        for enemies in self.enemyList:
            enemy_group.add(enemies)
        
        self.allLevelObjects = [rubbish1, rubbish2, rubbish3, rubbish4, rubbish5, streetLamp1, streetLamp2, streetLamp3, streetLamp4, burntCar, rustyCar, millitary_v, car,tank, text1, text2, text3]
        for objects in self.allLevelObjects:
            obstacles_group.add(objects)
            
        self.current_Level_Width = 1800
        
    #Level 2
    def levelTwo(self):
        self.bg = pygame.image.load('sprites\level2BG.png')
        self.ground = pygame.image.load('sprites\lvl1Road.png')
        self.bgX = 0
        self.bgX2 = self.bg.get_width()
        self.bgX3 = self.bgX2 + self.bg.get_width()
        self.groundX = 0
        self.groundX2 =  self.ground.get_width()
        
        
        item_box2 = collectible('Medpack', 750, SCREEN_HEIGHT - 200)
        collectibles_group.add(item_box2)

        millitary_v = obstacle('Millitary vehicle', 0, SCREEN_HEIGHT - 200)
        jeep = obstacle('Jeep', 700, SCREEN_HEIGHT - 220)
        tank = obstacle('Tank', 2150, SCREEN_HEIGHT - 190)
        
        rubbish1 = obstacle('Rubbish1', 1200, SCREEN_HEIGHT - 80)
        rubbish2 = obstacle('Rubbish2', 376, SCREEN_HEIGHT - 100)
        rubbish3 = obstacle('Rubbish3', 840, SCREEN_HEIGHT - 60)
        rubbish4 = obstacle('Rubbish4', 1870, SCREEN_HEIGHT - 96)
        
        streetLamp1 = obstacle('streetlamp', 400, SCREEN_HEIGHT - 358)
        streetLamp2 = obstacle('streetlamp', 800, SCREEN_HEIGHT - 358)
        streetLamp3 = obstacle('streetlamp', 1200, SCREEN_HEIGHT - 358)
        streetLamp4 = obstacle('streetlamp', 1600, SCREEN_HEIGHT - 358)
        
        robotEnemy1 = enemy('enemyA', 900, SCREEN_HEIGHT - 150, 0, 10, 30, 40, 400, 1300) 
        robotEnemy2 = enemy('enemyA', 820, SCREEN_HEIGHT - 80, 0, 10, 30, 40, 500, 1200)
        robotEnemy3 = enemy('enemyB', 2050, SCREEN_HEIGHT - 150, 0, 10, 30, 40, 1400, 2000)  
        robotEnemy4 = enemy('enemyA', 1900, SCREEN_HEIGHT - 140, 0, 10, 30, 40, 1240, 2000)  
        robotEnemy5 = enemy('enemyB', 2050, SCREEN_HEIGHT - 100, 0, 10, 30, 40, 1360, 2000)  
        robotEnemy6 = enemy('enemyA', 1800, SCREEN_HEIGHT - 170, 0, 10, 30, 40, 1120, 2000)  
        robotEnemy7 = enemy('enemyA', 1980, SCREEN_HEIGHT - 100, 0, 10, 30, 40, 1900, 2000)  
        robotEnemy8 = enemy('enemyA', 1990, SCREEN_HEIGHT - 170, 0, 10, 30, 40, 1950, 2000)  
        
        self.enemyList = [robotEnemy1,robotEnemy2,robotEnemy3, robotEnemy4,robotEnemy5,robotEnemy6, robotEnemy7, robotEnemy8]  
        
        for enemies in self.enemyList:
            enemy_group.add(enemies)
         
        self.allLevelObjects = [rubbish1, rubbish2, rubbish3, rubbish4, streetLamp1, streetLamp2, streetLamp3, streetLamp4, millitary_v, jeep, tank]
        for objects in self.allLevelObjects:
            obstacles_group.add(objects)
  
        self.current_Level_Width = 1800
    
    #Level 3 with boss    
    def levelThree(self):  
        self.bg = pygame.image.load('sprites\level3BG.png')
        self.ground = pygame.image.load('sprites\lvl1Road.png')
        self.bgX = 0
        self.bgX2 = self.bg.get_width()
        self.bgX3 = self.bgX2 + self.bg.get_width()
        self.groundX = 0
        self.groundX2 =  self.ground.get_width()
        
        
        item_box1 = collectible('Medpack', 425, SCREEN_HEIGHT - 120)
        item_box2 = collectible('Medpack', 450, SCREEN_HEIGHT - 50)
        collectibles_group.add(item_box1, item_box2)

        millitary_v = obstacle('Millitary vehicle', 0, SCREEN_HEIGHT - 200)
        tank = obstacle('Tank', 2150, SCREEN_HEIGHT - 190)
        
        rubbish1 = obstacle('Rubbish1', 1410, SCREEN_HEIGHT - 170)
        rubbish2 = obstacle('Rubbish2', 720, SCREEN_HEIGHT - 70)
        rubbish3 = obstacle('Rubbish3', 1940, SCREEN_HEIGHT - 130)
        rubbish4 = obstacle('Rubbish4', 1700, SCREEN_HEIGHT - 70)
        
        
        streetLamp1 = obstacle('streetlamp', 400, SCREEN_HEIGHT - 375)
        streetLamp2 = obstacle('streetlamp', 800, SCREEN_HEIGHT - 375)
        streetLamp3 = obstacle('streetlamp', 1200, SCREEN_HEIGHT - 375)
        streetLamp4 = obstacle('streetlamp', 1600, SCREEN_HEIGHT - 375)
        
        
        robotBoss = enemy('enemyBoss', 1700, SCREEN_HEIGHT - 150, 0, 0, 130, 120, 600, 800) 
        robotEnemy1 = enemy('enemyB', 1600, SCREEN_HEIGHT - 120, 0, 10, 30, 40, 1350, 1700)
        robotEnemy2 = enemy('enemyB', 1650, SCREEN_HEIGHT - 180, 0, 10, 30, 40, 1350, 1700) 
        
        self.enemyList = [robotEnemy1, robotEnemy2,  robotBoss]   
        
        for enemies in self.enemyList:
            enemy_group.add(enemies)
         
        self.allLevelObjects = [rubbish1, rubbish2, rubbish3, rubbish4, streetLamp1, streetLamp2, streetLamp3, streetLamp4, millitary_v, tank]
        for objects in self.allLevelObjects:
            obstacles_group.add(objects)
     
        
        self.current_Level_Width = 1800
         
    #Update level background based on screen scroll 
    def update(self, screen):
        
        if self.bgX <= 0 and self.bgX >= -self.current_Level_Width and player.x >= SCROLL_THRESH + player.velocity:
            self.bgX += screen_scroll
            self.bgX2 = self.bgX + self.bg.get_width()
            self.bgX3 = self.bgX2 + self.bg.get_width()
            screen.blit(self.bg, (self.bgX , 0))  
            screen.blit(self.bg, (self.bgX2, 0))
            screen.blit(self.bg, (self.bgX3, 0))
        
        if self.groundX <= 0 and self.groundX >= -self.current_Level_Width and player.x >= SCROLL_THRESH + player.velocity:
            self.groundX += screen_scroll 
            self.groundX2 = self.groundX + self.ground.get_width()
            self.groundX3 = self.groundX2 + self.ground.get_width()
            self.groundX4 = self.groundX3 + self.ground.get_width()
            screen.blit(self.ground, (self.groundX , SCREEN_HEIGHT - 150))  
            screen.blit(self.ground, (self.groundX2, SCREEN_HEIGHT - 150))
            screen.blit(self.ground, (self.groundX3, SCREEN_HEIGHT - 150))
            screen.blit(self.ground, (self.groundX4, SCREEN_HEIGHT - 150))
        
        if self.bgX >=0:
            self.bgX = 0 
        
        if self.groundX >=0:
            self.groundX = 0 
            
        if self.bgX <= -self.current_Level_Width:
            self.bgX = -self.current_Level_Width
            
        if self.groundX <= -self.current_Level_Width:
                self.groundX = -self.current_Level_Width
  
    pressed_keys = pygame.key.get_pressed()
    pressed_mouse = pygame.mouse.get_pressed()
    cursor_pos = pygame.mouse.get_pos()    

#Set current level to Level 1 and load level
currentLevel = levelLoad(0)  
currentLevel.setLevel()  

#Draws all objects and updates screen
def drawGame():

    currentLevel.update(screen)
    obstacles_group.draw(screen)
    for obs in obstacles_group:
        obs.update()
    
    #Checks for enemies
    if len(enemy_group) > 0:   
        
        #Checks for player collision with enemies and draws enemies above or below player based on hitbox Y coordinate.
        for enemy in enemy_group:
            if enemy.hitbox[1] + enemy.height +40 < player.rect[1] + player.rect[3] and enemy.hitbox[1] + enemy.height + 40 > player.rect[1]:      
                if enemy.hitbox[0] + enemy.width > player.rect[0] and enemy.hitbox[0] - enemy.width < player.rect[0] + player.rect[2]:
                    
                    enemy.spriteCollision = True   
                    enemy.update(screen)
                    enemy.move()
                      
                else:
                    enemy.spriteCollision = False
                    
            else:
                enemy.spriteCollision = False 
                
        #Loop to check if player bullets have hit a target        
        for enemy in enemy_group:
            for bullet in bullets:
                if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
                    if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                        enemy.hit()
                        bullets.pop(bullets.index(bullet))
                        
                if bullet.x < SCREEN_WIDTH and bullet.x > 0:
                    bullet.x += (bullet.velocity + screen_scroll)
                else:
                    bullets.pop(bullets.index(bullet))
                    
        #Loop to check if enemy bullets have hit the player                  
            for bullet in enemy.ebullets:
                if bullet.y - bullet.radius < player.rect[1] + player.rect[3] and bullet.y + bullet.radius > player.rect[1]:
                    if bullet.x + bullet.radius > player.rect[0] and bullet.x - bullet.radius < player.rect[0] + player.rect[2]:
                        player.hit()
                        enemy.ebullets.pop(enemy.ebullets.index(bullet))
                        
                if bullet.x < SCREEN_WIDTH and bullet.x > 0 and bullet.y > 0 and bullet.y < SCREEN_HEIGHT:
                    bullet.x += bullet.velocity + screen_scroll
                    
                    
                else:
                    enemy.ebullets.pop(enemy.ebullets.index(bullet))
                    
    #If there are no enemies, bullets can still be fired
    else:
        for bullet in bullets:
            if bullet.x < SCREEN_WIDTH and bullet.x > 0 and bullet.y > 0 and bullet.y < SCREEN_HEIGHT:
                bullet.x += bullet.velocity + screen_scroll        
            else:
                bullets.pop(bullets.index(bullet))
                
    #Draw all game obstacles on screen                      
    obstacles_group.draw(screen)
    for obs in obstacles_group:
        obs.update()
    
    #Draw player on screen              
    player.update(pressed_keys, pressed_mouse)
    player.draw(screen)
    player.UI(screen)
    
    #Draw all game obstacles 2 on screen     
    obstacles_group2.draw(screen)
    for obs in obstacles_group2:
        obs.update()

    #Draw enemies if they are not colliding with player     
    if len(enemy_group) > 0:             
        if enemy.spriteCollision == False:
            for enemies in enemy_group:   
                enemies.update(screen)
                enemies.move() 
    
    #Draw all game collectibles on screen             
    collectibles_group.update()
    collectibles_group.draw(screen)
    
    for items in collectibles_group:
        items.update()
    
    #Draw all player bullets on screen
    for bullet in bullets:
        bullet.draw(screen)
        
    #Draw all enemy bullets on screen     
    for enemy in enemy_group:
        for ebullet in enemy.ebullets:
            ebullet.draw(screen)


#Define bullet count for player
bulletCount = 0

#Define global variables for game running and menu
global menu
global gameRun  
restartTimer = 10 
menu = True   
gameRun = False 
restart = False

run = True
#Main game loop
while run:
    pressed_keys = pygame.key.get_pressed()
    pressed_mouse = pygame.mouse.get_pressed()
    
    #If ESC exit pygame
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    if pressed_keys[K_ESCAPE]:
        run = False
        
    #Main menu
    if menu == True:
        gameMenubg = (0,0, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        pygame.draw.rect(screen, (255,255,255), gameMenubg)
        screen.blit(pygame.image.load('sprites\maintitle.png'), (190, 130))
        menu_text = font.render("Press ENTER to start", True, (20, 20, 20))
        highscore_text = font.render(f"HIGHSCORE: {highScore}", True, (242, 80, 53))
        screen.blit(menu_text, (260, 300))
        screen.blit(highscore_text, (300, 350))
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_RETURN]:
            player = Player(200, 450, 64, 64)
            enemy_group.empty()
            collectibles_group.empty()
            obstacles_group.empty()
            obstacles_group2.empty()
            player.playerDead = False
            
            currentLevel.runLevel = 0
            currentLevel.setLevel = currentLevel.levelList[0]
            currentLevel.setLevel() 
            
            currentLevel.bgX = 0
            menu = False   
            gameRun = True
        pygame.display.update()
    
    #Restart level 
    if restart == True:
            
        enemy_group.empty()
        collectibles_group.empty()
        obstacles_group.empty()
        obstacles_group2.empty()
        
        currentLevel.runLevel = 0
        currentLevel.setLevel = currentLevel.levelList[0]
        currentLevel.setLevel() 
        
        player.playerDead = False
        player = Player(200, 500, 64, 64)
        restart = False

    #Main running code for game
    if gameRun == True:
        
        drawGame()
        if player.current_health <= 0 and player.current_lives == 0: 
                player.die()   
                 
        #IF all enemies dead, proceed to next level           
        if len(enemy_group) == 0: 
            if currentLevel.runLevel == 2:
                finish_text = font.render("CONGRATULATIONS!", True, (237, 237, 237))
                finish_text2 = font.render("YOU FINISHED THE GAME!", True, (237, 237, 237))
                finish_text3 = font.render("Press BACKSPACE to return to menu.", True, (237, 237, 237))
                pygame.draw.rect(screen, (25,38,240), (150, 280, 475, 140))
                screen.blit(finish_text, (260, SCREEN_HEIGHT/2))
                screen.blit(finish_text2, (230, SCREEN_HEIGHT/2 + 35))
                screen.blit(finish_text3, (170, SCREEN_HEIGHT/2 + 70))
                if pressed_keys[K_BACKSPACE]:
                    menu = True
                    gameRun = False
                    
            else:    
                nextLevelText = obstacle('nextLevelText', SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                if not (finishLevelText):
                    obstacles_group.add(nextLevelText)
                    finishLevelText = True

                #Load next level
                if pressed_keys[K_RETURN] and player.playerDead != True:
                    enemy_group.empty()
                    collectibles_group.empty()
                    obstacles_group.empty()
                    obstacles_group2.empty()
                    currentLevel.runLevel += 1
                    currentLevel.setLevel = currentLevel.levelList[currentLevel.runLevel]
                    currentLevel.setLevel()
                    finishLevelText = False
                    
        pygame.display.update()
        
        #Ensure we maintain a 30 frames per second rate
        clock.tick(30)




