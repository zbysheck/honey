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
    _PL_WIDTH = 64
    _PL_HEIGHT = 64
    _PL_MARGIN = 0

    # Statics
    _suspicion_value = 0
    _suspicion_delay = 0
    _suspicion_meter_velocity = 7
    _last_suspicion_meter_update = 0

    # Public references
    player = None

    def __init__(self, patrol_zone, sprite_img_path = "img/husband.png"):
        super(Husband, self).__init__()

       # Attributes
        self._change_x = -1
        self._change_y = 0
        self._x0 = 500
        self._y0 = 0
        self._direction = "L"
        self._sprite_frame_frequency = 4
        self._walking_frames_l = []
        self._walking_frames_r = []
        self._patrol_zone = []
        self._enabled = False
        self._patrol_zone = patrol_zone

        sprite_sheet = SpriteSheet(sprite_img_path)

        for i in range(9):
            image = sprite_sheet.get_image(i * self._PL_WIDTH, 3 * self._PL_HEIGHT, self._PL_WIDTH, self._PL_HEIGHT-self._PL_MARGIN)
            self._walking_frames_r.append(image)

        for i in range(9):
            image = sprite_sheet.get_image(i * self._PL_WIDTH, self._PL_HEIGHT, self._PL_WIDTH, self._PL_HEIGHT-self._PL_MARGIN)
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

        # frame
        pygame.draw.rect(screen, black, (x - 5, y - 5, 99 + 10, height + 10))

        # suspicion meter
        pygame.draw.rect(screen, red, (x, y, width, height))

    @staticmethod
    def _increase_suspicion_meter(value):
        if (Husband._suspicion_delay % Husband._suspicion_meter_velocity == 0):

            if ((Husband._suspicion_value + value) >= 100):
                Husband._suspicion_value = 100
            else:
                Husband._suspicion_value += value

        Husband._suspicion_delay += 1

    @staticmethod
    def _decrease_suspicion_meter(value):
        if (Husband._suspicion_delay % Husband._suspicion_meter_velocity == 0):

            if ((Husband._suspicion_value - value) < 0):
                Husband._suspicion_value = 0
            else:
                Husband._suspicion_value -= value

        Husband._suspicion_delay += 1

    def _update_position(self):
        k = Husband._suspicion_value // 13

        if k == 0:
            k = 1

        dx = (k * self._change_x)
        dy = (k * self._change_y)

        self._x0 += dx
        self._y0 += dy
        self.rect.x += dx
        self.rect.y += dy

        print "k=" + str(k)

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

        if not self.player.hidden:
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

            # check if player is in the husband sight
            if pygame.sprite.collide_rect(block, self.player):
                print "I see you!!!"

                Husband._increase_suspicion_meter(10)

                pygame.event.post(Event(pygame.USEREVENT, {"action": constants.MESSAGE, "message": "I see you!!!", "time": 5}))

            # check if husband caught player
            if pygame.sprite.collide_rect(self, self.player):
                print "I got you!!!"

                Husband._increase_suspicion_meter(100)

                pygame.event.post(Event(pygame.USEREVENT, {"action": constants.MESSAGE, "message": "GAME OVER", "time": 10, "kill": True}))

    def _ai(self):
        self._update_position()

        if self._x0 > self._patrol_zone[1]:
            self._direction = "L"
            self._set_direction(-1, 0)
        elif self._x0 < self._patrol_zone[0]:
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
