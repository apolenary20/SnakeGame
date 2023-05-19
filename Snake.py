class Snake:
    """
    Класс Snake представляет собой модель змейки в игре.
    Она имеет позицию, направление движения и может расти в длину.
    """

    def __init__(self, position, direction):
        """
        Создает новый объект Snake.

        Args:
            position (tuple): Координаты начальной позиции змейки.
            direction (tuple): Направление движения змейки.
        """
        self.segments = [position, (position[0] - direction[0], position[1] - direction[1])]
        self.direction = direction
        self.block_direction = False

    def change_direction(self, new_direction):
        """
        Изменяет направление движения змейки.

        Args:
            new_direction (tuple): Новое направление движения.
        """
        if not self.block_direction:
            if (new_direction[0], new_direction[1]) != (-self.direction[0], -self.direction[1]):
                self.direction = new_direction

        self.block_direction = True

    def move(self, next_position):
        """
        Перемещает змейку в следующую позицию.

        Args:
            next_position (tuple): Координаты следующей позиции.
        """
        self.segments.pop()
        self.segments.insert(0, next_position)

    def is_collision(self):
        """
        Проверяет, произошло ли столкновение змейки со своим телом.

        Returns:
            bool: True, если произошло столкновение, иначе False.
        """
        return self.get_head() in self.segments[1:]

    def get_head(self):
        """
        Возвращает координаты головы змейки.

        Returns:
            tuple: Координаты головы змейки.
        """
        return self.segments[0]

    def get_segments(self):
        """
        Возвращает все сегменты змейки.

        Returns:
            list: Список координат всех сегментов змейки.
        """
        return self.segments

    def grow(self):
        """
        Увеличивает размер змейки, добавляя новый сегмент в конец.
        """
        last_segment = self.segments[-1]
        second_last_segment = self.segments[-2]

        delta_x = last_segment[1] - second_last_segment[1]
        delta_y = last_segment[0] - second_last_segment[0]

        new_segment = (last_segment[0] + delta_y, last_segment[1] + delta_x)
        self.segments.append(new_segment)

    def get_length(self):
        """
        Возвращает длину змейки.

        Returns:
            int: Длина змейки.
        """
        return len(self.segments)
