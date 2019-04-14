# -*- coding: cp1252 -*-
from pygame import *
from math import cos, sin, pi
import os.path
import sys

"""
Une addaptation du jeu pour communiquer aver l'ia

Description :

- start () : void
- action("Droite"/"gauche") : action_feedback

"""

# couleurs
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

#Fonction pour charger les images
def load_image(name, colorkey=None):
    fullname = os.path.join(os.getcwd(), 'images', name)
    img = image.load(fullname)
    img = img.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey, RLEACCEL)
    return img, img.get_rect()

class Brique(sprite.Sprite):
    """Les briques sont détruites par la balle."""
    def __init__(self, screen, x, y):
        sprite.Sprite.__init__(self)
        self.screen = screen
        self.x, self.y = x, y
        self.image, self.rect = load_image('brique.GIF')
        self.rect.topleft = (self.x, self.y)

class Balle(sprite.Sprite):
    """Une balle qui se déplace sur l'écran."""
    def __init__(self, screen):
        sprite.Sprite.__init__(self)
        self.screen = screen
        self.area = self.screen.get_rect()
        self.image, self.rect = load_image('balle.GIF', -1)
        self.reinit()
        self.is_lauched = False
        self.has_bounced = False

    def reinit(self):
        self.rect.centerx = self.area.centerx
        self.rect.centery = 500
        self.angle = pi/3.3
        self.flag = 1

    def update(self):
        if self.flag == 1:
            dx, dy = 7*cos(self.angle), 7*sin(self.angle)
            self.rect = self.rect.move(dx, dy)
            #Collision sur les parois de l'écran
            if not self.area.contains(self.rect):
                tl = not self.area.collidepoint(self.rect.topleft)
                tr = not self.area.collidepoint(self.rect.topright)
                bl = not self.area.collidepoint(self.rect.bottomleft)
                br = not self.area.collidepoint(self.rect.bottomright)
                if tr and tl or (br and bl):
                    self.angle = -self.angle
                if tl and bl:
                    self.angle = pi - self.angle
                if tr and br:
                    self.angle = pi - self.angle
                if bl and br:
                    self.reinit()
                    j.reinit()
                    j.vies = j.vies - 1
            #Collision avec la raquette du joueur
            elif self.rect.colliderect(j.rect):
                self.rect.bottom = j.rect.top
                self.angle = -self.angle
                self.has_bounced = True
            #Collision avec une brique du groupe briquesprite
            collision = sprite.spritecollide(self, brs, 1)
            if collision:
                self.angle = -self.angle
                j.score = j.score + 5*(len(collision))

    def start(self):
        self.flag = 1
    def pause(self):
        if self.flag == 1:
            self.flag = 'p'
            return
        if self.flag == 'p':
            self.flag = 1

class Raquette(sprite.Sprite):
    """Une raquette pour empécher la balle de tomber."""
    def __init__(self, screen):
        sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('raquette.GIF')
        self.screen = screen
        self.area = self.screen.get_rect()
        self.score = 0
        self.vies_max = 5
        self.vies = self.vies_max
        self.font1 = font.Font(None, 25)
        self.font2 = font.Font(None, 25)
        self.reinit()

    def update(self):
        text1 = self.font1.render("Score : "+str(self.score), 1, (0, 0, 0))
        text1pos = text1.get_rect(topleft=(5, 5))
        text2 = self.font2.render("Vies : "+str(self.vies), 1, (0, 0, 0))
        text2pos = text2.get_rect(topright=(515, 5))
        self.screen.blit(text1, text1pos)
        self.screen.blit(text2, text2pos)

    def reinit(self):
        self.rect.centerx = self.area.centerx
        self.rect.centery = 510
        self.flag = 0

    def left(self):
        if self.flag == 0:
            rect = self.rect.move((-60, 0))
            if rect.left < 0:
                rect.left = 0
            self.rect = rect

    def right(self):
        if self.flag == 0:
            rect = self.rect.move((60, 0))
            if rect.right > self.area.right:
                rect.right = self.area.right
            self.rect = rect

    def start(self):
        self.flag = 1

    def pause(self):
        if self.flag == 1:
            self.flag = 'p'
            return
        if self.flag == 'p':
            self.flag = 1


