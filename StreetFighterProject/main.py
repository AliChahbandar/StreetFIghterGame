import pygame
from pygame import mixer
from fighter import Fighter #from file fighter import Fighter class

mixer.init()
pygame.init()


#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Street Fighter')

#cap the frame rate
clock = pygame.time.Clock()
FPS = 60

#def colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE =(255, 255, 255)

#game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0] #player scores p1 p2
round_over = False
ROUND_OVER_COOLDOWN =2000

#fighter variables
WARRIOR_SIZE =162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA =[WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZZARD_SIZE =250
WIZZARD_SCALE = 3
WIZZARD_OFFSET = [112, 107]
WIZZARD_DATA = [WIZZARD_SIZE, WIZZARD_SCALE, WIZZARD_OFFSET]

#music and sound
pygame.mixer.music.load("audio/music.mp3")
pygame.mixer.music.set_volume(.05)
pygame.mixer.music.play(-1,0.0, 5000)
#sound effects
sword_fx = pygame.mixer.Sound("audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("audio/magic.wav")
magic_fx.set_volume(.75)


#Load background image 
bg_image = pygame.image.load("images/background/background.jpg").convert_alpha() #loads the image 


#load spritesheets
warrior_sheet = pygame.image.load("images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("images/wizard/Sprites/wizard.png").convert_alpha()


victory_img = pygame.image.load("images/icons/victory.png").convert_alpha()

#number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS =[8, 8, 1, 8, 8, 3, 7]


#def fonts
count_font = pygame.font.Font("fonts/turok.ttf", 80)
score_font = pygame.font.Font("fonts/turok.ttf", 30)

#draw text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))
#drawing function background
def draw_bg():
    scale_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)) #to make sure the image is scaled to the screen width/height
    screen.blit(scale_bg, (0, 0))

#health bars function
def draw_health_bars(health, x ,y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x-2, y-2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x,y, 400 * ratio, 30))


#create fighter instances
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx) 
fighter_2 = Fighter(2, 700, 310,True, WIZZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)


#game loop
run = True
while run:

    clock.tick(FPS)

    #draw bg
    draw_bg()

    #show player stats
    draw_health_bars(fighter_1.health, 20, 20)
    draw_health_bars(fighter_2.health, 580, 20)
    draw_text("P1: "+ str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: "+ str(score[1]), score_font, RED, 580, 60)

    #intro count
    if intro_count <=0:
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        #display count
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT/3)
        if(pygame.time.get_ticks()- last_count_update) >=1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            

  

    #update    
    fighter_1.update()
    fighter_2.update()
    

    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # check player defeat
    if round_over == False:
        if fighter_1.alive == False:
            score[1]+= 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
            
        elif fighter_2.alive == False:
            score[0]+= 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks()- round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx) 
            fighter_2 = Fighter(2, 700, 310,True, WIZZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

    #add events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    #Update display
    pygame.display.update()

#exit pygame
pygame.quit()
            