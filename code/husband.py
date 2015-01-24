__author__ = 'ksakowsk'

import pygame
import time

from spritesheet_functions import SpriteSheet

class Husband(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    # -- Attributes
    # Set speed vector of player
    change_x = 0
    change_y = 0
    x0 = 0
    y0 = 0
    direction = "R"
    sprite_frame_frequency = 4

    PL_WIDTH = 64
    PL_HEIGHT = 64
    PL_MARGIN = 0

    # This holds all the images for the animated walk left/right of our player
    walking_frames_l = []
    walking_frames_r = []
    walking_frames_u = []
    walking_frames_d = []

    player = None

    def __init__(self):
        super(Husband, self).__init__()

        self.change_x = 1
        self.change_y = 0

        sprite_sheet = SpriteSheet("husband.png")

        for i in range(9):
            image = sprite_sheet.get_image(i * self.PL_WIDTH, 3 * self.PL_HEIGHT, self.PL_WIDTH, self.PL_HEIGHT-self.PL_MARGIN)
            self.walking_frames_r.append(image)
        for i in range(9):
            image = sprite_sheet.get_image(i * self.PL_WIDTH, self.PL_HEIGHT, self.PL_WIDTH, self.PL_HEIGHT-self.PL_MARGIN)
            self.walking_frames_l.append(image)
        for i in range(9):
            image = sprite_sheet.get_image(i * self.PL_WIDTH, 0, self.PL_WIDTH, self.PL_HEIGHT-self.PL_MARGIN)
            self.walking_frames_u.append(image)
        for i in range(9):
            image = sprite_sheet.get_image(i * self.PL_WIDTH, 2 * self.PL_HEIGHT, self.PL_WIDTH, self.PL_HEIGHT-self.PL_MARGIN)
            self.walking_frames_d.append(image)

        # Set the image the player starts with
        self.image = self.walking_frames_l[0]

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

    def _update_position(self):
        self.x0 = self.x0 + self.change_x
        self.y0 = self.y0 + self.change_y
        self.rect.x = self.rect.x + self.change_x
        self.rect.y = self.rect.y + self.change_y

    def _update_animation(self):
        self.sprite_frame_frequency = self.sprite_frame_frequency + 4

        if self.direction == "R":
            frame = (self.sprite_frame_frequency // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (self.sprite_frame_frequency // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

    def _set_direction(self, x, y):
        self.change_x = x
        self.change_y = y

    def _collision_detection(self):
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            print "collision!"

    def _ai(self):
        self._update_position()

        if self.x0 > 350:
            self.direction = "L"
            self._set_direction(-1, 0)
        elif self.x0 < 0:
            self.direction = "R"
            self._set_direction(1, 0)

        self._collision_detection()

        print str(time.time()) + "\t" + "updating " + "x=" + str(self.rect.x) + " y=" + str(self.rect.y)

    def update(self):
        self._ai();
        self._update_animation()
