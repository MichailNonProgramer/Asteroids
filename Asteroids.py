import pygame
import Game

if __name__ == '__main__':
    pygame.init()
    game = Game.Game()
    game.game_loop("Menu")
    pygame.quit()
    quit()
