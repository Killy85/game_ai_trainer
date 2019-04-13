from game_adapted import Game_adapted

if __name__ == '__main__':
    game = Game_adapted()
    game.main()

    for p in range(10):
        game.update_frame(1)