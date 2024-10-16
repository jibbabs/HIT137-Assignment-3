
#Sprites courtesy of CRAFTPIX.NET
# Import the pygame module
import pygame
import math
from pygame.locals import *
from game import player
from game import currentLevel

pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
x = 0
y = SCREEN_HEIGHT - 25

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.Font(None, 36)
SCROLL_THRESH = 50
screen_scroll = 0
LEVEL_WIDTH = 100
bg_scroll = 0           

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
                    player.current_health += 20
            self.kill()        
          
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Gun_upgrade':
                player.gunLvl += 1
                player.bulletLim += 1
                player.bulletSpeed += 4
                player.shotSpeed -= 2
                player.bulletSize += 1
                player.bulletDmg += 1
                
            self.kill()        
                
        if self.item_type == 'Life':
            if player.current_lives < player.max_lives:
                player.current_lives += 1
            self.kill()
      
class obstacle (pygame.sprite.Sprite):
    burntCar = pygame.image.load('sprites\-burnt_car.png').convert_alpha()
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
        global undercollision
        global uppercollision
        global leftcollision
        global rightcollision
        #Move with level
        #pygame.draw.rect(screen, (0,100,0),self.rect,1)
        
    
         
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
        self.hitbox = (self.x - 10 ,self.y - 3,self.width,self.height)
        self.enemy_type = enemy_type
        self.rect = self.hitbox
        self.timer = 10
        self.spriteCollision = False
        self.aggro = False
        self.enemy_type = enemy_type
        self.left = False
        self.right = False
        if self.enemy_type == 'enemyA':
            enemy.enemyA(self)
        self.ebullets = []
        
    def enemyA(self):
        self.velocity = 2
        self.walkRight = [pygame.image.load('sprites\enemyWR1.png'), pygame.image.load('sprites\enemyWR2.png'), pygame.image.load('sprites\enemyWR3.png'), pygame.image.load('sprites\enemyWR4.png'), pygame.image.load('sprites\enemyWR5.png'), pygame.image.load('sprites\enemyWR6.png')]
        self.walkLeft = [pygame.image.load('sprites\enemyWL1.png'), pygame.image.load('sprites\enemyWL2.png'), pygame.image.load('sprites\enemyWL3.png'), pygame.image.load('sprites\enemyWL4.png'), pygame.image.load('sprites\enemyWL5.png'), pygame.image.load('sprites\enemyWL6.png')]
        self.shootingR = pygame.image.load('sprites\shooting.png')
        self.shootingL = pygame.image.load('sprites\shootingL.png')
        self.facing = 1
        self.bulletLim = 2
        self.bulletColour = (234,237,211)
        self.range = 400
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
        
        
    def update(self, screen):
        
        if self.shotTimer < self.shotPause:
            if self.followR == True:
                screen.blit(self.shootingR, (self.x, self.y))
                
            else:
                screen.blit(self.shootingL, (self.x, self.y))
                
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
            
        self.bulletx = self.bulletx * self.facing
        if self.shotTimer == self.shotPause:
            if player.x < self.x + self.range and player.x > self.x - self.range:
                if len(self.ebullets) < self.bulletLim:
                    self.ebullets.append(projectile(round((self.x + (self.width/2)) + self.bulletx), round (self.y + self.bullety), 4, self.bulletColour, self.facing, self.bulletSpeed))
                   
                    self.shotTimer -= 1
        else:
            self.shotTimer -= 1
            
        if self.shotTimer <= 0:
            self.shotTimer = self.shotPause
        
        # Draw enemy health bar background
        pygame.draw.rect(screen, (100,0,0), (self.x + self.healthx, self.y + self.healthy, self.bar_width, self.bar_height))

        # Calculate the width of the current health
        health_ratio = self.currentHealth / self.health
        current_bar_width = self.bar_width * health_ratio
        
        # Draw current health
        pygame.draw.rect(screen, (0,128,0), (self.x + self.healthx, self.y + self.healthy, current_bar_width, self.bar_height))
         
            
    def move(self):

        #Detects if player is within enemy range and begins following.
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
                
                #Collision detection with player
                self.hitbox = (self.x + self.xadj,self.y + self.yadj,self.width,self.height)
                
                if self.hitbox[1] - self.height < player.rect[1] + player.rect[3] and self.hitbox[1] + self.height > player.rect[1]:
                    if self.hitbox[0] + self.width > player.rect[0] and self.hitbox[0] - self.width < player.rect[0] + player.rect[2]:
                        self.timer -= 1
                        
                        if self.timer <= 0:
                            player.hit()
                            self.timer = 10
                if self.walkCount >= 18:
                        self.walkCount = 0
        else:
            self.x += screen_scroll
            
    def hit(self):
        self.currentHealth -= player.bulletDmg
        if self.currentHealth  <= 0:
            self.kill()
        pass


enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
collectibles_group = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
obstacles_group2 = pygame.sprite.Group()

class levelLoad():  
    def __init__(self, level):

        self.levelList = [self.levelOne, self.levelTwo, self.levelThree]
        self.runLevel = level
        self.setLevel = self.levelList[self.runLevel]  
               
        
        
    def levelOne(self):
        self.bg = pygame.image.load('sprites\level1BG.png')
        self.ground = pygame.image.load('sprites\lvl1Road.png')
        self.bgX = 0
        self.bgX2 = self.bg.get_width()
        self.bgX3 = self.bgX2 + self.bg.get_width()
        self.groundX = 0
        self.groundX2 =  self.ground.get_width()
        
        item_box = collectible('Gun_upgrade', 600, SCREEN_HEIGHT - 130)
        collectibles_group.add(item_box)
        item_box2 = collectible('Medpack', 700, SCREEN_HEIGHT - 60)
        collectibles_group.add(item_box2)

        burntCar = obstacle('Burnt_car', 400, SCREEN_HEIGHT - 200)
        
        rubbish1 = obstacle('Rubbish1', 560, SCREEN_HEIGHT - 60)
        rubbish2 = obstacle('Rubbish2', 840, SCREEN_HEIGHT - 120)
        rubbish3 = obstacle('Rubbish3', 1700, SCREEN_HEIGHT - 200)
        rubbish4 = obstacle('Rubbish4', 1200, SCREEN_HEIGHT - 50)
        
        text1 = obstacle('Level1text', 300, 350)
        text2 = obstacle('Level1text2', 1100, 350)
        text3 = obstacle('Level1text3', 1800, 350)
        
        streetLamp1 = obstacle('streetlamp', 400, SCREEN_HEIGHT - 358)
        streetLamp2 = obstacle('streetlamp', 800, SCREEN_HEIGHT - 358)
        streetLamp3 = obstacle('streetlamp', 1200, SCREEN_HEIGHT - 358)
        streetLamp4 = obstacle('streetlamp', 1600, SCREEN_HEIGHT - 358)
        
        #robotEnemy1 = enemy('enemyA', 1300, SCREEN_HEIGHT - 150, 0, 20, 30, 20, 1000, 1400) 
        robotEnemy2 = enemy('enemyA', 600, SCREEN_HEIGHT - 150, 0, 20, 30, 20, 600, 800) 
        
        self.enemyList = [ robotEnemy2]   
        
        for enemies in self.enemyList:
            enemy_group.add(enemies)
         
        self.allLevelObjects = [rubbish1, rubbish2, rubbish3, rubbish4, streetLamp1, streetLamp2, streetLamp3, streetLamp4, burntCar, text1, text2, text3]
        for objects in self.allLevelObjects:
            obstacles_group.add(objects)
            
        self.current_Level_Width = 2000
        
    
    def levelTwo(self):
        self.bg = pygame.image.load('sprites\level2BG.png')
        self.ground = pygame.image.load('sprites\lvl1Road.png')
        self.bgX = 0
        self.bgX2 = self.bg.get_width()
        self.bgX3 = self.bgX2 + self.bg.get_width()
        self.groundX = 0
        self.groundX2 =  self.ground.get_width()
        
        item_box = collectible('Gun_upgrade', 600, SCREEN_HEIGHT - 130)
        collectibles_group.add(item_box)
        item_box2 = collectible('Medpack', 700, SCREEN_HEIGHT - 60)
        collectibles_group.add(item_box2)

        
        
        rubbish1 = obstacle('Rubbish1', 560, SCREEN_HEIGHT - 60)
        rubbish2 = obstacle('Rubbish2', 840, SCREEN_HEIGHT - 120)
        rubbish3 = obstacle('Rubbish3', 1700, SCREEN_HEIGHT - 200)
        rubbish4 = obstacle('Rubbish4', 1200, SCREEN_HEIGHT - 50)
        
        text1 = obstacle('Level1text', 300, 350)
        text2 = obstacle('Level1text2', 1100, 350)
        text3 = obstacle('Level1text3', 1800, 350)
        
        streetLamp1 = obstacle('streetlamp', 400, SCREEN_HEIGHT - 358)
        streetLamp2 = obstacle('streetlamp', 800, SCREEN_HEIGHT - 358)
        streetLamp3 = obstacle('streetlamp', 1200, SCREEN_HEIGHT - 358)
        streetLamp4 = obstacle('streetlamp', 1600, SCREEN_HEIGHT - 358)
        
        #robotEnemy1 = enemy('enemyA', 1300, SCREEN_HEIGHT - 150, 0, 20, 30, 20, 1000, 1400) 
        robotEnemy2 = enemy('enemyA', 600, SCREEN_HEIGHT - 150, 0, 20, 30, 20, 600, 800) 
        
        self.enemyList = [ robotEnemy2]   
        
        for enemies in self.enemyList:
            enemy_group.add(enemies)
         
        self.allLevelObjects = [rubbish1, rubbish2, rubbish3, rubbish4, streetLamp1, streetLamp2, streetLamp3, streetLamp4, text1, text2, text3]
        for objects in self.allLevelObjects:
            obstacles_group.add(objects)
  
        self.current_Level_Width = 2000
         
    def levelThree(self):  
        self.bg = pygame.image.load('sprites\image.png')
        self.ground = pygame.image.load('sprites\lvl1Road.png')
        self.bgX = 0
        self.bgX2 = self.bg.get_width()
        self.bgX3 = self.bgX2 + self.bg.get_width()
        self.groundX = 0
        self.groundX2 =  self.ground.get_width()
        
        item_box = collectible('Gun_upgrade', 600, SCREEN_HEIGHT - 130)
        collectibles_group.add(item_box)
        item_box2 = collectible('Medpack', 700, SCREEN_HEIGHT - 60)
        collectibles_group.add(item_box2)

        
        
        rubbish1 = obstacle('Rubbish1', 560, SCREEN_HEIGHT - 60)
        rubbish2 = obstacle('Rubbish2', 840, SCREEN_HEIGHT - 120)
        rubbish3 = obstacle('Rubbish3', 1700, SCREEN_HEIGHT - 200)
        rubbish4 = obstacle('Rubbish4', 1200, SCREEN_HEIGHT - 50)
        
        text1 = obstacle('Level1text', 300, 350)
        text2 = obstacle('Level1text2', 1100, 350)
        text3 = obstacle('Level1text3', 1800, 350)
        
        streetLamp1 = obstacle('streetlamp', 400, SCREEN_HEIGHT - 375)
        streetLamp2 = obstacle('streetlamp', 800, SCREEN_HEIGHT - 375)
        streetLamp3 = obstacle('streetlamp', 1200, SCREEN_HEIGHT - 375)
        streetLamp4 = obstacle('streetlamp', 1600, SCREEN_HEIGHT - 375)
        
        #robotEnemy1 = enemy('enemyA', 1300, SCREEN_HEIGHT - 150, 0, 20, 30, 20, 1000, 1400) 
        robotEnemy2 = enemy('enemyA', 600, SCREEN_HEIGHT - 150, 0, 20, 30, 20, 600, 800) 
        
        self.enemyList = [ robotEnemy2]   
        
        for enemies in self.enemyList:
            enemy_group.add(enemies)
         
        self.allLevelObjects = [rubbish1, rubbish2, rubbish3, rubbish4, streetLamp1, streetLamp2, streetLamp3, streetLamp4, text1, text2, text3]
        for objects in self.allLevelObjects:
            obstacles_group.add(objects)
     
        
        self.current_Level_Width = 2000
         
    
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
                          


