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

#Player
player_size = 16
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


score = 0

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
        pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

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


#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
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
    

    #Check for collision with player
    if collision_check(enemy_list, player_pos):
        print(f"Game Over! Your final score is {score}.")
        pygame.quit()
        sys.exit()
    
    #Display
    show_score(score)


    pygame.draw.rect(screen, WHITE, (player_pos[0], player_pos[1], player_size, player_size))
    pygame.display.update()