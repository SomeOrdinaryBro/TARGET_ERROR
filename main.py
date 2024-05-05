import pygame
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Target #Error')

#Game FRAME RATE
clock = pygame.time.Clock()
FPS = 60

#Game Var
GRAVITY = 0.80

#player action
moving_left = False
moving_right = False
shoot = False

#load images
bullet_img = pygame.image.load('./assets/icons/bullet.png').convert_alpha()

#COLORS
BG = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen,RED, (0, 300), (SCREEN_WIDTH, 300))

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed 
        self.ammo = ammo
        self.start_ammo = ammo  
        self.shoot_cooldown = 0 
        self.health = 100   
        self.max_health = self.health 
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = False
        self.flip = False
        
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
        animation_types = ['Idle' , 'Run', 'Jump']
        for animation in animation_types:
            
            temp_list = []
            num_of_frames = len(os.listdir(f'./assets/{self.char_type}/{animation}'))
            
            for i in range(num_of_frames):
                img = pygame.image.load(f'./assets/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    def update(self):
        self.update_animation()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def move(self, moving_left, moving_right):
        #reset movement var
        dx = 0
        dy = 0
        
        #move left and right
        if moving_left:
            dx = -self.speed    
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        #Jump    
        if self.jump == True and self.in_air == False: 
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        #Gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
        #collision
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False
        
        #update position
        self.rect.x += dx
        self.rect.y += dy
 
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        #update image based on current image
        self.image = self.animation_list[self.action][self.frame_index]
        #elapsed
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            
            
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            #update anim setting
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self):
        self.rect.x += (self.direction * self.speed)
        #memory update
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                self.kill()
                
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                self.kill()
        
#Sprite group
bullet_group = pygame.sprite.Group()

player = Soldier('player_character', 50, 50, 3, 5, 20)
enemy = Soldier('enemy_character', 400, 200, 3, 5, 20)


x = 200
y = 200
scale = 3

run = True

while run:
    
    clock.tick(FPS)
    
    draw_bg()
    
    player.update()
    player.draw()
    enemy.draw()

    #update/draw groups
    bullet_group.update()
    bullet_group.draw(screen)
    
    #update player actions
    if player.alive:
        if shoot: 
            player.shoot()
        if player.in_air:
            player.update_action(2)#2: jump
        elif moving_left or moving_right:
            player.update_action(1) #1: run
        else:
            player.update_action(0) #0: idle
        
        player.move(moving_left, moving_right)
        
    for event in pygame.event.get():
        #button presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
                
        #button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
        
        #Quit Game
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.update()
          
pygame.quit()