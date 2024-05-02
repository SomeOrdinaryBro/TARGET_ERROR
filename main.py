import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Target #Error')

#Game FRAME RATE
clock = pygame.time.Clock()
FPS = 60

#player action
moving_left = False
moving_right = False

#COLORS
BG = (144, 201, 120)

def draw_bg():
    screen.fill(BG)

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed        
        self.direction = 1
        self.flip = False
        
        self.animation_list = []
        self.index = 0
        for i in range(5):
            img = pygame.image.load(f'./assets/{self.char_type}/idle/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list.append(img)
            
        self.image = self.animation_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
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
            
        #update position
        self.rect.x += dx
        self.rect.y += dy
        
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
    
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

player = Soldier('player_character', 200, 200, 3, 5)
enemy = Soldier('enemy_character', 400, 200, 3, 5)


x = 200
y = 200
scale = 3

run = True

while run:
    
    clock.tick(FPS)
    
    draw_bg()
    
    player.draw()
    enemy.draw()
    
    player.move(moving_left, moving_right)
    
    for event in pygame.event.get():
        #button presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                run = False
                
        #button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
        
        
        #Quit Game
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.update()
          
pygame.quit()