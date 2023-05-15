
class Snake:
    def __init__(self, position, direction):
        self.segments = [position, (position[0] - direction[0], position[1] - direction[1])]
        self.direction = direction
        self.block_direction = False

    def change_direction(self, new_direction):

        if not self.block_direction:
            if (new_direction[0], new_direction[1]) != (-self.direction[0], -self.direction[1]):
                self.direction = new_direction

        self.block_direction = True

    def get_next_position(self):
        self.block_direction = False
        next_position = (self.segments[0][0] + self.direction[0], self.segments[0][1] + self.direction[1])
        return next_position

    def move(self):
        next_position = self.get_next_position()
        self.segments.pop()
        self.segments.insert(0, next_position)

    def is_collision(self):
        return self.get_head() in self.segments[1:]

    def get_head(self):
        return self.segments[0]

    def get_segments(self):
        return self.segments

    def grow(self):
        last_segment = self.segments[-1]
        second_last_segment = self.segments[-2]

        delta_x = last_segment[1] - second_last_segment[1]
        delta_y = last_segment[0] - second_last_segment[0]

        new_segment = (last_segment[0] + delta_y, last_segment[1] + delta_x)
        self.segments.append(new_segment)

    def get_length(self):
        return len(self.segments)
