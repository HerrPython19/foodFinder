import pygame, sys
from pygame.locals import *

#Global variables representing window dimensions
WINDOWWIDTH = 400
WINDOWHEIGHT = 300

#Global variable for top-level surface
WINDOWSURF = None
DRAWSURF = None

#Color globals
BLACK = (0,0,0)
WHITE = (255,255,255)

#Define our desired FPS
FPS = 60

#Main function
def main():
    pygame.init()
    WINDOWSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    DRAWSURF = pygame.Surface((WINDOWWIDTH,WINDOWHEIGHT))
    DRAWSURF.fill(BLACK)
    pygame.display.set_caption("Food Finder")
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        WINDOWSURF.blit(DRAWSURF,(0,0))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
