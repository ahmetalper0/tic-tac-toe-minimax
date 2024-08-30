from random import uniform
from time import sleep
from sys import exit
import pygame

pygame.init()

#-------------------------------------------------- << GAME CLASS >> --------------------------------------------------#

class Game:

    def __init__(self):

        self.table = self.generate_table()
        self.current_player = 'X'
        self.current_text_image = human_text_image
        self.game_over = False
        self.winner = None
        self.winning_combo = None

    def generate_table(self):

        table = []

        index = 0

        for row in range(3):

            for column in range(3):

                x = 10 + 160 * column
                y = 70 + 160 * row

                table.append({'x' : x, 'y' : y, 'rect' : pygame.Rect(x, y, 150, 150), 'index' : index, 'value' : '-'})

                index += 1

        return table
    
    def is_game_over(self):

        win_combinations = [

            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6] 

        ]

        for combo in win_combinations:

            if (self.table[combo[0]]['value'] == self.table[combo[1]]['value'] == self.table[combo[2]]['value'] != '-'):

                self.game_over = True
                self.winner = self.table[combo[0]]['value']
                self.winning_combo = combo

                if self.winner == 'X':

                    self.current_text_image = win_text_image

                if self.winner == 'O':

                    self.current_text_image = lose_text_image

                return
        
        if all(cell['value'] != '-' for cell in self.table):   

            self.game_over = True
            self.winner = 'draw'
            self.current_text_image = draw_text_image

    def make_move(self, index):

        self.table[index]['value'] = self.current_player

        self.current_player = 'X' if self.current_player == 'O' else 'O'
        self.current_text_image = human_text_image if self.current_player == 'X' else ai_text_image

        self.is_game_over()

    def get_empty_cells(self):

        return [index for index,cell in enumerate(self.table) if cell['value'] == '-']
    
    def reset_game(self):

        self.__init__()

#-------------------------------------------------- << AI CLASS >> --------------------------------------------------#

class AI:

    def minimax(self, game, depth, is_maximizing):

        game_copy = Game()

        game_copy.table = [cell.copy() for cell in game.table]
        game_copy.current_player = game.current_player
        
        game_copy.is_game_over()

        if game_copy.winner == 'X':

            return -1
            
        elif game_copy.winner == 'O':

            return 1
            
        elif game_copy.winner == 'draw':

            return 0
        
        if is_maximizing:

            best_score = float('-inf')

            for index in game_copy.get_empty_cells():

                game_copy.table[index]['value'] = 'O'

                game_copy.is_game_over()

                score = self.minimax(game_copy, depth + 1, False)

                game_copy.table[index]['value'] = '-'

                game_copy.game_over = False
                game_copy.winner = None

                best_score = max(score, best_score)

            return best_score
        
        else:

            best_score = float('inf')

            for index in game_copy.get_empty_cells():

                game_copy.table[index]['value'] = 'X'

                game_copy.is_game_over()

                score = self.minimax(game_copy, depth + 1, True)

                game_copy.table[index]['value'] = '-'

                game_copy.game_over = False
                game_copy.winner = None

                best_score = min(score, best_score)

            return best_score

    def get_best_move(self, game):

        best_score = float('-inf')
        best_move = None

        for index in game.get_empty_cells():

            game_copy = Game()
            
            game_copy.table = [cell.copy() for cell in game.table]
            game_copy.current_player = game.current_player

            game_copy.table[index]['value'] = 'O'

            game_copy.is_game_over()

            score = self.minimax(game_copy, 0, False)

            if score > best_score:

                best_score = score
                best_move = index

        return best_move

#-------------------------------------------------- << PYGAME VARIABLES >> --------------------------------------------------#

SCREEN_WIDTH = 490
SCREEN_HEIGHT = 550

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)

clock = pygame.time.Clock()

ai_image = pygame.image.load('images/ai_image.png') # 150x150
human_image = pygame.image.load('images/human_image.png') # 150x150
ai_text_image = pygame.image.load('images/ai_text_image.png') # 470 x 50
human_text_image = pygame.image.load('images/human_text_image.png') # 470 x 50
win_text_image = pygame.image.load('images/win_text_image.png') # 470 x 50
lose_text_image = pygame.image.load('images/lose_text_image.png') # 470 x 50
draw_text_image = pygame.image.load('images/draw_text_image.png') # 470 x 50

border_background_color = '#303030'

game_reset_time = 2 # seconds

game = Game()

ai = AI()

#-------------------------------------------------- << PYGAME FUNCTIONS >> --------------------------------------------------#

def draw():

    screen.fill(border_background_color)

    screen.blit(game.current_text_image, (10, 10))

    for cell in game.table:

        if cell['value'] == '-':

            pygame.draw.rect(screen, '#d9d9d9', cell['rect'])

        if cell['value'] == 'X':

            screen.blit(human_image, cell['rect'])
            
        if cell['value'] == 'O':

            screen.blit(ai_image, cell['rect'])
            
    if game.winning_combo and game.game_over:

        start = game.table[game.winning_combo[0]]
        end = game.table[game.winning_combo[2]]

        start_pos = (start['x'] + 75, start['y'] + 75)
        end_pos = (end['x'] + 75, end['y'] + 75)
        
        pygame.draw.line(screen, '#ff0000', start_pos, end_pos, 10)
        
def check_game_result():

    if game.game_over:

        print('Game Over!')

        if game.winner == 'Draw':

            print('The game is a draw!')

        else:

            print(f'Winner : {game.winner}')

        print(f'Resetting the game in {game_reset_time} second...\n')

        pygame.time.wait(game_reset_time * 1000)

        game.reset_game()

#-------------------------------------------------- << PYGAME MAIN LOOP >> --------------------------------------------------#

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()

            exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_q:

                pygame.quit()

                exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if not game.game_over:

                for cell in game.table:

                    if cell['rect'].collidepoint(event.pos[0], event.pos[1]):

                        if cell['value'] == '-':

                            game.make_move(cell['index'])

                            if not game.game_over:

                                draw()

                                pygame.display.update()

                                sleep(uniform(0.1, 0.3))

                                ai_move = ai.get_best_move(game)

                                game.make_move(ai_move)

    draw()

    pygame.display.update()

    check_game_result()

    clock.tick(60)
