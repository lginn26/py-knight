# Imports
import pygame


# Initialize game engine
pygame.init()


# Window
SCALE = 64
WIDTH = 16 * SCALE
HEIGHT = 9 * SCALE
SIZE = (WIDTH, HEIGHT)
TITLE = "Name of Game"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY_BLUE = (0, 200, 225)
GREEN = (0, 200, 0)


# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/cheri.ttf", 96)


# Sounds
JUMP_SND = pygame.mixer.Sound('assets/sounds/jump.ogg')
GEM_SND = pygame.mixer.Sound('assets/sounds/gem.ogg')


# Images
''' characters '''
hero_img = pygame.image.load('assets/images/characters/platformChar_walk1.png').convert_alpha()

''' tiles '''
grass_img = pygame.image.load('assets/images/tiles/platformPack_tile001.png').convert_alpha()
platform_img = pygame.image.load('assets/images/tiles/platformPack_tile020.png').convert_alpha()
                  
''' items '''
gem_img = pygame.image.load('assets/images/items/platformPack_item008.png').convert_alpha()


# Game physics
GRAVITY = 1


# Stages
START = 0
PLAYING = 1
END = 3


# Game classes
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x * SCALE
        self.rect.y = y * SCALE
        
        #bounding_rect = self.mask.get_bounding_rects()
        #print(self.rect, bounding_rect)

    
class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * SCALE
        self.rect.y = y * SCALE

        self.speed = 5
        self.jump_power = 24
        self.vx = 0
        self.vy = 0

    def move_left(self):
        self.vx = -self.speed
    
    def move_right(self):
        self.vx = self.speed

    def stop(self):
        self.vx = 0
    
    def jump(self):
        pass

    def apply_gravity(self):
        pass

    def move_and_check_tiles(self):
        ''' move in horizontal direction and resolve colisions '''
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, tiles, False)

        for hit in hit_list:
            if self.vx > 0:
                self.rect.right = hit.rect.left
            elif self.vx < 0:
                self.rect.left = hit.rect.right
                
        ''' move in vertical direction and resolve colisions '''
        self.rect.y += self.vy
        hit_list = pygame.sprite.spritecollide(self, tiles, False)

        for hit in hit_list:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
            elif self.vy < 0:
                self.rect.top = hit.rect.bottom

            self.vy = 0
        
    def check_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def process_items(self):
        pass

    def set_image(self):
        pass
    
    def update(self):
        self.apply_gravity()
        self.move_and_check_tiles()
        self.process_items()
        self.check_edges()


class Gem(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * SCALE
        self.rect.y = y * SCALE

    def apply(self, player):
        pass
        
    def update(self):
        pass


class Enemy(pygame.sprite.Sprite):
    pass

    
# Game helper functions
def show_title_screen():
    text = FONT_XL.render(TITLE, 1, WHITE)
    screen.blit(text, [128, 204])
    
def show_end_screen():
    text = FONT_LG.render("You Win", 1, WHITE)
    screen.blit(text, [128, 204])

def show_stats():
    text = FONT_LG.render(str(player.score), 1, WHITE)
    screen.blit(text, [20, 20])
       
def setup():
    global hero, player, tiles, items, stage
    
    ''' Make sprites '''
    hero = Hero(3, 7, hero_img)

    t1 = Tile(0, 8, grass_img)
    t2 = Tile(1, 8, grass_img)
    t3 = Tile(2, 8, grass_img)
    t4 = Tile(3, 8, grass_img)
    t5 = Tile(4, 8, grass_img)
    t6 = Tile(5, 8, grass_img)
    t7 = Tile(6, 8, grass_img)
    t8 = Tile(7, 8, grass_img)
    t9 = Tile(8, 8, grass_img)
    t10 = Tile(9, 8, grass_img)
    t11 = Tile(10, 8, grass_img)
    t12 = Tile(11, 8, grass_img)
    t13 = Tile(12, 8, grass_img)
    t14 = Tile(13, 8, grass_img)
    t15 = Tile(14, 8, grass_img)
    t16 = Tile(15, 8, grass_img)

    t17 = Tile(5, 5, platform_img)
    t18 = Tile(6, 5, platform_img)
    t19 = Tile(7, 5, platform_img)

    t20 = Tile(10, 3, platform_img)
    t21 = Tile(11, 3, platform_img)
    t22 = Tile(12, 3, platform_img)

    i1 = Gem(13, 7, gem_img)
    i2 = Gem(6, 4, gem_img)
    i3 = Gem(11, 2, gem_img)
    
    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    items = pygame.sprite.Group()
    tiles = pygame.sprite.Group()

    ''' Add sprites to groups '''
    player.add(hero)

    tiles.add(t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16)
    tiles.add(t17, t18, t19)
    tiles.add(t20, t21, t22)
    
    items.add(i1, i2, i3)
    
    ''' set stage '''
    stage = START

    
# Game loop
setup()

running = True
while running:
    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
                    
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    hero.jump()

    pressed = pygame.key.get_pressed()

    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            hero.move_left()
        elif pressed[pygame.K_RIGHT]:
            hero.move_right()
        else:
            hero.stop()
        
    
    # Game logic
    if stage == PLAYING:
        player.update()

            
    # Drawing code
    screen.fill(SKY_BLUE)
    player.draw(screen)
    tiles.draw(screen)
    items.draw(screen)
        
    if stage == START:
        show_title_screen()        
    elif stage == END:
        show_end_screen()

    
    # Update screen
    pygame.display.flip()
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
