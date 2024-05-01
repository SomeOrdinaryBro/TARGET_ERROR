import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Target #Error')

#player action
moving_left = False
moving_right = False

class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, ):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('./assets/player_character/Gunner_Black_Idle.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    def draw(self):
        screen.blit(self.image, player.rect)
    
    
player = Soldier(200, 200, 3)


x = 200
y = 200
scale = 3

run = True

while run:
    
    player.draw()
    
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