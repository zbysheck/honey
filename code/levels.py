import pygame

import constants
import platforms
import thing

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

    def onetile(self, tile, y,x,passable):
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
                        generated.append(self.onetile(platforms.WALL_SPRITE, i, j, False))
                        t = self.onetile(platforms.WALL_SPRITE, i, j, False)
                        block = platforms.Platform(t[0], t[1], t[2], self.player)
                        self.platform_list.add(block)
                    else:
                        # Put wallpaper behind other stuff
                        t = thing.Thing
                        chosen_sprite = self.onetile(thing.WALLPAPER_SPRITE, i, j, self.player)
                        if txt[i][j] == 'l':
                            chosen_sprite = self.onetile(thing.LADDER_SPRITE, i, j, self.player)
                        elif txt[i][j] == 'w':
                            chosen_sprite = self.onetile(thing.WINDOW_WALL_SPRITE, i, j, self.player)
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
        screen.blit(self.background,(self.world_shift // 3,0))

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

        for thing in self.thing_list:
            thing.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

    def match_doors(self):
        door_dict = {}
        for i in self.thing_list:
            if isinstance(i, thing.Staircase):
                if i.door_number in door_dict:
                    i.paired_door = door_dict[i.door_number]
                    door_dict[i.door_number].paired_door = i
                else:
                    door_dict[i.door_number] = i



# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("background_01.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -2500

        txt="""
 ##################
 #................#
 #.....1......2...#
 ##################
 #.......#........#
 #b...1..D...2.....
 ##################"""

        level = self.generate_tiles(txt)#+level

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
        husband = platforms.Husband()
        husband.rect.x = 200
        husband.rect.y = constants.SCREEN_HEIGHT - husband.rect.height - constants.TILE_HEIGHT
        husband.player = player
        self.enemy_list.add(husband)

# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("background_02.png").convert()
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
