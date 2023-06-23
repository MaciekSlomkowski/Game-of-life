import pygame
import numpy as np
import button

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (50, 50, 255)
RED = (220, 20, 60)
MENUCOLOR = (100, 149, 237)


class GameOfLife:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.cell_color = BLACK
        self.running = False
        self.FPS = 30
        self.ROWS = 30
        self.COLS = 40
        self.WIDTH = 800
        self.HEIGHT = 600
        self.CELL_SIZE = self.WIDTH // self.COLS, self.HEIGHT // self.ROWS
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.grid = self.create_grid()

    def change_size(self, size):
        """
        receives size string, (either of "small" ,"normal", "big")
        and changes size of the cell
        size = 800X600
        """
        if size == "small":
            self.ROWS, self.COLS = 30, 40
        elif size == "normal":
            self.ROWS, self.COLS = 60, 80
        elif size == "big":
            self.ROWS, self.COLS = 125, 150

        self.CELL_SIZE = self.WIDTH // self.COLS, self.HEIGHT // self.ROWS

        self.grid = self.create_grid()

    def create_grid(self):
        """
        Creates empyt board
        """
        return np.zeros((self.ROWS, self.COLS), dtype=bool)

    def draw_grid(self):
        self.screen.fill(WHITE)
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.grid[row][col]:
                    pygame.draw.rect(self.screen, self.cell_color, (col * self.CELL_SIZE[0], row * self.CELL_SIZE[1],
                                                                    self.CELL_SIZE[0], self.CELL_SIZE[1]))

    def update_grid(self):
        """
        Updates grid for new epoch
        """
        new_grid = self.grid.copy()
        for row in range(self.ROWS):
            for col in range(self.COLS):
                neighbors = np.sum(self.grid[max(0, row - 1):min(row + 2, self.ROWS),
                                   max(0, col - 1):min(col + 2, self.COLS)]) - self.grid[row][col]
                if self.grid[row][col]:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[row][col] = False
                else:
                    if neighbors == 3:
                        new_grid[row][col] = True
        return new_grid

    def get_cell_pos(self, mouse_pos):
        """
        Returns cell clicked
        """
        x, y = mouse_pos
        col = x // self.CELL_SIZE[0]
        row = y // self.CELL_SIZE[1]
        return row, col

    def start_screen(self):
        """
        Displays starting screem
        """
        while True:
            self.screen.fill(MENUCOLOR)
            title_font = pygame.font.Font("PokemonGb-RAeo.ttf", 36)
            subtitle_font = pygame.font.Font("PokemonGb-RAeo.ttf", 14)  # smaller font for subtitle

            title_text = title_font.render("Game of Life", True, WHITE)
            subtitle_text = subtitle_font.render("press spacebar to continue", True, WHITE)  # New subtitle text

            title_pos = title_text.get_rect(
                center=(self.WIDTH // 2, self.HEIGHT // 2 - 50))  # tomake room for subtitle
            subtitle_pos = subtitle_text.get_rect(
                center=(self.WIDTH // 2, self.HEIGHT // 2 + 10))  # position of subtitle

            self.screen.blit(title_text, title_pos)
            self.screen.blit(subtitle_text, subtitle_pos)  # draw subtitle on screen

            pygame.display.flip()
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True

    def change_color(self, color):
        """
        recieves color string, (either of "BLACK" ,"GREEN", "BLUE", "RED")
        and changes color of the cells
        """
        colors = {
            'BLACK': BLACK,
            'GREEN': GREEN,
            'BLUE': BLUE,
            'RED': RED
        }
        self.cell_color = colors.get(color)

    def second_screen(self):
        """
        Displays second screen with some info
        """
        while True:
            self.screen.fill(MENUCOLOR)
            font = pygame.font.Font("PokemonGb-RAeo.ttf", 16)
            options = ['To pause and resume the game press SPACEBAR',
                       'To run one epoch press right arrow key',
                       'To open menu press Escape key']
            for i, option in enumerate(options):
                text = font.render(option, True, WHITE)
                self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2,
                                        (self.HEIGHT // 2 - text.get_height() // 2 + i * 100) - 100))
            pygame.display.flip()
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True

    def fps_menu(self):
        """
        Displays FPS menu
        """
        fps15_img = pygame.image.load("images/button_15fps.png").convert_alpha()
        fps30_img = pygame.image.load("images/button_30fps.png").convert_alpha()
        fps60_img = pygame.image.load("images/button_60fps.png").convert_alpha()

        fps15_button = button.Button(150, 150, fps15_img, 1)
        fps30_button = button.Button(320, 150, fps30_img, 1)
        fps60_button = button.Button(490, 150, fps60_img, 1)

        while True:
            self.screen.fill(MENUCOLOR)

            fps15_button.draw(self.screen)
            fps30_button.draw(self.screen)
            fps60_button.draw(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 'quit'
                elif event.type == pygame.MOUSEBUTTONUP:
                    if fps15_button.rect.collidepoint(event.pos):
                        self.FPS = 15
                        return 'back'
                    elif fps30_button.rect.collidepoint(event.pos):
                        self.FPS = 30
                        return 'back'
                    elif fps60_button.rect.collidepoint(event.pos):
                        self.FPS = 60
                        return 'back'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        return 'back'

    def size_menu(self):
        small_img = pygame.image.load("images/button_small.png").convert_alpha()
        normal_img = pygame.image.load("images/button_normal.png").convert_alpha()
        big_img = pygame.image.load("images/button_big.png").convert_alpha()

        small_button = button.Button(150, 250, small_img, 1)
        normal_button = button.Button(320, 250, normal_img, 1)
        big_button = button.Button(510, 250, big_img, 1)

        while True:
            self.screen.fill(MENUCOLOR)
            if small_button.draw(self.screen):
                pygame.time.delay(200)  # add delay here
                self.change_size("small")
                return 'back'
            if normal_button.draw(self.screen):
                pygame.time.delay(200)  # add delay here
                self.change_size("normal")
                return 'back'
            if big_button.draw(self.screen):
                pygame.time.delay(200)  # add delay here
                self.change_size("big")
                return 'back'

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or pygame.K_ESCAPE:
                        return 'back'

    def color_menu(self):
        black_img = pygame.image.load("images/button_black.png").convert_alpha()
        green_img = pygame.image.load("images/button_green.png").convert_alpha()
        blue_img = pygame.image.load("images/button_blue.png").convert_alpha()
        red_img = pygame.image.load("images/button_red.png").convert_alpha()
        while True:
            self.screen.fill(MENUCOLOR)
            black_button = button.Button(70, 250, black_img, 1)
            green_button = button.Button(245, 250, green_img, 1)
            blue_button = button.Button(425, 250, blue_img, 1)
            red_button = button.Button(590, 250, red_img, 1)

            if black_button.draw(self.screen):
                self.change_color('BLACK')
                return
            elif green_button.draw(self.screen):
                self.change_color('GREEN')
                return
            elif blue_button.draw(self.screen):
                self.change_color('BLUE')
                return
            elif red_button.draw(self.screen):
                self.change_color('RED')
                return

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False

    def menu(self):
        """
        Displays menu interface
        """
        fps_img = pygame.image.load("images/button_fps.png").convert_alpha()
        size_img = pygame.image.load("images/button_size.png").convert_alpha()
        color_img = pygame.image.load("images/button_color.png").convert_alpha()
        fps_button = button.Button(150, 50, fps_img, 1)
        size_button = button.Button(300, 50, size_img, 1)
        color_button = button.Button(460, 50, color_img, 1)

        while True:
            self.screen.fill(MENUCOLOR)
            if fps_button.draw(self.screen):
                if self.fps_menu() == 'back':
                    return
            if size_button.draw(self.screen):
                pygame.time.delay(200)
                if self.size_menu() == 'back':  # check for the 'back' signal
                    return
            if color_button.draw(self.screen):
                self.color_menu()

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or pygame.K_ESCAPE:
                        return True

    def run(self):
        if not self.start_screen():
            return
        if not self.second_screen():
            return

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = not self.running
                    elif event.key == pygame.K_c:
                        self.grid = self.create_grid()
                    elif event.key == pygame.K_RIGHT:
                        self.grid = self.update_grid()
                        self.draw_grid()
                    elif event.key == pygame.K_ESCAPE:
                        self.menu()
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.running:
                    if event.button == 1:
                        row, col = self.get_cell_pos(pygame.mouse.get_pos())
                        self.grid[row][col] = not self.grid[row][col]

            if self.running:
                self.grid = self.update_grid()

            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(self.FPS)
