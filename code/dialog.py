import pygame


class Dialog:
    x = 0
    y = 0
    message = ""
    bubble = None

    def __init__(self, x, y, message):
        self.x = x
        self.y = y
        self.message = message
        self.bubble = pygame.Rect(x, y, 32 * len(message), 44)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.bubble, 0)
        font = pygame.font.Font('resources/PressStart2P.ttf', 32)
        angle_display = font.render(self.message, 0, (0, 0, 0))
        surface.blit(angle_display, (self.x+8, self.y+8))