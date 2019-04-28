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
        
        self.reset()

    '''
        Déplace la tête et le reste du corps en fonction de l'action du joueur
    '''
    def do_move(self, action):
        new_position = [0,0]
        reward = 0

        self.screen.fill(self.white)


        '''
            Déplacement des body en fonction du body "parent"
        '''
        nb_players = len(self.players)
        for i in range(1, nb_players):
            body = self.players[nb_players - i]
            body_parent = self.players[nb_players - i - 1]
            bp_pos = body_parent['actual_position']
            body= self.new_body(bp_pos[0], bp_pos[1], body_parent['actual_direction'])

            self.players[len(self.players)-i] = body

            body_player = pygame.image.load("img/player_case.gif")
            body_rect = body_player.get_rect()
            body_rect.move_ip(body_parent['actual_position'])
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


        self.players[0] = player

        player_image = pygame.image.load("img/player_case.gif")
        player_rect = player_image.get_rect()
        player_rect.move_ip(player['actual_position'])

        self.screen.blit(player_image, player_rect)

        reward = self.get_reward()

        if(reward > 0):
            self.score += 1
            self.add_player_body()
            self.food = self.get_food_position()

        self.show_food()

        if(self.display):
            pygame.display.flip()

        return self.get_observation()

    def show_food(self):
        food_image = pygame.image.load("img/food_case.gif")
        food_rect = food_image.get_rect()
        food_rect.move_ip(self.food)
        self.screen.blit(food_image, food_rect)

    def get_score(self):
        return self.score

    def new_body(self, x=0, y=0, direction='LEFT'): 
        return {
            'actual_position': [x,y],
            'actual_direction': direction
        }

    def add_player_body(self):
        nb_players = len(self.players)
        body_architecture = self.new_body()

        if(nb_players > 0):
            last_body = self.players[nb_players - 1]
            free = self.get_body_free_space(nb_players - 1)
            key, value = random.choice(list(free.items()))
            body_architecture['actual_position'] = value
        else:
            body_architecture['actual_position'] = [int(self.screen_size/2), int(self.screen_size/2)]

        self.players.append(body_architecture)

    def get_food_position(self):
        x = int(random.randrange(0, self.screen_size, self.CASE_SIZE))
        y = int(random.randrange(0, self.screen_size, self.CASE_SIZE))

        return [x,y]

    def get_body_free_space(self, body_index):
        pos = self.players[body_index]['actual_position']
        up    = [pos[0]                             , pos[1] + self.DIRECTIONS['UP'][1]]
        left  = [pos[0] + self.DIRECTIONS['LEFT'][0], pos[1]]
        down  = [pos[0]                             , pos[1] + self.DIRECTIONS['DOWN'][1]]
        right = [pos[0] + self.DIRECTIONS['RIGHT'][0], pos[1]]

        free = {}

        # On contrôle d'abord les bordures
        if(self.control_border(up)):
            free['UP'] = up
        elif(self.control_border(left)):
            free['LEFT'] = left
        elif(self.control_border(down)):
            free['DOWN'] = down
        elif(self.control_border(right)):
            free['RIGHT'] = right

        for i in range(len(self.players)):
            pos = self.players[i]['actual_position']
            if(i != body_index):
                for key in free:
                    coord = free[key]
                    if(coord[0] == pos[0] and coord[1] == pos[1]):
                        del free[key]
        return free

    def get_reward(self):
        player = self.players[0]
        reward = -1

        pos = player['actual_position']
        if(pos[0] == self.food[0] and pos[1] == self.food[1]):
            # Check if player touch food
            reward = 100
        elif(pos[0] < 0 or pos[0] >= self.screen_size or pos[1] < 0 or pos[1] >= self.screen_size):
            # Check if player is on the border
            reward = -100
        else:
            # Check if player touch hiself
            for i in range(len(self.players)):
                pos_body = self.players[i]['actual_position']
                if(i != 0 and (pos_body[0] == pos[0] and pos_body[1] == pos[1])):
                    reward = -100
                    break

        return reward

    def reset(self):
        self.score = 0

        self.players = []

        self.add_player_body()

        player = self.players[0]
        player_image = pygame.image.load("img/player_case.gif")
        player_rect = player_image.get_rect()
        player_rect.move_ip(player['actual_position'])

        self.screen.fill(self.white)
        self.screen.blit(player_image, player_rect)

        self.food = self.get_food_position()

        self.show_food()

        if(self.display):
            pygame.display.flip()

    def control_border(self, pos):
        in_game_screen = True
        if(pos[0] < 0 or pos[0] >= self.screen_size):
            in_game_screen = False

        return in_game_screen

    def get_actions_set(self):
        return self.ACTIONS

    def get_observation(self):
        player = self.players[0]['actual_position']
        p_x = int(player[0]/self.CASE_SIZE) + 1
        p_y = int(player[1]/self.CASE_SIZE) + 1

        food = self.food
        f_x = int(food[0]/self.CASE_SIZE) + 1
        f_y = int(food[1]/self.CASE_SIZE) + 1

        return {'snake_location': [p_x, p_y], 'food_location': [f_x, f_y], 'reward': self.get_reward()}