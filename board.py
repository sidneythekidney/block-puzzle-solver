import piece

class Board:
    def __init__(self, board, board_rows, board_columns):
        self.board = board # Should be list of '.' and '*' representing empty and filled squares
        self.board_rows = board_rows
        self.board_columns = board_columns
        self.row_occupied_counts = [0] * board_rows
        self.column_occupied_counts = [0] * board_columns

        self.weights = {
            "num_squares_weight" : 0.8,
            "num_corners_weight" : 0.2
        }

        for row in range(0, board_rows):
            for column in range(0, board_columns):
                if board[self.get_square_from_row_and_column(row, column)] == '*':
                    self.row_occupied_counts[row] += 1
                    self.column_occupied_counts[column] += 1

        self.total_squares = self.board_rows * self.board_columns
        # Calculate total corners assuming square board
        self.total_corners = 4 * (self.board_rows - 2) * (self.board_columns - 2) + 6 * (self.board_rows + self.board_rows - 4) + 8
            
        self.EMPTY_SQUARE = '.'
        self.OCCUPIED_SQUARE = '*'

    def can_place_piece(self, piece, square):
        square_row, square_column = self.get_row_and_column_from_square(square)

        # Check if piece is out of bounds
        if square_row + piece.max_rows > self.board_rows or square_column + piece.max_columns > self.board_columns:
            return False

        # Check if board is already occupied
        for piece_square in piece.piece_squares:
            fill_square = self.get_square_from_row_and_column(square_row + piece_square[0], square_column + piece_square[1])
            if self.board[fill_square] == self.OCCUPIED_SQUARE:
                return False

        return True

    def place_piece(self, piece, square):
        square_row, square_column = self.get_row_and_column_from_square(square)

        deleted_rows = set()
        deleted_columns = set()

        for piece_square in piece.piece_squares:
            occupied_row = square_row + piece_square[0]
            occupied_column = square_column + piece_square[1]

            fill_square = self.get_square_from_row_and_column(occupied_row, occupied_column)
            self.board[fill_square] = self.OCCUPIED_SQUARE
            # Update the row and column counts
            self.row_occupied_counts[occupied_row] += 1
            self.column_occupied_counts[occupied_column] += 1
            
            # Add rows and columns to be deleted
            if (self.row_occupied_counts[occupied_row] == self.board_columns):
                deleted_rows.add(occupied_row)
            if (self.column_occupied_counts[occupied_column] == self.board_rows):
                deleted_columns.add(occupied_column)

        self.delete_rows_and_columns(deleted_rows, deleted_columns)

        return deleted_rows, deleted_columns

    def unplace_piece(self, piece, square, deleted_rows, deleted_columns):
        self.restore_rows_and_columns(deleted_rows, deleted_columns)
        square_row, square_column = self.get_row_and_column_from_square(square)

        for piece_square in piece.piece_squares:
            occupied_row = square_row + piece_square[0]
            occupied_column = square_column + piece_square[1]

            empty_square = self.get_square_from_row_and_column(occupied_row, occupied_column)
            self.board[empty_square] = self.EMPTY_SQUARE
            # Update the row and column counts
            self.row_occupied_counts[occupied_row] -= 1
            self.column_occupied_counts[occupied_column] -= 1

    def delete_rows_and_columns(self, deleted_rows, deleted_columns):
        # Delete full rows
        for row in deleted_rows:
            for occupied_square in range(row * self.board_columns, (row + 1) * self.board_columns):
                self.board[occupied_square] = self.EMPTY_SQUARE
            # Update row and column counts
            self.row_occupied_counts[row] = 0
            for column_number in range(self.board_columns):
                if column_number not in deleted_columns:
                    self.column_occupied_counts[column_number] -= 1

        # Delete full columns
        for column in deleted_columns:
            for occupied_square in range(column, self.board_rows * self.board_columns, self.board_columns):
                self.board[occupied_square] = self.EMPTY_SQUARE
            # Update row and column counts
            self.column_occupied_counts[column] = 0
            for row_number in range(self.board_rows):
                if row_number not in deleted_rows:
                    self.row_occupied_counts[row_number] -= 1

    def restore_rows_and_columns(self, restored_rows, restored_columns):
        # Delete full rows
        for row in restored_rows:
            for occupied_square in range(row * self.board_columns, (row + 1) * self.board_columns):
                self.board[occupied_square] = self.OCCUPIED_SQUARE
            # Update row and column counts
            self.row_occupied_counts[row] = 10
            for column_number in range(self.board_columns):
                if column_number not in restored_columns:
                    self.column_occupied_counts[column_number] += 1

        # Delete full columns
        for column in restored_columns:
            for occupied_square in range(column, self.board_rows * self.board_columns, self.board_columns):
                self.board[occupied_square] = self.OCCUPIED_SQUARE
            # Update row and column counts
            self.column_occupied_counts[column] = 10
            for row_number in range(self.board_rows):
                if row_number not in restored_rows:
                    self.row_occupied_counts[row_number] += 1

    def calculate_board_score(self):
        return self.calculate_num_squares() * self.weights["num_squares_weight"] + self.calculate_num_corners() * self.weights["num_corners_weight"]

    def calculate_num_squares(self):
        num_squares = 0
        for i in range(self.board_rows):
            for j in range(self.board_columns):
                if (self.board[self.get_square_from_row_and_column(i, j)] == self.OCCUPIED_SQUARE):
                    num_squares += 1
        return num_squares / self.total_squares

    def calculate_num_corners(self):
        num_corners = 0
        for i in range(self.board_rows):
            for j in range(self.board_columns):
                if (self.board[self.get_square_from_row_and_column(i, j)] == self.OCCUPIED_SQUARE):
                    # Check in all four directions to see if piece is surrounded
                    # Check above
                    if not i == 0 and self.board[self.get_square_from_row_and_column(i - 1, j)] == self.EMPTY_SQUARE:
                        num_corners += 1
                    # Check below
                    if not i == self.board_rows - 1 and self.board[self.get_square_from_row_and_column(i + 1, j)] == self.EMPTY_SQUARE:
                        num_corners += 1
                    # Check left
                    if not j == 0 and self.board[self.get_square_from_row_and_column(i, j - 1)] == self.EMPTY_SQUARE:
                        num_corners += 1
                    # Check right
                    if not j == self.board_columns - 1 and self.board[self.get_square_from_row_and_column(i, j + 1)] == self.EMPTY_SQUARE:
                        num_corners += 1
        return num_corners / self.total_corners

    def get_row_and_column_from_square(self, square):
        return square // self.board_rows, square % self.board_columns

    def get_square_from_row_and_column(self, row, column):
        return row * self.board_columns + column

    def print_board(self):
        for row in range(0, self.board_rows):
            for column in range(0, self.board_columns):
                print(self.board[self.get_square_from_row_and_column(row, column)] + ' ', end='')
            print() # Print new line
