# Set the font for the score
import pygame

from game.constansts import BALL_SIZE, PADDLE_HEIGHT, PADDLE_WIDTH, WHITE

def draw_text(text, x, y, screen, font):
    """Draws text on the screen"""
    text = font.render(text, True, WHITE)
    screen.blit(text, (x, y))

def draw_paddle(x, y, screen):
    """Draws a paddle on the screen"""
    pygame.draw.rect(screen, WHITE, [x, y, PADDLE_WIDTH, PADDLE_HEIGHT])

def draw_ball(x, y, screen):
    """Draws a ball on the screen"""
    pygame.draw.circle(screen, WHITE, [x, y], BALL_SIZE)