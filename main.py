import pygame
from pygame.locals import *
import time
import random


TILE_SIZE = 50
WINDOW_X, WINDOW_Y = 800, 800
WINDOW_COLOR = (224, 232, 162)
UI_COLOR = (53,83,10)
TIMER = 0.10

class Snake:
    def __init__(self, window_screen):
        self.window_screen = window_screen
        self.block = pygame.image.load("assets/sprites/snake_block.png").convert()
        self.direction = 'right'

        self.x, self.y = [TILE_SIZE], [TILE_SIZE]
        self.length = 1

    def grow(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    def draw_snake(self):
        self.window_screen.fill(WINDOW_COLOR)
        pygame.draw.rect(self.window_screen, UI_COLOR, (5, 5, WINDOW_X - 11, WINDOW_Y - 11), 5) 
        for i in range(self.length):
            self.window_screen.blit(self.block, (self.x[i], self.y[i]))

        pygame.display.update()

    def left(self):
        if self.direction == 'right':
            return
        self.direction = 'left'

    def right(self):
        if self.direction == 'left':
            return
        self.direction = 'right'

    def up(self):
        if self.direction == 'down':
            return
        self.direction = 'up'

    def down(self):
        if self.direction == 'up':
            return
        self.direction = 'down'

    def slither(self):
        #Each block follows previous block (like a conveyor belt)
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        

        if self.direction == 'left':
            self.x[0] -= TILE_SIZE

        if self.direction == 'right':
            self.x[0] += TILE_SIZE

        if self.direction == 'up':
            self.y[0] -= TILE_SIZE

        if self.direction == 'down':
            self.y[0] += TILE_SIZE
        
        self.draw_snake()

class Snack:
    def __init__(self, window_screen):
        self.window_screen = window_screen
        self.snack_sprite = pygame.image.load("assets/sprites/snack.png").convert_alpha()
        self.x, self.y = 100, 100

    def spawn(self):
        self.x = random.randint(1, WINDOW_X/TILE_SIZE - 1)*TILE_SIZE
        self.y = random.randint(1, WINDOW_Y/TILE_SIZE - 1)*TILE_SIZE

    def draw_snack(self):
        self.window_screen.blit(self.snack_sprite, (self.x, self.y))
        pygame.display.update()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Snake")
        self.surface = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
        self.snake = Snake(self.surface)
        self.snake.draw_snake()
        self.snack = Snack(self.surface)
        #self.snack.draw_snack()
        
    def reset(self):
        self.snake = Snake(self.surface)
        self.snack = Snack(self.surface)
    
    def play_sound(self, sound_name):
        if sound_name == "game_over":
            sound = pygame.mixer.Sound("assets/sounds/game_over.wav")

        elif sound_name == 'boop':
            sound = pygame.mixer.Sound("assets/sounds/boop.wav")

        pygame.mixer.Sound.play(sound)


    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + TILE_SIZE:
            if y1 >= y2 and y1 < y2 + TILE_SIZE:
                return True

        return False
    
    def display_score(self):
        #displays score
        font = pygame.font.Font('assets/fonts/Pixeled.ttf',15)
        score = (self.snake.length - 1) * 5
        score_txt = font.render(f"Score: {score}",True, UI_COLOR)
        self.surface.blit(score_txt, (15,10))

        #reads high score
        with open('high_score.txt', 'r') as f:
            line = f.readline()
            high_score = int(line.lstrip('high_score = '))

        #Updates high score
        if score > high_score :
            with open('high_score.txt', 'w') as f:
                high_score = score
                f.write('high_score = ' + str(score))
        
        #displays high score
        high_score_txt = font.render(f'High Score: {high_score}', True, UI_COLOR)
        self.surface.blit(high_score_txt, (600, 10))
    
    def play(self):
        self.snake.slither()
        self.snack.draw_snack()
        self.display_score()
        pygame.draw.rect(self.surface, UI_COLOR, (5, 5, WINDOW_X - 11, WINDOW_Y - 11), 5)
        pygame.display.update()

        # snake eats apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.snack.x, self.snack.y):
            self.play_sound("boop")
            self.snake.grow()
            self.snack.spawn()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('game_over')
                raise "Collision Occured"
        
        # snake hits wall
        if not (self.snake.x[0] in range(0,800) and self.snake.y[0] in range(0,800)):
            self.play_sound('game_over')
            raise "Hit the wall"

    def game_over(self):
        self.surface.fill(WINDOW_COLOR)

        font1 = pygame.font.Font('assets/fonts/Pixeled.ttf', 50)
        line1 = font1.render(f"Game Over!", True, UI_COLOR)
        self.surface.blit(line1, (180, 200))

        font2 = pygame.font.Font('assets/fonts/dogica.ttf', 20)
        line2 = font2.render(f"Press enter to play again!", True, UI_COLOR)
        self.surface.blit(line2, (150, 450))

        font3 = pygame.font.Font('assets/fonts/dogica.ttf', 10)
        line3 = font3.render(f'Mohit Kundu 2021', True, UI_COLOR)
        self.surface.blit(line3, (635, 785))

        self.display_score()
        pygame.display.update()

    def run(self):
        running = True
        is_game_over = False

        while running:
            for event in pygame.event.get():

                if event.type == KEYDOWN:
                
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        is_game_over = False

                    if not is_game_over:

                        if event.key == K_LEFT or event.key == K_a:
                            self.snake.left()

                        if event.key == K_RIGHT or event.key == K_d:
                            self.snake.right()

                        if event.key == K_UP or event.key == K_w:
                            self.snake.up()

                        if event.key == K_DOWN or event.key == K_s:
                            self.snake.down()

                elif event.type == QUIT:
                    running = False
            try:

                if not is_game_over:
                    self.play()

            except Exception as e:
                is_game_over = True
                self.game_over()
                self.reset()

            time.sleep(TIMER)

if __name__ == '__main__':
    game = Game()
    game.run()