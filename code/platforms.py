"""
Module for managing platforms.
"""
import pygame
import time

from spritesheet_functions import SpriteSheet

# These constants define our platform types:
#   Name of file
#   X location of sprite
#   Y location of sprite
#   Width of sprite
#   Height of sprite

GRASS_LEFT            = (576, 720, 70, 70)
GRASS_RIGHT           = (576, 576, 70, 70)
GRASS_MIDDLE          = (504, 576, 70, 70)
STONE_PLATFORM_LEFT   = (432, 720, 70, 40)
STONE_PLATFORM_MIDDLE = (648, 648, 70, 40)
STONE_PLATFORM_RIGHT  = (792, 648, 70, 40)
WALL_SPRITE           = (504, 288, 70, 70)

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, sprite_sheet_data):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("things_spritesheet2.png")
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])

        self.rect = self.image.get_rect()



class MovingPlatform(Platform):
    """ This is a fancier platform that can actually move. """
    change_x = 0
    change_y = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    level = None
    player = None

    def update(self):
        """ Move the platform.
            If the player is in the way, it will shove the player
            out of the way. This does NOT handle what happens if a
            platform shoves a player into another object. Make sure
            moving platforms have clearance to push the player around
            or add code to handle what happens if they don't. """

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1

class Husband(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    # -- Attributes
    # Set speed vector of player
    change_x = 0
    change_y = 0
    sprite_frame_frequency = 4

    PL_WIDTH = 64
    PL_HEIGHT = 64
    PL_MARGIN = 0

    # This holds all the images for the animated walk left/right of our player
    walking_frames_l = []
    walking_frames_r = []
    walking_frames_u = []
    walking_frames_d = []

    # What direction is the player facing?
    direction = "R"

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

        if self.rect.x > 400:
            self.direction = "L"
            self._set_direction(-1, 0)
        elif self.rect.x < 200:
            self.direction = "R"
            self._set_direction(1, 0)

        self._collision_detection()

        print str(time.time()) + "\t" + "updating " + "x=" + str(self.rect.x) + " y=" + str(self.rect.y)

    def update(self):
        self._ai();
        self._update_animation()


