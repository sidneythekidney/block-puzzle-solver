class Piece:
    def __init__(self, piece_squares, max_rows, max_columns):
        self.piece_squares = piece_squares # List of [row, column] where row and column are offsets from top left piece square
        self.max_rows = max_rows
        self.max_columns = max_columns

    def print_piece(self):
        piece_grid = []
        for i in range(self.max_rows):
            row = []
            for j in range(self.max_columns):
                row.append(' ')
            piece_grid.append(row)
        
        for piece_square in self.piece_squares:
            [row, column] = piece_square
            piece_grid[row][column] = '\u2584'
        for i in range(self.max_rows):
            for j in range(self.max_columns):
                print(piece_grid[i][j] + ' ', end='')
            print()
        print()