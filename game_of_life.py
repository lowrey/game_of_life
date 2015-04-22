import pygame
import random
import math
import copy


def refresh_grid():
    global grid, nextGrid, gridsize, generations
    grid = []
    nextGrid = []
    for i in range(0, gridsize):
        tmp = []
        for i2 in range(0, gridsize):
            # tmp.append(False)
            if random.randint(0, 1) == 0:
                tmp.append(False)
            else:
                tmp.append(True)
        grid.append(tmp)
        nextGrid.append(tmp)
        generations = 0


def clear_grid():
    global grid, nextGrid, gridsize, generations, lastDrawnGrid
    for x in range(0, gridsize):
        for y in range(0, gridsize):
            grid[x][y] = False
            nextGrid[x][y] = False
    generations = 0
    lastDrawnGrid = []


def get_num_neighbors(x, y):
    global grid, gridsize
    num_neighbors = 0
    for xDif in range(-1, 2):
        for yDif in range(-1, 2):
            if xDif == 0 and yDif == 0:
                continue
            xCoord = x + xDif
            yCoord = y + yDif
            # print "Checking " + str(xCoord) + ", " + str(yCoord)
            if xCoord < 0 or yCoord < 0 or xCoord >= gridsize or yCoord >= gridsize:
                pass
            else:
                if grid[xCoord][yCoord]:
                    num_neighbors += 1
    return num_neighbors


def generation():
    global grid, gridsize, nextGrid, generations
    nextGrid = copy.deepcopy(grid)
    for x in range(0, gridsize):
        for y in range(0, gridsize):
            n = get_num_neighbors(x, y)

            if n == 2:
                pass
            elif n == 3:
                nextGrid[x][y] = True
            else:
                nextGrid[x][y] = False
    grid = nextGrid
    generations += 1


def drawScreen():
    screen.fill([255, 255, 255])
    # draw the screen
    screen.lock()

    for x in range(0, gridsize):
        for y in range(0, gridsize):
            if grid[x][y]:
                pygame.draw.rect(screen, (0, 0, 0), (x * xstretch, y * ystretch, xstretch, ystretch))

        screen.unlock()

if __name__ == "__main__":
    pygame.init()

    screen_size = [800, 600]

    screen = pygame.display.set_mode(screen_size)
    screen.fill([255, 255, 255])

    mainloop = True
    autorun = True
    fps = 60

    generations = 0

    gridsize = 60

    refresh_grid()

    xstretch = screen_size[0] / gridsize
    ystretch = screen_size[1] / gridsize
    # print xstretch, ystretch

    Clock = pygame.time.Clock()

    lastDrawnGrid = None

    while mainloop:
        tickFPS = Clock.tick(fps)
        if autorun:
            runningState = "Running."
        else:
            runningState = "Idle."
        pygame.display.set_caption(
            "%s Press Esc to quit. FPS: %.2f Generations: %d" % (runningState, Clock.get_fps(), generations))

        if autorun:
            generation()

        # only draw the screen if there's something new
        if lastDrawnGrid != grid:
            drawScreen()
            lastDrawnGrid = grid

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                if event.key == pygame.K_g:
                    generation()
                if event.key == pygame.K_r:
                    refresh_grid()
                if event.key == pygame.K_c:
                    clear_grid()
                if event.key == pygame.K_SPACE:
                    if autorun == False:
                        autorun = True
                    else:
                        autorun = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                xtile = int(math.ceil(event.pos[0] / xstretch))
                ytile = int(math.ceil(event.pos[1] / ystretch))

                if xtile >= gridsize or ytile >= gridsize:
                    continue

                if event.button == 1:
                    grid[xtile][ytile] = True
                    generations = 0
                    lastDrawnGrid = []
                elif event.button == 3:
                    grid[xtile][ytile] = False
                    generations = 0
                    lastDrawnGrid = []
                elif event.button == 2:
                    print "Neighbors: " + str(get_num_neighbors(xtile, ytile))

        pygame.display.update()

    pygame.quit()

