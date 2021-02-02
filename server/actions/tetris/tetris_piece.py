class TetrisPiece:
    def __init__(self, body_arr, piece_type, color):
        self.body_arr = body_arr
        self.piece_type = piece_type
        self.color = color

        self.__find_dims()
        self.__find_under_positions()
        self.__find_left_positions()
        self.__find_right_positions()

    def __eq__(self, other):
        if isinstance(other, TetrisPiece):
            return self.body_arr == other.body_arr
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __find_dims(self):
        min_x, min_y, max_x, max_y = 100, 100, -1, -1

        for x, y in self.body_arr:
            min_x, min_y = min(min_x, x), min(min_y, y)
            max_x, max_y = max(max_x, x), max(max_y, y)

        print(f'min_x: {min_x}, min_y: {min_y}, max_x: {max_x}, max_y: {max_y}')
        
        self.width = max_x - min_x + 1
        self.height = max_y - min_y + 1

        print(f'width: {self.width}, height: {self.height}')

    def __find_under_positions(self):
        self.under_positions = [(i, 100) for i in range(self.width)]

        for x, y in self.body_arr:
            self.under_positions[x] = (x, min(self.under_positions[x][1], y - 1))

    def __find_left_positions(self):
        self.left_positions = [(100, i) for i in range(self.height)]

        for x, y in self.body_arr:
            self.left_positions[y] = (min(self.left_positions[y][0], x - 1), y)

    def __find_right_positions(self):
        self.right_positions = [(-10, i) for i in range(self.height)]

        for x, y in self.body_arr:
            self.right_positions[y] = (max(self.right_positions[y][0], x + 1), y)

    def make_next_tetris_piece(self):
        inverted = [(y, x) for x, y in self.body_arr]
        reflected = [(x, self.width - y - 1) for x, y in inverted]
        return self.__class__(reflected, self.piece_type, self.color)

    def set_next_piece(self, next_piece):
        self.next_piece = next_piece

    def get_next_piece(self):
        return self.next_piece

    def set_curr_pos(self, x, y):
        self.curr_pos = (x, y)

    def get_curr_pos(self):
        return self.curr_pos


        




