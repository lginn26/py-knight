# Imports
import pygame


# Initialize game engine
pygame.init()


# Window
SCALE = 64
WIDTH = 28 * SCALE
HEIGHT = 15 * SCALE
SIZE = (WIDTH, HEIGHT)
TITLE = "Name of Game"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

world_width = 192 * SCALE
world_height = 15 * SCALE
world = pygame.Surface([world_width, world_height])
world_x = 0
world_y = 0

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
hero_img = pygame.image.load('assets/images/characters/py_knight.png').convert_alpha()

''' tiles '''
grass_surface_img = pygame.image.load('assets/images/tiles/grass_block_surface.png').convert_alpha()
grass_rightcorner_img = pygame.image.load('assets/images/tiles/grass_block_rightcorner.png').convert_alpha()
grass_leftcorner_img = pygame.image.load('assets/images/tiles/grass_block_leftcorner.png').convert_alpha()
grass_rightwall_img = pygame.image.load('assets/images/tiles/grass_block_rightwall.png').convert_alpha()
grass_leftwall_img = pygame.image.load('assets/images/tiles/grass_block_leftwall.png').convert_alpha()
grass_rightmerger_img = pygame.image.load('assets/images/tiles/grass_block_rightmerger.png').convert_alpha()
grass_leftmerger_img = pygame.image.load('assets/images/tiles/grass_block_leftmerger.png').convert_alpha()
grass_filler_img = pygame.image.load('assets/images/tiles/grass_block_filler.png').convert_alpha()

platfrom_wooden_left = pygame.image.load('assets/images/tiles/wooden_platform_left.png').convert_alpha()
platfrom_wooden_middle = pygame.image.load('assets/images/tiles/wooden_platform_middle.png').convert_alpha()
platfrom_wooden_right = pygame.image.load('assets/images/tiles/wooden_platform_right.png').convert_alpha()
                  
''' items '''


# Game physics
GRAVITY = 1
TERMINAL_VELOCITY = 16


# Stages
START = 0
PLAYING = 1
END = 3


# Game classes
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, t_type, isplatform=False):
        super().__init__()

        if t_type == "grs_s":
            self.image = grass_surface_img
        elif t_type == "grs_rc":
            self.image = grass_rightcorner_img
        elif t_type == "grs_lc":
            self.image = grass_leftcorner_img
        elif t_type == "grs_rw":
            self.image = grass_rightwall_img
        elif t_type == "grs_lw":
            self.image = grass_leftwall_img
        elif t_type == "grs_lm":
            self.image = grass_leftmerger_img
        elif t_type == "grs_rm":
            self.image = grass_rightmerger_img
        elif t_type == "grs_f":
            self.image = grass_filler_img
        elif t_type == "plf_wd_lft":
            self.image = platfrom_wooden_left
        elif t_type == "plf_wd_mid":
            self.image = platfrom_wooden_middle
        elif t_type == "plf_wd_rht":
            self.image = platfrom_wooden_right

        self.isplatform = isplatform
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

    def can_jump(self):
        self.rect.y += 2
        hit_list = pygame.sprite.spritecollide(self, tiles, False)
        self.rect.y -= 2

        return len(hit_list) > 0
    
    def jump(self):
        if self.can_jump():
            self.vy = -self.jump_power

    def apply_gravity(self):
        self.vy += GRAVITY
        self.vy = min(self.vy, TERMINAL_VELOCITY)

    def move_and_check_tiles(self):
        ''' move in horizontal direction and resolve colisions '''
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, tiles, False)

        for hit in hit_list:
            if not hit.isplatform:
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
                
            elif self.vy < 0 and not hit.isplatform:
                self.rect.top = hit.rect.bottom
        
                self.vy = 0
        
    def check_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > world_width:
            self.rect.right = world_width

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
def draw_grid(scale, color=GREEN, width=SIZE[0], height=SIZE[1]):
    '''
    Draws a grid that can overlay your picture.
    This should make it easier to figure out coordinates
    when drawing pictures.
    '''
    for x in range(0, width, scale):
        pygame.draw.line(screen, color, [x, 0], [x, height], 1)
    for y in range(0, height, scale):
        pygame.draw.line(screen, color, [0, y], [width, y], 1)

def show_title_screen():
    text = FONT_XL.render(TITLE, 1, WHITE)
    screen.blit(text, [128, 204])
    
