"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

Main module for platform scroller example.

From:
http://programarcadegames.com/python_examples/sprite_sheets/

Explanation video: http://youtu.be/czBDKWJqOao

Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/

Game art from Kenney.nl:
http://opengameart.org/content/platformer-art-deluxe

"""

import pygame

import time
from pygame.constants import FULLSCREEN
import constants
from husband import Husband
import levels
import dialog

from player import Player

current_message = "Oh no! It's my husband!"
message_expire = None
message_display_time = 2

def show_help(screen):
    textcolor = (255, 255, 255)
    font = pygame.font.Font('resources/FreeMono.ttf', 18)
    help_text = ["Help", "Move around    arrow keys", "Use sword  space"]
    for i, line in enumerate(help_text):
        angle_display = font.render(line, 0, textcolor)
        screen.blit(angle_display, (0, 18 * i))


def print_msg(message, x, y, screen):
    txt = dialog.Dialog(x, y, message)
    txt.draw(screen)


def main():
    """ Main Program """
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    global current_message, message_expire, message_display_time
    # music = pygame.mixer.Sound("resources/DST-Arch-Delerium.ogg")
    #music.play(loops=-1)

    # Set the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    flags = screen.get_flags()
    flags = flags|FULLSCREEN
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT), flags)

    pygame.display.set_caption("Platformer with sprite sheets")

    # Create the player
    player = Player()

    # Add husband
    husband = Husband()
    husband.player = player


    # Create all the levels
    level_list = [levels.Level01(player, husband)]
    #level_list.append(levels.Level_02(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    player.sprite_list = active_sprite_list
    player.rect.x = 340
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height - 30
    active_sprite_list.add(player)

    #Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    time_start = time.time()
    dead = False
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            if event.type == pygame.USEREVENT:
                if event.dict["action"] == constants.MESSAGE:
                    current_message = event.dict["message"]
                    message_display_time = event.dict["time"]
                    #done = True

                if event.dict.get("kill", False) and not dead:
                    dead = True

            if event.type == pygame.KEYDOWN and not dead:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_SPACE:
                    player.disable_movement()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
                if event.key == pygame.K_SPACE:
                    player.enable_movement()

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.x >= 500:
            diff = player.rect.x - 500
            player.rect.x = 500
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.x <= 120:
            diff = 120 - player.rect.x
            player.rect.x = 120
            current_level.shift_world(diff)

        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list) - 1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        #show_help(screen)

        if time.time() - time_start < 4 and time.time() - time_start > 2:
            print_msg("WHAT DO WE DO NOW?!?", 10, 510, screen)

        if current_message:
            print_msg(current_message, 10, 510, screen)
            if not message_expire:
                message_expire = time.time()
        if message_expire and time.time() - message_expire > message_display_time:
            current_message = None
            message_expire = None
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


if __name__ == "__main__":
    main()
