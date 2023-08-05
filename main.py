import pygame, json
from sys import exit
from random import randrange

pygame.init()
SCREEN = pygame.display.set_mode((600,500))
pygame.display.set_caption("Snake game")
CLOCK = pygame.time.Clock()

class Body():
    '''Snake body, it has a rectangle to position it on screen,
    speed of movement and direction to indicate where it will move'''
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,25,25)
        self.speed = 25
        self.direction = 'x'

class Objective():
    '''The objective that the snake needs to collect to grow,
    it only has a rectangle to position it on screen'''
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,25,25)

def check_collisions(snake,head_direction,head_speed):
    '''Brief: Checks collisions with screen boundaries and the snake itself.

    Parameters:
        - head_direction: axis where the next movement will be made.
        - head_speed: amount of pixels that the snake will move.
    
    return: 'True' in case the snake collisions or 'False' otherwise.'''
    rtn = False
    for i in range(len(snake)-1):
        if snake[-1].rect.colliderect(snake[i]):
            rtn = True
    if rtn == False:
        if head_direction == 'x':
            if snake[-1].rect.x + head_speed < 0 or\
                snake[-1].rect.x + head_speed > 575:
                rtn = True
        else:
            if snake[-1].rect.y + head_speed < 50 or\
                snake[-1].rect.y + head_speed > 475:
                rtn = True
    return rtn

def body_movement(snake, head_direction, head_speed):
    '''Brief: Moves every part of the body to their next position.

    Parameters:
        - snake: list of Body objects indicating their positions on screen.
        - head_direction: axis where the movement will be done.
        - head_speed: amount of pixels that the snake will move.'''
    for i in range(len(snake)):
        if i != len(snake)-1:
            snake[i].speed = snake[i+1].speed
            snake[i].direction = snake[i+1].direction
        else:
            snake[i].speed = head_speed
            snake[i].direction = head_direction

        if snake[i].direction == 'x':
            snake[i].rect.x += snake[i].speed
        else:
            snake[i].rect.y += snake[i].speed

def spawn_objective(snake,objective:Objective,first):
    '''Brief: Moves every part of the body to their next position.

    Parameters:
        - snake: list of Body objects indicating their positions on screen.
        - objective: the objective that will spawn.
        - first: bool to indicate if it's the first objective spawning in.'''
    find_flag = True
    while find_flag:
        objective_x = randrange(50,600,25)
        objective_y = randrange(50,500,25)
        objective.rect = pygame.Rect(objective_x,objective_y,25,25)
        find_flag = False
        for part in snake:
            if part.rect.colliderect(objective.rect):
                find_flag = True
    if not first:
        if snake[0].direction == 'x':
            snake.insert(0,Body(snake[0].rect.x-snake[0].speed,
                                snake[0].rect.y))
        else:
            snake.insert(0,Body(snake[0].rect.x,
                                snake[0].rect.y-snake[0].speed))

def create_file_json(path):
    '''Brief: Tries to open the file and if it's not possible it will create it.

    Parameters:
        - path: indicates the path where the file is located.'''
    try:
        with open(path) as file:
            pass
    except:
        with open(path,'w') as file:
            scores = {
                "best score":0
            }
            json.dump(scores,file,indent=4)

def set_scores_json(score):
    '''Brief: Sets the new score only if this one it's better than the old one.

    Parameters:
        - score: the new score made by the player.'''
    try:
        with open("scores.json",'r') as file:
            data = json.load(file)
        
        with open("scores.json",'w') as file:
            if data['best score'] < score:
                data['best score'] = score
            json.dump(data,file,indent=4)
    except Exception as e:
        print(e)

def get_data_json(path):
    '''Brief: Gets the data from a file and returns it.

    Parameters:
        - path: indicates the path where the file is located.
    
        return: the data obtained from the file or 'None' otherwise.'''
    data = None
    try:
        with open(path,'r') as file:
            data = json.load(file)
    except Exception as e:
        print(e)
    return data

create_file_json("scores.json")
font = pygame.font.Font("resources/pixeltype.ttf",60)
best_score = None

# Main menu
title_surf = font.render("Snake  game",False,"Green")
x,y = title_surf.get_size()
title_surf = pygame.transform.scale(title_surf,(x*2,y*2))
title_rect = title_surf.get_rect(center = (300,150))
play_surf = font.render("Play",False,"Green")
play_rect = play_surf.get_rect(center = (300,300))
quit_surf = font.render("Quit",False,"Green")
quit_rect = quit_surf.get_rect(center = (300,400))
main_menu = True

    # SFX
select_sfx = pygame.mixer.Sound("resources/select sfx.mp3")