def show_end_screen():
    text = FONT_LG.render("You Win", 1, WHITE)
    screen.blit(text, [128, 204])

def show_stats():
    text = FONT_LG.render(str(player.score), 1, WHITE)
    screen.blit(text, [20, 20])

def calculate_offset():
    x = -1 * hero.rect.centerx + WIDTH / 2

    if x >= 0:
        return 0, 0
    elif x <= WIDTH:
        return 0, 0
    else:
        return x, 0

def setup():
    global hero, player, tiles, items, stage
    
    ''' Make sprites '''
    hero = Hero(3, 7, hero_img)

    preped_tiles = [
    Tile(0, 14, "grs_s"), 
    Tile(1, 14, "grs_s"), 
    Tile(2, 14, "grs_s"), 
    Tile(3, 14, "grs_s"),
    Tile(4, 14, "grs_s"),
    Tile(5, 14, "grs_s"),
    Tile(6, 14, "grs_lm"),
    Tile(6, 13, "grs_lw"),
    Tile(6, 12, "grs_lw"),
    Tile(6, 11, "grs_lw"),
    Tile(6, 10, "grs_lc"),
    Tile(7, 10, "grs_s"),
    Tile(8, 10, "grs_s"),
    Tile(9, 10, "grs_s"),
    Tile(10, 10, "grs_s"),
    Tile(11, 10, "grs_rc"),
    Tile(11, 11, "grs_rw"),
    Tile(11, 12, "grs_rw"),
    Tile(11, 13, "grs_rw"),
    Tile(11, 14, "grs_rm"),
    Tile(12, 14, "grs_s"),
    Tile(13, 14, "grs_s"),
    Tile(14, 14, "grs_s"),
    Tile(15, 14, "grs_s"),
    Tile(16, 14, "grs_s"),
    Tile(17, 14, "grs_s"),
    Tile(18, 14, "grs_s"),
    Tile(19, 14, "grs_lm"),
    Tile(19, 13, "grs_lc"),
    Tile(20, 13, "grs_lm"),
    Tile(20, 12, "grs_lc"),
    Tile(21, 12, "grs_lm"),
    Tile(21, 11, "grs_lc"),
    Tile(22, 11, "grs_lm"),
    Tile(22, 10, "grs_lc"),
    Tile(23, 10, "grs_rc"),
    Tile(23, 11, "grs_rw"),
    Tile(23, 12, "grs_rw"),
    Tile(23, 13, "grs_rw"),
    Tile(23, 14, "grs_rw"),

    Tile(7, 14, "grs_f"),
    Tile(8, 14, "grs_f"),
    Tile(9, 14, "grs_f"),
    Tile(10, 14, "grs_f"),
    Tile(7, 13, "grs_f"),
    Tile(8, 13, "grs_f"),
    Tile(9, 13, "grs_f"),
    Tile(10, 13, "grs_f"),
    Tile(7, 12, "grs_f"),
    Tile(8, 12, "grs_f"),
    Tile(9, 12, "grs_f"),
    Tile(10, 12, "grs_f"),
    Tile(7, 11, "grs_f"),
    Tile(8, 11, "grs_f"),
    Tile(9, 11, "grs_f"),
    Tile(10, 11, "grs_f"),
    Tile(20, 14, "grs_f"),
    Tile(21, 14, "grs_f"),
    Tile(22, 14, "grs_f"),
    Tile(21, 13, "grs_f"),
    Tile(22, 13, "grs_f"),
    Tile(22, 12, "grs_f"),
    Tile(0, 10, "plf_wd_lft", True),
    Tile(1, 10, "plf_wd_mid", True),
    Tile(2, 10, "plf_wd_rht", True),  
                        ]      
    
    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    items = pygame.sprite.Group()
    tiles = pygame.sprite.Group()

    ''' Add sprites to groups '''
    player.add(hero)

    for t in preped_tiles:
        tiles.add(t)
    
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
                if event.key == pygame.K_UP:
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

    world_x, world_y = calculate_offset()
            
    # Drawing code
    world.fill(SKY_BLUE)
    player.draw(world)
    tiles.draw(world)
    items.draw(world)
    screen.blit(world, [world_x, world_y])
        
    if stage == START:
        show_title_screen()        
    elif stage == END:
        show_end_screen()

    
    # Update screen
    pygame.display.flip()
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
