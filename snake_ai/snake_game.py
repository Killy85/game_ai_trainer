import sys, pygame
import random

class Snake:

    ACTIONS = [0, 1, 2]

    DIRECTIONS = {
        'UP':       [0, -10],
        'DOWN':     [0, 10],
        'LEFT':     [-10, 0],
        'RIGHT':    [10, 0]
    }

    CASE_SIZE = 10

    '''
        Initialisation du jeu
    '''
    def __init__(self, nb_cases, display=True):
        pygame.init()
        self.display = display
        self.screen_size = nb_cases * self.CASE_SIZE
        size = width, height = self.screen_size, self.screen_size
        self.white = 255, 255, 255
        self.screen = pygame.display.set_mode(size)
        self.score = 0

        self.players = []
        self.add_player_body()
        player = self.players[0]
        player_image = pygame.image.load("img/player_case.gif")
        player_rect = player_image.get_rect()
        player_rect.move_ip(player['actual_position'])
        self.screen.fill(self.white)
        self.screen.blit(player_image, player_rect)

        self.food = [random.randrange(),random.randrange()]

        if(self.display):
            pygame.display.flip()


    '''
        Déplace la tête et le reste du corps en fonction de l'action du joueur
    '''
    def do_move(self, action):
        new_position = [0,0]
        reward = 0

        '''
            Déplacement des body en fonction du body "parent"
        '''
        for i in range(len(self.players) - 1, 0):
            body = self.players[i]
            body_player = pygame.image.load("img/player_case.gif")
            body_rect = body_player.get_rect()
            self.screen.fill(self.white)
            self.screen.blit(body_player, body_rect)

        '''
            Déplacemement du player en fonction de l'action, de sa position et de sa direction
        '''
        player = self.players[0]
        direction = player['actual_direction']
        if(action == self.ACTIONS[1]):
            
            if(direction == 'UP'):
                player['actual_direction'] = 'LEFT'
            elif(direction == 'LEFT'):
                player['actual_direction'] = 'DOWN'
            elif(direction == 'DOWN'):
                player['actual_direction'] = 'RIGHT'
            elif(direction == 'RIGHT'):
                player['actual_direction'] = 'UP'

        elif(action == self.ACTIONS[2]):
            
            if(direction == 'UP'):
                player['actual_direction'] = 'RIGHT'
            elif(direction == 'LEFT'):
                player['actual_direction'] = 'UP'
            elif(direction == 'DOWN'):
                player['actual_direction'] = 'LEFT'
            elif(direction == 'RIGHT'):
                player['actual_direction'] = 'DOWN'

        player['actual_position'][0] += self.DIRECTIONS[player['actual_direction']][0]
        player['actual_position'][1] += self.DIRECTIONS[player['actual_direction']][1]

        player_image = pygame.image.load("img/player_case.gif")
        player_rect = player_image.get_rect()
        player_rect.move_ip(player['actual_position'])

        self.screen.fill(self.white)
        self.screen.blit(player_image, player_rect)

        if(self.display):
            pygame.display.update()

        reward = self.get_reward()

        if(reward > 0):
            

        return {'state': player['actual_position'], 'reward': reward}

    def score():
        return self.score

    def add_player_body(self):
        nb_players = len(self.players)
        body_architecture = {
            'actual_position': [0,0],
            'actual_direction': 'LEFT'
        }

        if(nb_players > 0):
            last_body = self.players[nb_players - 1]
            free = self.get_body_free_space(nb_players - 1)
            if(free > 1):
                print('RANDOM')
            else:
                print('ONLY')
        else:
            body_architecture['actual_position'] = [self.screen_size/2, self.screen_size/2]

        self.players.append(body_architecture)

    def get_food_position(self):
        x = random.randrange(0, self.screen_size, self.CASE_SIZE)
        y = random.randrange(0, self.screen_size, self.CASE_SIZE)
        return 

    def get_body_free_space(self, body_index):
        free = self.ACTIONS
        for i in range(len(self.players)):
            if(i != body_index):
                print('poof')
        return free

    def get_reward(self):
        player = self.players[0]
        reward = 0

        pos = player['actual_position']
        if(pos[0] == self.food[0] && pos[1] == self.food[1]):
            # Check if player touch food
            reward = 1
        elif(pos[0] < 0 || pos[0] > self.screen_size || pos[1] < 0 || pos[1] > self.screen_size):
            # Check if player is on the border
            reward = -1
        else:
            # Check if player touch hiself
            for i in range(self.players):
                pos_body = self.players[i]['actual_position']
                if(i != body_index && (pos_body[0] == pos[0] && pos_body[1] == pos[1])):
                    reward = -1
                    break

        return reward