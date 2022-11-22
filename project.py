import pygame
import random

#Use 2D vectors
vector = pygame.math.Vector2

pygame.init()

#Set display surface (tile size is 32x32 so 960/32 = 30 tiles wide, 640/32 = 20 tiles high)
WINDOW_WIDTH = 800 #prev 900
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Dragon")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Set game values
score = 0
score_list = []
life = 1

#Set fonts
font = pygame.font.SysFont('Arial', 32, True)

#Set text
score_text = font.render("Score: " + str(score), True, (255, 255, 255))
score_rect = score_text.get_rect()
score_rect.topleft = (20, 10)

start_text = font.render("PRESS SPACE BAR TO JUMP", True, (255, 255, 255), (0, 0, 0))
start_text_rect = start_text.get_rect()
start_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100)

game_over_text = font.render("GAME OVER", True, (255, 255, 255))
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("PRESS ANY KEY TO CONTINUE", True, (255, 255, 255))
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50)

#Space Counter - to start the game with space key press
space_counter = 0

#Block sizes and counter
block_counter = 0
BLOCK_SIZE = (50, 100, 150, 200, 250, 300, 350)
BLOCK_STARTING_VELOCITY = 3

GAP_WIDTH = 150
GAP = WINDOW_HEIGHT - GAP_WIDTH

#Define classes

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, block_group):
        super().__init__()
    
        self.animation = []
        self.animation.append(pygame.transform.scale(pygame.image.load("dragon.png"), (66,43)))
        self.animation.append(pygame.transform.scale(pygame.image.load("dragon2.png"), (66,43)))
        
        self.current_sprite = 0
        self.image = self.animation[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.starting_x = x
        self.starting_y = y

        #Kinematics vectors (first value is the x, second value is the y)
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        #Kinematic constants
        self.VERTICAL_ACCLERATION = 0
        self.VERTICAL_JUMP_SPEED = 5 #Determines how high we can jump

        self.block_group = block_group

    def update(self):              
        self.animate(self.animation, 0.02)
    
        #Vertical accelration (gravity) is present always regardless of key-presses
        if space_counter == 1:
            self.VERTICAL_ACCLERATION = .20 #Gravity

        self.acceleration = vector(0, self.VERTICAL_ACCLERATION)

        #Calculate new kinematics values
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5*self.acceleration

        #Update new rect based on kinematic calculations
        self.rect.bottomleft = self.position

        self.check_collisions()

    def animate(self, sprite_list, speed):
        #Loop through the sprite list changing the current sprite
        if self.current_sprite <= 1:
            self.image = sprite_list[0]
            self.current_sprite += speed
        
        elif self.current_sprite > 1:
            self.current_sprite -= 0.4*speed
            self.image = sprite_list[1]
    
    def jump(self):
        self.velocity.y = -1*self.VERTICAL_JUMP_SPEED

    def check_collisions(self):
        global life

        if pygame.sprite.spritecollide(self, self.block_group, True):
            life = 0
        
        if self.rect.y <= 0 or self.rect.y >= WINDOW_HEIGHT:
            life = 0
        
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, image, block_height, block_velocity, player_starting_x):
        super().__init__()
        self.block_height = block_height

        self.image = pygame.transform.scale(pygame.image.load(image), (50, self.block_height)) # random block size
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.player_starting_x = player_starting_x

        self.block_velocity = block_velocity

    def update(self):
        self.move()
        self.score()
    
    def move(self):
        #Move the block
        global block_counter

        if self.rect.x <= 0:
            self.rect.x = WINDOW_WIDTH*2
            self.block_velocity = 0
            block_counter += 0.5

            if block_counter % 1 == 0:
                add_block(random.choice(BLOCK_SIZE))

        else:
            self.rect.x -= self.block_velocity
        
    def score(self):
        global score
        global block_counter

        if self.rect.x <= 0: #player_starting_x = 200    
            score += 50


#Main game loop
def main():
    global space_counter
    global score
    global life
    global block_group
    global my_player_group
    global my_player

    #Load in a background image
    background_image = pygame.image.load("BG.png")
    background_rect = background_image.get_rect()
    background_rect.topleft = (0, 0)

    #Load block
    block_group = pygame.sprite.Group()
    add_block(random.choice(BLOCK_SIZE))

    #Load the player
    my_player_group = pygame.sprite.Group()
    my_player = Player(200, WINDOW_HEIGHT//2, block_group)
    my_player_group.add(my_player)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #Player wants to jump
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and space_counter == 0: # Hit space to start
                    score = 0
                    space_counter = 1
                elif event.key == pygame.K_SPACE and space_counter == 1: # Normal hit space to jump
                    my_player.jump()       
        
        #Blit the background
        display_surface.blit(background_image, background_rect)

        if space_counter == 0:
            display_surface.blit(start_text, start_text_rect)
        
        #Blit the block
        block_group.update()
        block_group.draw(display_surface)

        #Update Score
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        display_surface.blit(score_text, score_rect)

        #Blit the player
        my_player_group.update()
        my_player_group.draw(display_surface)

        #Game over
        if life == 0:
            score_list.append(score)

            block_group.empty()
            my_player_group.empty()

            display_surface.blit(game_over_text, game_over_text_rect)
            display_surface.blit(continue_text, continue_text_rect)

            pygame.display.update()

            is_paused = True
            while is_paused:
                for event in pygame.event.get():
                    #Player wants to play again
                    if event.type == pygame.KEYDOWN:
                        score = 0
                        life = 1
                        space_counter = 1

                        block_group = pygame.sprite.Group()
                        add_block(random.choice(BLOCK_SIZE))

                        my_player_group = pygame.sprite.Group()
                        my_player = Player(200, WINDOW_HEIGHT//2, block_group)
                        my_player_group.add(my_player)

                        is_paused = False
                    
                    if event.type == pygame.QUIT:
                        is_paused = False
                        running = False

        #Update display and tick clock
        pygame.display.update()
        clock.tick(FPS)

    #End the game
    pygame.quit()

    print(final_score(score))
    print(highest_score(score_list))
    print(total_score(score_list))

#Add extra blocks
def add_block(block_top_height):
    global score

    block_group.add(Block(WINDOW_WIDTH, 0, "block_100.png", block_top_height, BLOCK_STARTING_VELOCITY + score / 500, 200)) # top block
    block_group.add(Block(WINDOW_WIDTH, WINDOW_HEIGHT - (GAP - block_top_height), "block_100.png", (GAP - block_top_height), BLOCK_STARTING_VELOCITY + score / 500, 200)) # bottom block

#Show final score
def final_score(score):    
    return f"Well done! Your score was {score}!"

#Show highest score
def highest_score(scorelist):
    if len(scorelist) == 0:
        return f"Your highest score in this session was 0!"
    else:
        return f"Your highest score in this session was {max(scorelist)}!"

def total_score(scorelist):
    return f"Your total score in this playing session was {sum(scorelist)}!"

if __name__ == "__main__":
    main()