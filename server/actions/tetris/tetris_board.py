from .tetris_piece import TetrisPiece
from random import randrange

# define grid positions of default-orientation tetris pieces
STICK = [(0, 0), (0, 1), (0, 2), (0, 3)]
L = [(0, 0), (0, 1), (0, 2), (1, 0)]
L2 = [(0, 0), (1, 0), (1, 1), (1, 2)]
S = [(0, 0), (1, 0), (1, 1), (2, 1)]
S2 = [(0, 1), (1, 1), (1, 0), (2, 0)]
SQUARE = [(0, 0), (0, 1), (1, 0), (1, 1)]
PYRAMID = [(0, 0), (1, 0), (2, 0), (1, 1)]

# put all basic pieces in an array
BASIC_PIECES = [("stick", STICK, (0, 255, 255)), 
                ("l", L, (255, 165, 0)), 
                ("l2", L2, (0, 0, 255)), 
                ("s", S, (0, 128, 0)), 
                ("s2", S2, (255, 0, 0)), 
                ("square", SQUARE, (255, 255, 0)), 
                ("pyramid", PYRAMID, (255, 0, 255))] 

# set width and height
WIDTH = 10
HEIGHT = 20

# start at position x = 18, y = 3

class TetrisBoard:
    def __init__(self, matrix):
        self.width = 10
        self.height = 20
        self.padded_height = self.height + 5
        self.matrix = matrix
        self.game_over = False

        # rows is our main inner representation of the tetris grid
        self.rows = [[0 for _ in range(self.width)] for _ in range(self.padded_height)]

        # number of occupied blocks per row
        self.row_counts = [ 0 for _ in range(self.padded_height)]

        # number of occupied blocks per column
        self.heights = [ 0 for _ in range(self.width)]

        self.__build_pieces()

    def __build_pieces(self):
        """initialize all pieces (including different rotations) from BASIC_PIECES"""
        self.piece_names = []
        self.pieces = {}

        for name, body_arr, rgb_color in BASIC_PIECES:
            # add entries to piece_names and pieces
            self.piece_names.append(name)
            self.pieces[name] = []

            # create piece at default rotation
            curr_piece = TetrisPiece(body_arr, name, self.matrix.get_color(*rgb_color))
            
            # for each piece
            for i in range(3):
                # make the next piece
                next_piece = curr_piece.make_next_tetris_piece()
                # set it as next to curr piece
                curr_piece.set_next_piece(next_piece)
                # add curr piece to pieces
                self.pieces[name].append(curr_piece)
                # update curr piece to next piece
                curr_piece = next_piece
            
            # set the next piece of the curr piece to the default rotation and add to pieces
            curr_piece.set_next_piece(self.pieces[name][0])
            self.pieces[name].append(curr_piece)

    def get_random_piece(self):
        piece_type = self.piece_names[randrange(len(self.piece_names))]
        return self.pieces[piece_type][randrange(4)]

    def draw_frame(self):
        x_left, x_right = 17, 28
        y_top, y_bottom = self.matrix.num_rows() - 3, self.matrix.num_rows() - 24
        color = self.matrix.get_color(100, 100, 100)

        for j in range(x_left, x_right + 1):
            self.matrix[y_top, j] = color
            self.matrix[y_bottom, j] = color

        for i in range(y_bottom, y_top + 1):
            self.matrix[i, x_left] = color
            self.matrix[i, x_right] = color

        self.update_matrix()

    def draw_pos(self, x, y, color):
        """add a position to matrix without calling matrix.draw()"""
        if self.check_in_bounds(x, y) and y < self.height:
            self.matrix[self.matrix.num_rows() - y - 4, x + 18] = color

    def update_matrix(self):
        self.matrix.show()

    def draw_curr_piece(self):
        """add the current piece to matrix without calling matrix.draw()"""
        piece_x, piece_y = self.curr_piece.get_curr_pos()
        for relative_x, relative_y in self.curr_piece.body_arr:
            x_pos, y_pos = piece_x + relative_x, piece_y + relative_y
            self.draw_pos(x_pos, y_pos, self.curr_piece.color)

    def undraw_curr_piece(self):
        """set the color of the current piece to black without calling matrix.draw()"""
        piece_x, piece_y = self.curr_piece.get_curr_pos()
        for relative_x, relative_y in self.curr_piece.body_arr:
            x_pos, y_pos = piece_x + relative_x, piece_y + relative_y
            self.draw_pos(x_pos, y_pos, 0)

    def draw_grid(self):
        """add all grid blocks to matrix without calling draw()"""
        for i in range(self.height):
            row = self.rows[i]
            for j, color in enumerate(row):
                self.draw_pos(j, i, color)

    def place(self):
        """once a tetris piece reaches the bottom of the grid, place it there"""
        piece_x, piece_y = self.curr_piece.get_curr_pos()
        for relative_x, relative_y in self.curr_piece.body_arr:
            x_pos, y_pos = piece_x + relative_x, piece_y + relative_y
            self.rows[y_pos][x_pos] = self.curr_piece.color
            self.heights[x_pos] = max(self.heights[x_pos], self.curr_piece.get_curr_pos()[1] + y_pos)
            self.row_counts[y_pos] += 1

    def clear_rows(self):
        """clear all rows that have been completed and remove them from the grid"""
        rows_to_clear = []

        # find rows to clear and save their index
        for n, width in enumerate(self.row_counts):
            if width == self.width:
                rows_to_clear.append(n)

        rows_to_clear.reverse()

        # delete each row
        for row_num in rows_to_clear:
            del self.rows[row_num]
            heights_to_decrease = []

            # decrease the height of any column with blocks above the cleared row
            for n, height in enumerate(self.heights):
                if height > row_num:
                    heights_to_decrease.append(n)
            
            for col_num in heights_to_decrease:
                self.heights[col_num] -= 1
        
        # add new empty rows for every deleted row
        for _ in rows_to_clear:
            self.rows.append([0 for _ in range(self.width)])
        
        # if we have cleared a row, recalculate row_counts
        if len(rows_to_clear) > 0:
            self.row_counts = [sum([(1 if x > 0 else 0) for x in row]) for row in self.rows]

        return len(rows_to_clear)

    def __detect_collision(self, piece_pos, collision_positions, x_offset=0, y_offset=0):
        """Helper function to detect left, right and under collisions"""
        piece_x, piece_y = piece_pos

        for relative_x, relative_y in collision_positions:
            x_pos = piece_x + relative_x + x_offset
            y_pos = piece_y + relative_y + y_offset

            if not self.check_in_bounds(x_pos, y_pos):
                return True
            
            if y_pos < self.height and self.rows[y_pos][x_pos] != 0:
                return True
        return False

    def detect_left_collision(self):
        return self.__detect_collision(self.curr_piece.get_curr_pos(), self.curr_piece.left_positions)

    def detect_right_collision(self):
        return self.__detect_collision(self.curr_piece.get_curr_pos(), self.curr_piece.right_positions)

    def detect_under_collision(self):
        return self.__detect_collision(self.curr_piece.get_curr_pos(), self.curr_piece.under_positions)


    def check_in_bounds(self, x, y):
        """checks whether a position is within the left and right walls, 
        and whether the position is above the ground
        """
        return x >= 0 and y >= 0 and x < 10

    def check_end_condition(self):
        for i in range(self.height, self.padded_height):
            if self.row_counts[i] > 0:
                return True
        return False

    def drop_random_piece(self):
        to_drop = self.get_random_piece()
        start_x, start_y = int((self.width / 2) - (to_drop.width / 2)), self.height - 1
        to_drop.set_curr_pos(start_x, start_y)
        self.curr_piece = to_drop
        self.draw_curr_piece()
        self.update_matrix()

    def rotate(self):
        next_piece = self.curr_piece.get_next_piece()
        collision = self.__detect_collision(self.curr_piece.get_curr_pos(), next_piece.body_arr)
        if not collision:
            self.undraw_curr_piece()
            next_piece.set_curr_pos(*self.curr_piece.get_curr_pos())
            self.curr_piece = next_piece
            self.draw_curr_piece()
            self.update_matrix()

    def move_sideways(self, direction):
        offset = 1 if direction == 'r' else -1
        collision = self.detect_right_collision() if direction == 'r' else self.detect_left_collision()
        
        if not collision:
            self.undraw_curr_piece()
            curr_pos = self.curr_piece.get_curr_pos()
            new_x, new_y = curr_pos[0] + offset, curr_pos[1]
            self.curr_piece.set_curr_pos(new_x, new_y)
            self.draw_curr_piece()
            self.update_matrix()

    def move_down(self):
        collision = self.detect_under_collision()

        if collision:
            self.place()
            self.clear_rows()
            self.draw_grid()
            self.update_matrix()
            if self.check_end_condition():
                return 0
            self.drop_random_piece()
            return 1
        else:
            self.undraw_curr_piece()
            curr_pos = self.curr_piece.get_curr_pos()
            new_x, new_y = curr_pos[0], curr_pos[1] - 1
            self.curr_piece.set_curr_pos(new_x, new_y)
            self.draw_curr_piece()
            self.update_matrix()
            return 2
    
    def drop_down(self):
        move_down_result = 2
        while move_down_result == 2:
            move_down_result = self.move_down()

        if move_down_result == 0:
            self.game_over = True
        
        
        