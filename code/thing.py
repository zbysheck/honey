"""
Module for managing platforms.
"""
import pygame

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
LADDER_SPRITE         = (504, 144, 70, 70)
WALLPAPER_SPRITE      = (504, 0, 70, 70)
WINDOW_WALL_SPRITE    = (504, 359, 70, 70)
STAIR_SPRITE           = (648, 288, 70, 70)
BED                   = (72, 432, 70, 70)

class Thing(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, sprite_sheet_data, x, y, player):
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
        self.rect.x = x
        self.rect.y = y
        self.player = player


class ActionObject(Thing):
    def do_action(self):
        raise NotImplementedError()

    def update(self):
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit and not self.player._enabled:
            self.do_action()
            self.player.enable_movement()


class Staircase(ActionObject):
    def __init__(self, sprite_sheet_data, x, y, player, door_number):
        super(Staircase, self).__init__(sprite_sheet_data, x, y, player)
        self.door_number = door_number
        self.paired_door = None

    def do_action(self):
        self.player.rect.x = self.paired_door.rect.x
        self.player.rect.y = self.paired_door.rect.y