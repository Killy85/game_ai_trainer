from game_adapted import Game_adapted
from skimage.color import rgb2gray
from skimage.transform import resize
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

if __name__ == '__main__':
    game = Game_adapted(False)
    game.main()

    for p in range(2000):
        if(p == 1):
            print(game.update_frame(2))
        else:
            print(str(p) + " loop")
            images, reward, boolean = game.update_frame(1)
            for i in range(0,3):
                processed_observe = resize(rgb2gray(images[i]), (84, 84), mode='constant')
                plt.imshow(processed_observe)
                plt.show()