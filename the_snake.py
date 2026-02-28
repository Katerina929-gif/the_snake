"""Программа реализует классическую игру 'Змейка' на библиотеке Pygame."""

from random import choice, randint
from typing import List, Optional, Tuple, Union

import pygame as pg

# Определяем алиасы для чистоты кода
Point = tuple[int, int]
Color = tuple[int, int, int]

# Константа для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Направление движения:
UP: Point = (0, -1)
DOWN: Point = (0, 1)
LEFT: Point = (-1, 0)
RIGHT: Point = (1, 0)

# Цвет фона - черный:
DEFAULT_COLOR = (255, 255, 255)
BOARD_BACKGROUND_COLOR: Color = (0, 0, 0)
BORDER_COLOR: Color = (93, 216, 228)
APPLE_COLOR: Color = (255, 0, 0)
SNAKE_COLOR: Color = (0, 255, 0)

# Скорость:
SPEED: int = 20

COLOR = Union[Tuple[int, int, int], str, pg.Color]
# Настройки игрового окна:
screen: pg.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock: pg.time.Clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color: COLOR = DEFAULT_COLOR) -> None:
        """Инициализация базовых атрибутов объекта."""
        self.position: Point = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self) -> None:
        """Метод для отрисовки объектов."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self, occupied_positions: Optional[List[Point]] = None,
                 body_color: COLOR = APPLE_COLOR) -> None:
        """Инициализация яблока с проверкой позиции змейки."""
        super().__init__(body_color=body_color)
        self.body_color = APPLE_COLOR
        if occupied_positions is None:
            occupied_positions = [self.position]
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_position: List[Point]) -> None:
        """Устанавливает случайную позицию яблока на поле."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_position:
                break

    def draw(self) -> None:
        """Отрисовывает яблоко на экране."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self, body_color: COLOR = SNAKE_COLOR) -> None:
        """Инициализация начального состояния змейки."""
        super().__init__(body_color=body_color)
        self.length: int = 1
        self.positions: List[Point] = [self.position]
        self.direction: Point = RIGHT
        self.next_direction: Optional[Point] = None
        self.body_color: Color = SNAKE_COLOR

    def update_direction(self) -> None:
        """Обновляет направление после нажатия клавиши."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Логика движения змейки."""
        cur_head = self.get_head_position()
        x, y = self.direction
        new_position = ((cur_head[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                        (cur_head[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    def get_head_position(self) -> Point:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def draw(self) -> None:
        """Отрисовывает змейку, выделяя голову."""
        for position in self.positions:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)


def handle_keys(game_object) -> None:
    """Обрабатывает нажатия клавиш для изменения направления."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основная логика игры и цикл отрисовки."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        """Проверка: съела ли змея яблоко."""

        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            apple.randomize_position(snake.positions)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
