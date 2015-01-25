"""
Module for managing platforms.
"""
import time
import pygame
from pygame.event import Event
import constants
from player import Player

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
WARDROBE_OPEN         = (72, 360, 70, 70)
WARDROBE_CLOSED       = (144, 360, 70, 70)
WARDROBE_CLOSED2       = (217, 360, 69, 70)
DOOR_OPEN         = (720, 432, 70, 70)
DOOR_CLOSED       = (648, 432, 70, 70)
SOCK              = (72, 0, 70, 70)

class Thing(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, sprite_sheet_data, x, y, player):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("img/things_spritesheet2.png")
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

    def do_action(self, hit):
        raise NotImplementedError()

    def update(self):
        hit = pygame.sprite.spritecollideany(self, self.player)
        if hit and not hit._enabled:
            self.do_action(hit)
            hit.enable_movement()


class Staircase(ActionObject):
    def __init__(self, sprite_sheet_data, x, y, player, door_number):
        super(Staircase, self).__init__(sprite_sheet_data, x, y, player)
        self.door_number = door_number
        self.paired_door = None

    def do_action(self, hit):
        hit.rect.x = self.paired_door.rect.x
        hit.rect.y = self.paired_door.rect.y


class Wardrobe(Thing):

    def __init__(self, sprite_sheet_data, x, y, player, closed_image, closed_image2):
        super(Wardrobe, self).__init__(sprite_sheet_data, x, y, player)
        self.hidden = False
        self.open_image = self.image
        sprite_sheet = SpriteSheet("img/things_spritesheet2.png")
        self.closed_image = sprite_sheet.get_image(*closed_image)
        self.closed_image2 = sprite_sheet.get_image(*closed_image2)
        self.last_change = time.time()

    def update(self):
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit and not self.player._enabled and time.time() - self.last_change > 0.75:
            if self.hidden:
                self.image = self.open_image
                self.player.show()
                self.hidden = False
            else:
                self.image = self.closed_image
                self.player.hide()
                self.hidden = True
            self.last_change = time.time()

        if self.hidden and time.time() - self.last_change > 1:
            self.last_change = time.time()
            if self.image == self.closed_image:
                self.image = self.closed_image2
            else:
                self.image = self.closed_image

class Door(Thing):
    """ Door opens when you touch it and stays open """
    def __init__(self, sprite_sheet_data, x, y, player, open_image):
        super(Door, self).__init__(sprite_sheet_data, x, y, player)
        self.open = False
        self.closed_image = self.image
        sprite_sheet = SpriteSheet("img/things_spritesheet2.png")
        self.open_image = sprite_sheet.get_image(*open_image)
        self.last_change = time.time()

    def update(self):
        hit = pygame.sprite.spritecollideany(self, self.player)
        #print("hit: " + str(hit) + "  isOpen: " + str (self.open))
        if hit and not self.open:
            self.image = self.open_image
            self.open = True
        elif not hit and self.open:
            self.image = self.closed_image
            self.open = False

class FinalDoor(Door):
    def update(self):
        super(FinalDoor, self).update()
        hit = pygame.sprite.spritecollideany(self, self.player)
        if hit and isinstance(hit, Player):
            pygame.event.post(Event(pygame.USEREVENT, {"action": constants.MESSAGE, "message": "LEVEL COMPLETE", "time": 5}))


class Clothing(ActionObject):
    """ Clothing disappears when you pick it up """
    def do_action(self, hit):
        self.kill()