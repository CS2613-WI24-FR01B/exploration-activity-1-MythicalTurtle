import pygame, sys, random

#Initialize Pygame
pygame.init()

#Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Colours 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Fonts
pygame.font.init()  # Initialize font module
title_font = pygame.font.SysFont("comicsans", 70)
button_font = pygame.font.SysFont("comicsans", 50)
score_font = pygame.font.SysFont("comicsans", 30)

#Game over fonts
game_over_font = pygame.font.SysFont("comicsans", 70)
options_font = pygame.font.SysFont("comicsans", 50)

#High score
high_score = 0

#Button dimensions and position
button_width = 200
button_height = 100
button_x = SCREEN_WIDTH // 2 - button_width // 2
button_y = SCREEN_HEIGHT // 2 - button_height // 2

#replay buttons
replay_button_width = 200
replay_button_height = 100
replay_button_x = SCREEN_WIDTH // 2 - replay_button_width // 2
replay_button_y = SCREEN_HEIGHT // 2 + 50  #Under the Game Over text

#Player
player_size = 25
player_pos = [SCREEN_WIDTH//2, SCREEN_HEIGHT-2*player_size]
player_speed = 0.5

#Enemy
enemy_size = 15
enemy_speed = 0.8
enemy_pos = [random.randint(0, SCREEN_WIDTH-enemy_size), 0]
enemy_list = [{"pos": enemy_pos, "speed": enemy_speed}]

#Bullet
bullet_height = 20
bullet_width = 10
bullet_speed = 20
bullet_list = []

#Load images
player_image = pygame.image.load('player.gif').convert_alpha()
enemy_image = pygame.image.load('enemy.png').convert_alpha()

#Scale Images
player_image = pygame.transform.scale(player_image, (player_size, player_size))
enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))

score = 0
game_state = "menu" #Possible states: "menu", "playing", "game_over"

