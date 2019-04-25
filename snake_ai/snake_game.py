import sys, pygame

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
    def __init__(self, nb_cases):
        pygame.init()
        screen_size = nb_cases * self.CASE_SIZE
        size = width, height = screen_size, screen_size
        self.white = 255, 255, 255
        self.screen = pygame.display.set_mode(size)
        self.score = 0

        self.players = []
        add_player_body()
        player = self.players[0]
        player['player_rect'].move_ip(player['actual_position'])
        self.screen.fill(self.white)
        self.screen.blit(self.player, self.player_rect)

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
        for i in range(self.players.len() - 1, 0):
            body = self.players[i]
            self.screen.fill(self.white)
            self.screen.blit(body['player_image'], body['player_rect'])

        '''
            Déplacemement du player en fonction de l'action, de sa position et de sa direction
        '''
        player = self.players[0]
        direction = player['actual_direction']
        if(action == self.ACTIONS.LEFT):
            
            if(direction == 'UP')
                player['actual_direction'] = 'LEFT'
            elif(direction == 'LEFT'):
                player['actual_direction'] = 'DOWN'
            elif(direction == 'DOWN'):
                player['actual_direction'] = 'RIGHT'
            elif(direction == 'RIGHT'):
                player['actual_direction'] = 'UP'

        elif(action == self.ACTIONS.RIGHT):
            
            if(direction == 'UP')
                player['actual_direction'] = 'RIGHT'
            elif(direction == 'LEFT'):
                player['actual_direction'] = 'UP'
            elif(direction == 'DOWN'):
                player['actual_direction'] = 'LEFT'
            elif(direction == 'RIGHT'):
                player['actual_direction'] = 'DOWN'


        player['actual_position'] = player['actual_position'] + DIRECTIONS[player['actual_direction']]
        player['player_rect'].move_ip(player['actual_position'])
        self.screen.fill(self.white)
        self.screen.blit(body['player_image'], body['player_rect'])

        pygame.display.flip()

        reward = get_reward()

        return {state:player['actual_position'], reward: reward}

    def score():
        return self.score

    def add_player_body(self):
        nb_players = self.players.len()
        body_architecture = {
            'actual_position': [0,0],
            'actual_direction': 'LEFT',
            'player_image': pygame.image.load("img/player_case.gif"),
            'player_rect': body_architecture['player_image'].get_rect()
        }
        if(nb_players > 0):
            last_body = self.players[nb_players - 1]
            free = get_body_free_space(nb_players - 1)
            if(free > 1):
        else:
            body_architecture['actual_position'] = [screen_size/2, screen_size/2]

        self.players.append(body_architecture)


    def get_body_free_space(self, body_index):
        free = self.ACTIONS
        for i in range(self.players.len()):
            if(i != body_index ):
                print('poof')
        return free

    def get_reward(self):
        return 0