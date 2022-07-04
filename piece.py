class Piece:
    def __init__(self, piece_squares, max_rows, max_columns) -> None:
        self.piece_squares = piece_squares # List of [row, column] where row and column are offsets from top left piece square
        self.max_rows = max_rows
        self.max_columns = max_columns
