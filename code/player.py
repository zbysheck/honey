"""
This module is used to hold the Player class. The Player represents the user-
controlled sprite on the screen.
"""
import pygame

import constants

from platforms import MovingPlatform
from spritesheet_functions import SpriteSheet


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    # Flag indicates whether movement is enabled or disabled
    _enabled = True

    # -- Attributes
    # Set speed vector of player
    change_x = 0
    change_y = 0

    saved_x = None
    saved_y = None

    PL_WIDTH = 31
    PL_HEIGHT = 61
    PL_MARGIN = 8

    # This holds all the images for the animated walk left/right
    # of our player
    walking_frames_l = []
    walking_frames_r = []
    walking_frames_u = []
    walking_frames_d = []

    # What direction is the player facing?
    direction = "R"

    # List of sprites we can bump against
    level = None

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("img/player.png")
        # Load all the right facing images into a list

        for i in range(7):
            image = sprite_sheet.get_image(i * self.PL_WIDTH, 3 * self.PL_HEIGHT, self.PL_WIDTH,
                                           self.PL_HEIGHT - self.PL_MARGIN)
            self.walking_frames_r.append(image)
        for i in range(7):
            image = sprite_sheet.get_image(i * self.PL_WIDTH, 2 * self.PL_HEIGHT, self.PL_WIDTH,
                                           self.PL_HEIGHT - self.PL_MARGIN)
            self.walking_frames_l.append(image)
        for i in range(7):
            image = sprite_sheet.get_image(i * self.PL_WIDTH, self.PL_HEIGHT, self.PL_WIDTH,
                                           self.PL_HEIGHT - self.PL_MARGIN)
            self.walking_frames_u.append(image)
        for i in range(7):
            image = sprite_sheet.get_image(i * self.PL_WIDTH, 0, self.PL_WIDTH, self.PL_HEIGHT - self.PL_MARGIN)
            self.walking_frames_d.append(image)

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

    def update(self):
        if self._enabled:
            """ Move the player. """
            # Gravity
            self.calc_grav()

            # Move left/right
            self.rect.x += self.change_x
            pos = self.rect.x + self.level.world_shift
            if self.direction == "R":
                frame = (pos // 30) % len(self.walking_frames_r)
                self.image = self.walking_frames_r[frame]
            else:
                frame = (pos // 30) % len(self.walking_frames_l)
                self.image = self.walking_frames_l[frame]

            # See if we hit anything
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            for block in block_hit_list:
                # If we are moving right,
                # set our right side to the left side of the item we hit
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right

            # Move up/down
            self.rect.y += self.change_y

            # Check and see if we hit anything
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            for block in block_hit_list:

                # Reset our position based on the top/bottom of the object.
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom

                # Stop our vertical movement
                self.change_y = 0

                if isinstance(block, MovingPlatform):
                    self.rect.x += block.change_x

    def calc_grav(self):
        if self._enabled:
            """ Calculate effect of gravity. """
            if self.change_y == 0:
                self.change_y = 1
            else:
                self.change_y += .35

            # See if we are on the ground.
            if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
                self.change_y = 0
                self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        if self._enabled:
            self.rect.y += 2
            platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            self.rect.y -= 2

            # If it is ok to jump, set our speed upwards
            if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
                self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        if self._enabled:
            self.change_x = -6
            self.direction = "L"

    def go_right(self):
        """ Called when the user hits the right arrow. """
        if self._enabled:
            self.change_x = 6
            self.direction = "R"

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

    def enable_movement(self):
        self._enabled = True

    def disable_movement(self):
        self._enabled = False

    def show(self):
        self.add(self.sprite_list)
        print "SHOW"

    def hide(self):
        self.kill()
