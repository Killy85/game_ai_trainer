from game_adapted import Game_adapted

if __name__ == '__main__':
    game = Game_adapted()
    game.main()

    for p in range(10):
        if(p == 1):
            print(game.update_frame(2))
        else:
            print(game.update_frame(1))