class Game_adapted():

    def __init__(self, limit_fps = True):
        self.limit_fps = limit_fps
        """ """


    def briques(self, screen, niv):
        #Construction des briques selon le niveau
        briques = sprite.RenderPlain()
        if niv == 1:
            x, y = 7, 40
            while x < 470:
                brique = Brique(screen, x, y)
                briques.add(brique)
                y = y + 16
                if y == 200:
                    y = 40
                    x = x + 46
        if niv == 2:
            x, y = 7, 40
            while x < 470:
                brique = Brique(screen, x, y)
                briques.add(brique)
                y = y + 16
                if y == 200:
                    y = 40
                    x = x + 92
        return briques

    def initialisation(self, screen):
        balle = Balle(screen)
        joueur = Raquette(screen)
        ballesprite = sprite.RenderPlain(balle)
        joueursprite = sprite.RenderPlain(joueur)
        briquesprite = self.briques(screen, 2)
        return balle, joueur, ballesprite, joueursprite, briquesprite

    def start(self):
        self.b.start()
        j.start()

    def pause(self):
        self.b.pause()
        j.pause()

    def update_frame(self, movement):
        reward = 0
        rectPos = j.rect.x
        startBrs = len(brs)
        start_vie = j.vies
        #flag2 = True
        for p in range(30): # while flag2:
            if self.limit_fps :
                self.chrono.tick(60)
            # Contréler la raquette
            if(movement == 2 and p == 5):
                # Deplacement de la barre vers la droite
                j.right()
            if(movement == 0 and p == 5):
                # Deplacement de la barre vers la gauche
                j.left()
            if j.vies == 0:
                # Si le joueur n'a plus de vies
                msg5 = self.cadre.render("Vous avez perdu. Votre score:", 0, black)
                msg6 = self.cadre.render(str(j.score), 0, black)
                pos_msg5 = msg5.get_rect()
                pos_msg5.center = self.area.center
                pos_msg6 = msg6.get_rect()
                pos_msg6.center = self.area.center
                pos_msg6.centery = self.area.centery + 50
                # Affichage à l'écran
                self.screen.fill(red)
                self.screen.blit(msg5, pos_msg5)
                self.screen.blit(msg6, pos_msg6)
                display.flip()
                reward -= 100;
                j.vies = j.vies_max
            if len(brs) == 0:
                # S'il n'y a plus de briques
                msg7 = self.cadre.render("Vous avez gagné. Votre score:", 0, black)
                msg8 = self.cadre.render(str(j.score), 0, black)
                pos_msg7 = msg7.get_rect()
                pos_msg7.center = self.area.center
                pos_msg8 = msg8.get_rect()
                pos_msg8.center = self.area.center
                pos_msg8.centery = self.area.centery + 50
                # Affichage à l'écran
                self.screen.fill(green)
                self.screen.blit(msg7, pos_msg7)
                self.screen.blit(msg8, pos_msg8)
                display.flip()
                flag5 = True
                while flag5:
                    for e in event.get():
                        if e.type == KEYDOWN and e.key == K_ESCAPE:
                            flag5 = False
                            flag2 = False
            if(self.b.has_bounced and self.b.is_lauched):
                reward += 5
                self.b.has_bounced = False
            # Rafraichissement de l'écran pendant le jeu
            self.screen.fill(blue)
            self.bs.update()
            self.js.update()
            self.bs.draw(self.screen)
            self.js.draw(self.screen)
            brs.draw(self.screen)
            display.flip()

        brick_reward = startBrs - len(brs) * 5
        life_reward = ((start_vie - j.vies) * -100)
        self.b.is_lauched = True
        if(start_vie - j.vies): self.b.is_lauched = False
        self.b.has_bounced = False
        return (j.rect.x, self.b.rect.x), reward+life_reward, (start_vie == 1 and j.vies == 5)

    def main(self):
        #Initialisation de l'écran
        init()
        self.screen = display.set_mode((540, 550))
        display.set_caption('Casse Briques v.1.1.')
        icon, icon_rect = load_image('icon.GIF')
        display.set_icon(icon)
        self.area = self.screen.get_rect()
        self.screen.fill((0, 0, 0))
        display.flip()
        #Accueil
        self.cadre = font.Font(None, 35)
        self.chrono = time.Clock()
        global j, brs
        self.b, j, self.bs, self.js, brs = self.initialisation(self.screen)

if __name__ == '__main__':
    Game_adapted().main()