def drop_enemies(enemy_list):
    delay = random.random()
    #Adjust spawn threshold based on score
    threshold = max(0.1 - (score // 5) * 0.01, 0.02)
    #Increase max enemies on screen based on score
    max_enemies = 10 + (score // 50)
    
    if len(enemy_list) < max_enemies and delay < threshold:
        #Choose spawn side based on score, with new sides introduced at higher scores
        side = random.choice(['top', 'left', 'right', 'bottom']) if score > 1000 else 'top'
        x_pos, y_pos = get_spawn_position(side)
        #Create enemy with varied speed
        enemy_speed = 0.5 + (score // 5000) * 0.05
        enemy_list.append({"pos": [x_pos, y_pos], "speed": enemy_speed, "type": "bullet", "side": side})
    
        if score > 150:
            #spawn bullet enemies from all sides
            side = random.choice(['top', 'left', 'right', 'bottom'])
            x_pos, y_pos = get_spawn_position(side)
            bullet_enemy_speed = 0.5 + (score // 5000) * 0.05 
            enemy_list.append({"pos": [x_pos, y_pos], "speed": bullet_enemy_speed, "type": "bullet", "side": side})


def get_spawn_position(side):
    if side == 'top':
        return random.randint(0, SCREEN_WIDTH - enemy_size), 0
    elif side == 'left':
        return 0, random.randint(0, SCREEN_HEIGHT - enemy_size)
    elif side == 'right':
        return SCREEN_WIDTH - enemy_size, random.randint(0, SCREEN_HEIGHT - enemy_size)
    elif side == 'bottom':
        return random.randint(0, SCREEN_WIDTH - enemy_size), SCREEN_HEIGHT - enemy_size



#Creates enemy
def draw_enemies(enemy_list):
    for enemy in enemy_list:
        enemy_pos = enemy["pos"]
        screen.blit(enemy_image, enemy_pos)
        #pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

#Changes the position of an enemy
def update_enemy_positions(enemy_list, score):
    for enemy in enemy_list[:]:
        #non-bullet enemies simply move downwards, no 'side' key needed
        if 'type' in enemy and enemy['type'] == "bullet":
            side = enemy.get("side", "top")  #Defaults to "top" if 'side' key doesn't exist
            if side == "top":
                enemy["pos"][1] += enemy["speed"]
            elif side == "bottom":
                enemy["pos"][1] -= enemy["speed"]
            elif side == "left":
                enemy["pos"][0] += enemy["speed"]
            elif side == "right":
                enemy["pos"][0] -= enemy["speed"]
            # Additional logic for other sides
        else:
            enemy["pos"][1] += enemy["speed"]

        #Remove enemy if it goes off-screen
        if enemy["pos"][1] >= SCREEN_HEIGHT or enemy["pos"][1] < 0 or enemy["pos"][0] >= SCREEN_WIDTH or enemy["pos"][0] < 0:
            enemy_list.remove(enemy)
            score += 1
    return score


#Checks if an enemy has hit the player
def detect_collision(enemy, player_pos):
    e_x, e_y = enemy["pos"]  #Extracting enemy position
    p_x, p_y = player_pos

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

def collision_check(enemy_list, player_pos):
    for enemy in enemy_list:
        if detect_collision(enemy, player_pos):
            return True
    return False


def show_score(score):
    font = pygame.font.SysFont("monospace", 35)
    score_text = "Score: " + str(score)
    label = font.render(score_text, 1, WHITE)
    screen.blit(label, (SCREEN_WIDTH - 200, SCREEN_HEIGHT -40))

def main_menu():
    global game_state  #Access the global game_state variable
    menu_running = True
    while menu_running:
        draw_main_menu(high_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"  #Return a state indicating the game should quit
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    game_state = "playing"  #Update game state to start playing
                    menu_running = False
    return game_state


def draw_main_menu(high_score):
    screen.fill(BLACK)
    #Title
    title_text = title_font.render("My Game", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
    
    #Play Button
    pygame.draw.rect(screen, GREEN, (button_x, button_y, button_width, button_height))
    button_text = button_font.render("Play", True, BLACK)
    screen.blit(button_text, (button_x + button_width // 2 - button_text.get_width() // 2, button_y + button_height // 2 - button_text.get_height() // 2))
    
    #High Score
    high_score_text = score_font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (10, 10))

    pygame.display.update()

def draw_game_over_menu():
    screen.fill(BLACK)
    #Game over text on screen
    game_over_text = game_over_font.render("Game Over", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2 - 50))
    
    #Replay/ play again button
    pygame.draw.rect(screen, GREEN, (replay_button_x, replay_button_y, replay_button_width, replay_button_height))
    replay_text = options_font.render("Replay", True, BLACK)
    screen.blit(replay_text, (replay_button_x + replay_button_width // 2 - replay_text.get_width() // 2, replay_button_y + replay_button_height // 2 - replay_text.get_height() // 2))
    
    pygame.display.update()

def game_over_screen():
    global game_state
    game_over_running = True
    while game_over_running:
        draw_game_over_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Define replay_button bounds as you did for the play button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if replay_button_x <= mouse_x <= replay_button_x + replay_button_width and replay_button_y <= mouse_y <= replay_button_y + replay_button_height:
                    game_state = "menu"  #Or directly "playing" if restarting the game
                    game_over_running = False
    return game_state


def game_loop():
    global score, player_pos, enemy_list, game_state  #Access global variables
    #Initialize/reset game state variables as needed
    score = 0
    player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_size]
    enemy_list = [{"pos": [random.randint(0, SCREEN_WIDTH - enemy_size), 0], "speed": enemy_speed}]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
    
        #Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed

        if keys[pygame.K_RIGHT] and player_pos[0] + player_size < SCREEN_WIDTH:
            player_pos[0] += player_speed
            
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= player_speed

        if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT-player_size:
            player_pos[1] += player_speed
            

        screen.fill(BLACK)

        #Enemy updates
        drop_enemies(enemy_list)
        score = update_enemy_positions(enemy_list, score)
        draw_enemies(enemy_list)
        
        
        #Display in-game
        show_score(score)
        

        screen.blit(player_image, player_pos)
        #pygame.draw.rect(screen, WHITE, (player_pos[0], player_pos[1], player_size, player_size))
        pygame.display.update()
            
        #Check for collision with player
        if collision_check(enemy_list, player_pos):
            game_state = "game_over"
            return game_state  #Return to transition to the game over screen
        
while True:
    if game_state == "menu":
        game_state = main_menu()
    elif game_state == "playing":
        game_state = game_loop()
    elif game_state == "game_over":
        if (score > high_score):
            high_score = score
        game_state = game_over_screen()
    elif game_state == "quit":
        pygame.quit()
        sys.exit()

