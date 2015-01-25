from pygame.event import Event
from constants import GAME_OVER_EVENT
import constants

__author__ = 'ksakowsk'

import pygame
import sys
import time

from spritesheet_functions import SpriteSheet

class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, width, height):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       color = pygame.Color(255, 0, 0 , 0);
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()


class Husband(pygame.sprite.Sprite):
    """ This class implements husband. """

    # Constants
    PL_WIDTH = 64
    PL_HEIGHT = 64
    PL_MARGIN = 0

    # Attributes
    _change_x = 0
    _change_y = 0
    _x0 = 500
    _y0 = 0
    _direction = "L"
    _sprite_frame_frequency = 4
    _walking_frames_l = []
    _walking_frames_r = []
    _suspicion_value  = 0

    _enabled = False

    player = None

    def __init__(self):
        super(Husband, self).__init__()

        self._change_x = -1
        self._change_y = 0

        sprite_sheet = SpriteSheet("img/husband.png")

        for i in range(9):
            image = sprite_sheet.get_image(i * self.PL_WIDTH, 3 * self.PL_HEIGHT, self.PL_WIDTH, self.PL_HEIGHT-self.PL_MARGIN)
            self._walking_frames_r.append(image)
        for i in range(9):
            image = sprite_sheet.get_image(i * self.PL_WIDTH, self.PL_HEIGHT, self.PL_WIDTH, self.PL_HEIGHT-self.PL_MARGIN)
            self._walking_frames_l.append(image)

        # Set the image the player starts with
        self.image = self._walking_frames_l[0]

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

    def draw_suspicion_meter(self, screen):
        red     = (255, 0, 0)
        black   = (0, 0, 0)
        x       = 680
        y       = 30
        width   = self._suspicion_value
        height  = 20

        pygame.draw.rect(screen, black, (x - 5, y - 5, 99 + 10, height + 10))
        pygame.draw.rect(screen, red, (x, y, width, height))

    def _update_suspicion_meter(self):
        self._suspicion_value = (self._suspicion_value + 1) % 100

    def _update_position(self):
        self._x0 += self._change_x
        self._y0 += self._change_y
        self.rect.x += self._change_x
        self.rect.y += self._change_y

    def _update_animation(self):
        self._sprite_frame_frequency += 4

        if self._direction == "R":
            frame = (self._sprite_frame_frequency // 30) % len(self._walking_frames_r)
            self.image = self._walking_frames_r[frame]
        else:
            frame = (self._sprite_frame_frequency // 30) % len(self._walking_frames_l)
            self.image = self._walking_frames_l[frame]

    def _set_direction(self, x, y):
        self._change_x = x
        self._change_y = y

    def _collision_detection(self):
        # husband sight range simulated by rectangle with given size
        width = 100
        height = 70
        block = Block(width, height)

        # compute sight rectangle coordinates in order to detect whether player has been seen or not
        if self._direction == "R":
            block.rect.x = self.rect.x + width
            block.rect.y = self.rect.y
        elif self._direction == "L":
            block.rect.x = self.rect.x - width
            block.rect.y = self.rect.y

        # detect collision
        if pygame.sprite.collide_rect(block, self.player):
            print "collision!"
            pygame.event.post(Event(pygame.USEREVENT, {"action": constants.MESSAGE, "message": "GAME OVER", "time": 5}))

    def _ai(self):
        self._update_position()

        self._update_suspicion_meter()

        if self._x0 > 500:
            self._direction = "L"
            self._set_direction(-1, 0)
        elif self._x0 < 0:
            self._direction = "R"
            self._set_direction(1, 0)

        self._collision_detection()

        #print str(time.time()) + "\t" + "updating " + "x=" + str(self.rect.x) + " y=" + str(self.rect.y)

    def update(self):
        self._ai()
        self._update_animation()

    def enable_movement(self):
        # if True - husband cannot move through stairs and doors
        self._enabled = True