# Game
snake = [Body(50,100),Body(75,100),Body(100,100)]
head_speed = 25
head_direction = 'x'
fruit = Objective(500,0)
keys_flag = True
game = False
game_delay = 0
score = 0
game_over_surf = font.render("GAME  OVER",False,"Red","Black")
x,y = game_over_surf.get_size()
game_over_surf = pygame.transform.scale(game_over_surf,(x*2,y*2))
game_over_rect = game_over_surf.get_rect(center=(300,250))

    # SFX
eat_sfx = pygame.mixer.Sound("resources/eat sfx.mp3")
eat_sfx.set_volume(0.7)
crash_sfx = pygame.mixer.Sound("resources/crash sfx.mp3")
crash_sfx.set_volume(0.5)
game_over_sfx = pygame.mixer.Sound("resources/gameover sfx.mp3")
game_over_sfx.set_volume(0.5)

    # Music
music = pygame.mixer.Sound("resources/music.mp3")
music_flag = True
music.set_volume(0.4)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif game:
            if event.type == pygame.KEYDOWN and keys_flag:
                if event.key == pygame.K_RIGHT:
                    if not(head_direction == 'x' and head_speed == -25):
                        head_speed = 25
                        head_direction = 'x'
                        keys_flag = False
                elif event.key == pygame.K_LEFT:
                    if not(head_direction == 'x' and head_speed == 25):
                        head_speed = -25
                        head_direction = 'x'
                        keys_flag = False
                elif event.key == pygame.K_UP:
                    if not(head_direction == 'y' and head_speed == 25):
                        head_speed = -25
                        head_direction = 'y'
                        keys_flag = False
                elif event.key == pygame.K_DOWN:
                    if not(head_direction == 'y' and head_speed == -25):
                        head_speed = 25
                        head_direction = 'y'
                        keys_flag = False
        elif main_menu:
            if event.type == pygame.MOUSEBUTTONDOWN and\
                pygame.mouse.get_pressed()[0]:
                x,y = pygame.mouse.get_pos()
                if play_rect.collidepoint(x,y):
                    select_sfx.play(0)
                    pygame.draw.rect(SCREEN,"gray",play_rect,2)
                    game = True
                    main_menu = False
                    best_score = get_data_json("scores.json")['best score']
                    snake = [Body(50,100),Body(75,100),Body(100,100)]
                    head_speed = 25
                    head_direction = 'x'
                    score = 0
                    spawn_objective(snake,fruit,True)
                    music_flag = True
                elif quit_rect.collidepoint(x,y):
                    pygame.quit()
                    exit()

    if not main_menu:
        if check_collisions(snake,head_direction,head_speed) and game:
            game = False
            game_delay = pygame.time.get_ticks()
            crash_sfx.play(0)
            music.fadeout(1000)
            music_flag = True
            set_scores_json(score)
        if game:
            if music_flag:
                music.play(-1)
                music_flag = False
            body_movement(snake,head_direction,head_speed)
            if snake[-1].rect.colliderect(fruit.rect):
                eat_sfx.play(0)
                spawn_objective(snake,fruit,False)
                score += 1
            
            SCREEN.fill("black")
            pygame.draw.rect(SCREEN,"#b32222",(0,0,600,50))
            SCREEN.blit(font.render(f"Score: {score}",False,"black"),(60,10))
            SCREEN.blit(font.render(f"Best score: {best_score}",False,"black"),(280,10))
            pygame.draw.rect(SCREEN,"red",fruit.rect,2)
            for part in snake:
                if part != snake[-1]:
                    pygame.draw.rect(SCREEN,"#02a9f7",part.rect,2)
                else:
                    pygame.draw.rect(SCREEN,"#0a3bd4",part.rect,2)
        else:
            if pygame.time.get_ticks()-game_delay>1000:
                if music_flag:
                    game_over_sfx.play(0)
                    music_flag = False
                SCREEN.blit(game_over_surf,game_over_rect)
            if pygame.time.get_ticks()-game_delay>3000:
                main_menu = True
    else:
        SCREEN.fill("black")
        SCREEN.blit(title_surf,title_rect)
        SCREEN.blit(play_surf,play_rect)
        SCREEN.blit(quit_surf,quit_rect)
        x,y = pygame.mouse.get_pos()
        if play_rect.collidepoint(x,y):
            select_rect = pygame.Rect(play_rect.x,play_rect.y,play_rect.width+40,play_rect.height+20)
            select_rect.center = play_rect.center
            pygame.draw.rect(SCREEN,"green",select_rect,2)
        elif quit_rect.collidepoint(x,y):
            select_rect = pygame.Rect(quit_rect.x,quit_rect.y,quit_rect.width+40,quit_rect.height+20)
            select_rect.center = quit_rect.center
            pygame.draw.rect(SCREEN,"green",select_rect,2)

    keys_flag = True
    pygame.display.flip()
    CLOCK.tick(8)