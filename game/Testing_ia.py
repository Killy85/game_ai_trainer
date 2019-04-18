from game_adapted import Game_adapted

if __name__ == '__main__':
    game = Game_adapted(False)
    game.main()

    for p in range(2000):
        if(p == 1):
            print(game.update_frame(2))
        else:
            print(str(p) + " loop")
            game.update_frame(1)