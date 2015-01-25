import pygame

import constants
import platforms
import thing

from husband import Husband


class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    # Lists of sprites used in all levels. Add or remove
    # lists as needed for your game. """
    platform_list = None
    enemy_list = None
    thing_list = None
    door_list = {}
    tileSize = 70
    wallpaper_points = []
    wallpaper_color = (0, 0, 0)

    # Background image
    background = None

    # How far this world has been scrolled left/right
    world_shift = 0
    level_limit = -1000

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.thing_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

    def one_tile(self, tile, y, x, passable):
        return [tile, x*self.tileSize, y*self.tileSize, passable]

    def generate_tiles(self, txt):
        generated = []
        txt = txt.split("\n")
        result = []
        for i in txt:
            result.append(list(i))
        for i in range(len(result)):
            for j in range(len(result[i])):
                if txt[i][j] != ' ':
                    if txt[i][j] == '#':
                        generated.append(self.one_tile(platforms.WALL_SPRITE, i, j, False))
                        t = self.one_tile(platforms.WALL_SPRITE, i, j, False)
                        block = platforms.Platform(t[0], t[1], t[2], self.player)
                        self.platform_list.add(block)
                    elif txt[i][j] != '.':
                        # Put wallpaper behind other stuff (or nooot)
                        t = thing.Thing
                        if txt[i][j] == 'l':
                            chosen_sprite = self.one_tile(thing.LADDER_SPRITE, i, j, self.player)
                        elif txt[i][j] == 'w':
                            chosen_sprite = self.one_tile(thing.WINDOW_WALL_SPRITE, i, j, self.player)
                        elif txt[i][j] == 's':
                            chosen_sprite = [thing.WARDROBE_OPEN, j*self.tileSize, i*self.tileSize, self.player, thing.WARDROBE_CLOSED, thing.WARDROBE_CLOSED2]
                            t = thing.Wardrobe
                        elif txt[i][j] == 'D':
                            chosen_sprite = [thing.DOOR_CLOSED, j*self.tileSize, i*self.tileSize, self.player, thing.DOOR_OPEN]
                            t = thing.Door
                        elif txt[i][j] == 'c':
                            chosen_sprite = [thing.SOCK, j*self.tileSize, i*self.tileSize, self.player]
                            t = thing.Clothing
                        elif txt[i][j] == 'b':
                            chosen_sprite = self.one_tile(thing.BED, i, j, self.player)
                        elif txt[i][j].isdigit():
                            chosen_sprite = [thing.STAIR_SPRITE, j*self.tileSize, i*self.tileSize, self.player, txt[i][j]]
                            t = thing.Staircase
                        if chosen_sprite:
                            block = t(*chosen_sprite)
                            self.thing_list.add(block)
                            self.match_doors()

        return generated

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.thing_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        # We don't shift the background as much as the sprites are shifted
        # to give a feeling of depth.
        screen.fill(constants.BLUE)
        screen.blit(self.background, (self.world_shift // 3, 0))

        # Draw wallpaper
        pygame.draw.polygon(screen, self.wallpaper_color, self.wallpaper_points)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.thing_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for the_thing in self.thing_list:
            the_thing.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for x in self.wallpaper_points:
            x[0] += shift_x

    def match_doors(self):
        door_dict = {}
        for i in self.thing_list:
            if isinstance(i, thing.Staircase):
                if i.door_number in door_dict:
                    i.paired_door = door_dict[i.door_number]
                    door_dict[i.door_number].paired_door = i
                else:
                    door_dict[i.door_number] = i

    def translate_wallpaper(self):
        self.wallpaper_points = [[x * self.tileSize for x in y] for y in self.wallpaper_points]  # Fuck yeah
        print self.wallpaper_points


# Create platforms for the level
class Level01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("img/background_01.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -2500

        txt = """
 ################
 #..............#
 #..s..1......2.#
 ##################
 #.......#........#
 #b...1..D.c.2.....
 ##################"""

        level = self.generate_tiles(txt)  # +level

        # init wallpaper boundaries
        self.wallpaper_points += [[1, 1], [16, 1], [16, 4], [18, 4], [18, 7], [1, 7]]
        self.translate_wallpaper()
        self.wallpaper_color = (189, 140, 191)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE, 1350, 280, self.player)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        # Add husband
        husband = Husband()
        husband.rect.x = 200
        husband.rect.y = constants.SCREEN_HEIGHT - husband.rect.height - 100
        husband.player = player
        self.enemy_list.add(husband)


# Create platforms for the level
class Level02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("img/background_02.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -1000

        # Array with type of platform, and x, y location of the platform.
        level = [ [platforms.STONE_PLATFORM_LEFT, 500, 550],
                  [platforms.STONE_PLATFORM_MIDDLE, 570, 550],
                  [platforms.STONE_PLATFORM_RIGHT, 640, 550],
                  [platforms.GRASS_LEFT, 800, 400],
                  [platforms.GRASS_MIDDLE, 870, 400],
                  [platforms.GRASS_RIGHT, 940, 400],
                  [platforms.GRASS_LEFT, 1000, 500],
                  [platforms.GRASS_MIDDLE, 1070, 500],
                  [platforms.GRASS_RIGHT, 1140, 500],
                  [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                  ]

        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.player)
            self.platform_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE, 1500, 300, self.player)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
