# Python 3.11.0
import pygame
import sys
import random
import time


class Snake:
    '''
    A class to create and run the Snake game.

    Attributes:
        BLACK (tuple(int,int,int)): The color black (in RGB format).
        WHITE (tuple(int,int,int)): The color white (in RGB format).
        RED (tuple(int,int,int)): The color red (in RGB format).

        BLANK (int): Value to represent a blank tile on the board.
        SNAKE (int): Value to represent a snake tile on the board.
        APPLE (int): Value to represent an apple tile on the board.

        WINDOW_WIDTH (int): How wide the game window will be (in pixels).
        WINDOW_HEIGHT (int): How tall the game window will be (in pixels).
        BLOCK_SIZE (int): How wide each block will be (in pixels).

        board (list(list(int))): A list to represent all of the tiles in the window.
        direction (int): The direction that the snake is travelling in (-1 = N/A, 0 = up, 1 = right, 2 = down, 3 = left).
        snake_coords (list(tuple(int,int))): List of coordinates that the snake occupies.

    Methods:
        start(): Opens the pygame window and starts the game.
        move(): Moves the player by 1 pixel.
        spawn_snake(): Creates the first snake pixel.
        spawn_apple(): Creates an apple at a random coordinate.
        has_win() --> bool: Determines if the player has won or not.
        trigger_win(): Exits the program
        trigger_loss(): Exits the program
        draw_grid(): Draws the screen with each square representing the snake or an apple.
    '''


    def __init__(self, window_width : int, window_height : int, block_size : int):
        '''
        Constructs all the necessary attributes for the Snake object.

        Parameters:
            window_width (int): How wide the game window will be (in pixels).
            window_height (int): How tall the game window will be (in pixels).
            block_size (int): How wide each block will be (in pixels).
        '''
        # Define colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (200, 200, 200)
        self.RED = (200, 0, 0)

        # Define board values
        self.BLANK = 0
        self.SNAKE = 1
        self.APPLE = 2

        # Define window constraints
        self.WINDOW_WIDTH = window_width
        self.WINDOW_HEIGHT = window_height
        self.BLOCK_SIZE = block_size

        # Define game vars
        self.board = []
        self.direction = -1
        self.snake_coords = []

        # Populate board
        for x in range(0, self.WINDOW_WIDTH, self.BLOCK_SIZE):
            l = []
            for y in range(0, self.WINDOW_HEIGHT, self.BLOCK_SIZE):
                l.append(self.BLANK)
            self.board.append(l)
        
        self.spawn_snake()
        self.spawn_apple() 


    def start(self):
        '''
        Starts the game and creates the pygame window.
        The player is stationary to begin and will start moving
        once any of the arrow keys are pressed.
        '''
        pygame.init()
        pygame.display.set_caption('Snake')
        self.SCREEN = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.CLOCK = pygame.time.Clock()
        self.SCREEN.fill(self.BLACK)

        while True:
            self.move()
            self.draw_grid()
            if self.has_win():
                self.trigger_win()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Up arrow pressed
                    if event.key == pygame.K_UP:
                        if self.direction != 2:
                            self.direction = 0
                    # Right arrow pressed
                    elif event.key == pygame.K_RIGHT:
                        if self.direction != 3:
                            self.direction = 1
                    # Down arrow pressed
                    elif event.key == pygame.K_DOWN:
                        if self.direction != 0:
                            self.direction = 2
                    # Left arrow pressed
                    elif event.key == pygame.K_LEFT:
                        if self.direction != 1:
                            self.direction = 3

            pygame.display.update()
            time.sleep(0.1) # Tick speed
    

    def move(self):
        '''
        Moves the player by 1 pixel in the current direction
        (as defined by self.direction).
        If the player moves onto an apple, the snake length will
        increase by 1, and a new apple will be spawned. If the snake
        runs into a wall or runs into itself, self.trigger_loss() will be executed.
        '''
        old_head = self.snake_coords[0]
        if self.direction == 0:
            # North
            new_coords = (old_head[0], old_head[1] - 1)
        elif self.direction == 1:
            # East
            new_coords = (old_head[0] + 1, old_head[1])
        elif self.direction == 2:
            # South
            new_coords = (old_head[0], old_head[1] + 1)
        elif self.direction == 3:
            # West
            new_coords = (old_head[0] - 1, old_head[1])
        else:
            return
        
        # Out of bounds on X
        if new_coords[0] < 0 or new_coords[0] > (self.WINDOW_WIDTH // self.BLOCK_SIZE) - 1:
            self.trigger_loss()
            return
        
        # Out of bounds on Y
        if new_coords[1] < 0 or new_coords[1] > (self.WINDOW_HEIGHT // self.BLOCK_SIZE) - 1:
            self.trigger_loss()
            return
        
        # Snake hits itself
        if self.board[new_coords[0]][new_coords[1]] == self.SNAKE:
            self.trigger_loss()
            return
        
        # Remove tail (don't spawn new apple)
        if self.board[new_coords[0]][new_coords[1]] != self.APPLE:
            tail = self.snake_coords.pop(len(self.snake_coords) - 1)
            self.board[tail[0]][tail[1]] = self.BLANK
        else:
            # Spawn apple
            self.spawn_apple()

        # Add new head
        self.snake_coords.insert(0, new_coords)
        self.board[new_coords[0]][new_coords[1]] = self.SNAKE

        
    def spawn_snake(self):
        '''
        Spawns the snake at a random location at the very beginning of the game.
        '''
        x = random.randint(0, (self.WINDOW_WIDTH // self.BLOCK_SIZE) - 1)
        y = random.randint(0, (self.WINDOW_HEIGHT // self.BLOCK_SIZE) - 1)

        self.snake_coords.append((x, y))
        self.board[x][y] = self.SNAKE


    def spawn_apple(self):
        '''
        Spawns a new apple on the board. Function checks and doesn't
        spawn any apples on top of the snake.
        '''
        if self.has_win():
            return
        x = random.randint(0, (self.WINDOW_WIDTH // self.BLOCK_SIZE) - 1)
        y = random.randint(0, (self.WINDOW_HEIGHT // self.BLOCK_SIZE) - 1)

        while self.board[x][y] != 0:
            x = random.randint(0, (self.WINDOW_WIDTH // self.BLOCK_SIZE) - 1)
            y = random.randint(0, (self.WINDOW_HEIGHT // self.BLOCK_SIZE) - 1)

        self.board[x][y] = self.APPLE
    

    def has_win(self):
        '''
        Determines if the snake is long enough to constitute a win.

        Returns:
            has_win (bool): Bool for whether or not all squares are taken by the snake.
        '''
        total_squares = (self.WINDOW_WIDTH // self.BLOCK_SIZE) * (self.WINDOW_HEIGHT // self.BLOCK_SIZE)
        return total_squares <= len(self.snake_coords)


    def trigger_win(self):
        '''
        Function that is run after the player wins by occupying every square.
        This function will simply exit the program.
        '''
        pygame.quit()
        sys.exit()


    def trigger_loss(self):
        '''
        Function that is run after the player collides with a wall or collides with themselves.
        This function will simply exit the program.
        '''
        pygame.quit()
        sys.exit()


    def draw_grid(self):
        '''
        Draws the grid and colors each square depending on if
        there is an apple or snake using the self.board variable.
        '''
        for x in range(0, self.WINDOW_WIDTH, self.BLOCK_SIZE):
            for y in range(0, self.WINDOW_HEIGHT, self.BLOCK_SIZE):
                square = self.board[x // self.BLOCK_SIZE][y // self.BLOCK_SIZE]

                rect = pygame.Rect(x, y, self.BLOCK_SIZE, self.BLOCK_SIZE)

                if square == self.BLANK:
                    pygame.draw.rect(self.SCREEN, self.BLACK, rect)
                elif square == self.APPLE:
                    pygame.draw.rect(self.SCREEN, self.RED, rect)
                elif square == self.SNAKE:
                    pygame.draw.rect(self.SCREEN, self.WHITE, rect)


def main():
    snake = Snake(400, 400, 20)
    snake.start()


if __name__ == "__main__":
    main()
