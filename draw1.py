# Import module
import pygame

# Open function drawing without this function we cant use draw
def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

# Color section
    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)

# Coordination of drawing
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

# This is the functions for requirements that we need to add in this game
def draw_rectangle(screen, start, end, width, color_mode):
    pygame.draw.rect(screen, color_mode, pygame.Rect(start[0], start[1], end[0]-start[0], end[1]-start[1]), width)

def draw_circle(screen, center, radius, color_mode):
    pygame.draw.circle(screen, color_mode, center, radius)

def erase(screen, position, radius):
    pygame.draw.circle(screen, (0, 0, 0), position, radius)

# Initialize and set display
def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

# Parameters for drawing
    radius = 15
    mode = 'blue'
    draw_mode = 'line'  # Added draw_mode to switch between line, rectangle, and circle
    points = []
    drawing = False
    erasing = False

# This is the loops for changing the atributes like colors or modes
    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                elif event.key == pygame.K_e:
                    erasing = not erasing
                elif event.key == pygame.K_1:  # Press '1' for line mode
                    draw_mode = 'line'
                elif event.key == pygame.K_2:  # Press '2' for rectangle mode
                    draw_mode = 'rectangle'
                elif event.key == pygame.K_3:  # Press '3' for circle mode
                    draw_mode = 'circle'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    points.append(event.pos)
                elif event.button == 3:
                    erasing = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    points.clear()
                elif event.button == 3:
                    erasing = False

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    points.append(event.pos)
                elif erasing:
                    erase(screen, event.pos, radius)

        screen.fill((0, 0, 0))

# loop for forms of drawing like rectangle or circle
        if draw_mode == 'line':
            for i in range(len(points) - 1):
                drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
        elif draw_mode == 'rectangle' and len(points) >= 2:
            draw_rectangle(screen, points[0], points[-1], radius, mode)
        elif draw_mode == 'circle' and len(points) >= 2:
            center = points[0]
            dx = points[-1][0] - center[0]
            dy = points[-1][1] - center[1]
            radius = int((dx * dx + dy * dy) ** 0.5)
            draw_circle(screen, center, radius, mode)

        pygame.display.flip()
        clock.tick(60)

main()