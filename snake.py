from random import randrange, choice
from time import sleep

import curses
from curses import wrapper

class Apple:
    character = "🍎"

    def __init__(self, color, screen):
        self.color = color
        self.screen = screen
        self.eaten = False
        self.y, self.x = randrange(0, screen.getmaxyx()[0]), randrange(0, screen.getmaxyx()[1])
        self.pos = [self.y, self.x]

    def draw(self):
        self.screen.addch(*self.pos, self.character, self.color)


class Snake:
    up, right, down, left = "up", "", "down", "left"
    directions = [up, right, down, left]

    character = "⬤"

    def __init__(self, screen, size, color, head_color=None):
        self.alive = True
        self.direction = choice([self.up, self.down, self.left])
        self.color = color
        self.head_color = head_color if head_color else color
        self.screen = screen
        self.score = 0

        max_y, max_x = screen.getmaxyx()
        self.snake = [[max_y // 2, max_x // 2 + i] for i in range(size + 1)]
        self.head = self.snake[0]

    def draw(self):
        for segment in self.snake:
            if segment == self.head:
                self.screen.addch(*self.head, self.character, self.head_color)

            else:
                self.screen.addch(*segment, self.character, self.color)

    def update(self, apple):
        if self.alive:
            if apple.pos == self.head:
                apple.eaten = True
                self.score += 1

            else:
                del self.snake[-1]

            if self.head in self.snake[1:]:
                self.alive = False
                self.screen.clear()
                self.screen.addstr(self.screen.getmaxyx()[0] // 2, self.screen.getmaxyx()[1] // 2 - 4, "GAME OVER", self.color)
                self.screen.refresh()
                sleep(3)
                return
            
            y, x = self.head

            # New Syntax, Can Be Used With Python3.10.x+
            match self.direction:
                case self.up:
                    new_segment = [(y - 1) % self.screen.getmaxyx()[0], x]

                case self.right:
                    new_segment = [y, (x + 1) % self.screen.getmaxyx()[1]]

                case self.down:
                    new_segment = [(y + 1) % self.screen.getmaxyx()[0], x]

                case self.left:
                    new_segment = [y, (x - 1) % self.screen.getmaxyx()[1]]

            self.snake.insert(0, new_segment)
            self.head = self.snake[0]

def setup(screen, apple_color, snake_color, head_color = None, size = 3):
    return Snake(screen, size, snake_color, head_color), Apple(apple_color, screen)

def main(screen):
    screen.clear()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    apple_color = curses.color_pair(1)
    snake_color = curses.color_pair(2)
    head_color = curses.color_pair(3)

    snake, apple = setup(screen, apple_color, snake_color, head_color)
    paused = False
    screen.nodelay(1)

    while snake.alive:
        screen.clear()

        key = screen.getch()

        if (key == ord("w") or key == curses.KEY_UP) and snake.direction != snake.down:
            snake.direction = snake.up

        elif (key == ord("d") or key == curses.KEY_RIGHT) and snake.direction != snake.left:
            snake.direction = snake.right

        elif (key == ord("s") or key == curses.KEY_DOWN) and snake.direction != snake.up:
            snake.direction = snake.down

        elif (key == ord("a") or key == curses.KEY_LEFT) and snake.direction != snake.right:
            snake.direction = snake.left
        elif key == ord(" "):
            paused = not paused
        
        snake.update(apple)

        if apple.eaten:
            apple = Apple(apple_color, screen)

        apple.draw()
        snake.draw()

        screen.addstr(0, 0, str(snake.score))

        screen.refresh()
        sleep(0.15)


wrapper(main)