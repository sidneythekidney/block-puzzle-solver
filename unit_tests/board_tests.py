import sys
sys.path.insert(0, '../')
import board
import piece
import unittest

# Initialize needed variables
board_rows = 10
board_columns = 10
empty_start_board = [
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
]

occupied_start_board = [
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '*', '*', '.', '.', '.', '.', '.', '.', '.',
    '.', '*', '*', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
]

delete_and_restore_rows_and_columns_start_board = [
    '.', '*', '*', '.', '.', '.', '.', '.', '.', '.',
    '*', '.', '.', '*', '*', '*', '*', '*', '*', '*',
    '*', '.', '.', '*', '*', '*', '*', '*', '*', '*',
    '.', '*', '*', '.', '.', '.', '.', '.', '.', '.',
    '.', '*', '*', '.', '.', '.', '.', '.', '.', '.',
    '.', '*', '*', '.', '.', '.', '.', '.', '.', '.',
    '.', '*', '*', '.', '.', '.', '.', '.', '.', '.',
    '.', '*', '*', '.', '.', '.', '.', '.', '.', '.',
    '.', '*', '*', '.', '.', '.', '.', '.', '.', '.',
    '.', '*', '*', '.', '.', '.', '.', '.', '.', '.',
]

empty_board = board.Board(empty_start_board, board_rows, board_columns)
occupied_board = board.Board(occupied_start_board, board_rows, board_columns)
delete_and_restore_rows_and_columns_board = board.Board(delete_and_restore_rows_and_columns_start_board, board_rows, board_columns)

# Create a 2x2 piece to place
piece2x2 = piece.Piece([[0,0],[1,0],[0,1],[1,1]], 2, 2)

# Create 1x1 piece to place
piece1x1 = piece.Piece([[0,0]], 1, 1)

class BoardUnitTests(unittest.TestCase):

    def test_get_row_and_column_from_square(self):
        self.assertEqual(empty_board.get_row_and_column_from_square(0), (0, 0), "Invalid row and column obtained from square!")
        self.assertEqual(empty_board.get_row_and_column_from_square(1), (0, 1), "Invalid row and column obtained from square!")
        self.assertEqual(empty_board.get_row_and_column_from_square(10), (1, 0), "Invalid row and column obtained from square!")
        self.assertEqual(empty_board.get_row_and_column_from_square(11), (1, 1), "Invalid row and column obtained from square!")
        self.assertEqual(empty_board.get_row_and_column_from_square(99), (9, 9), "Invalid row and column obtained from square!")

    def test_get_square_from_row_and_column(self):
        self.assertEqual(empty_board.get_square_from_row_and_column(0, 0), 0, "Invalid square obtained from row and column!")
        self.assertEqual(empty_board.get_square_from_row_and_column(0, 1), 1, "Invalid square obtained from row and column!")
        self.assertEqual(empty_board.get_square_from_row_and_column(1, 0), 10, "Invalid square obtained from row and column!")
        self.assertEqual(empty_board.get_square_from_row_and_column(1, 1), 11, "Invalid square obtained from row and column!")
        self.assertEqual(empty_board.get_square_from_row_and_column(9, 9), 99, "Invalid square obtained from row and column!")

    def test_can_place_piece(self):
        
        self.assertTrue(empty_board.can_place_piece(piece1x1, 0))
        self.assertTrue(empty_board.can_place_piece(piece1x1, 9))
        self.assertTrue(empty_board.can_place_piece(piece1x1, 10))
        self.assertTrue(empty_board.can_place_piece(piece1x1, 99))
        
        self.assertFalse(occupied_board.can_place_piece(piece1x1, 11))

        # Can't place piece out of bounds
        self.assertTrue(empty_board.can_place_piece(piece2x2, 0))
        self.assertFalse(empty_board.can_place_piece(piece2x2, 9))
        self.assertTrue(empty_board.can_place_piece(piece2x2, 10))
        self.assertFalse(empty_board.can_place_piece(piece2x2, 99))

        # Can't overwrite occupied squares
        self.assertTrue(occupied_board.can_place_piece(piece2x2, 13))
        self.assertTrue(occupied_board.can_place_piece(piece2x2, 31))
        self.assertFalse(occupied_board.can_place_piece(piece2x2, 0))
        self.assertFalse(occupied_board.can_place_piece(piece2x2, 22))
        self.assertFalse(occupied_board.can_place_piece(piece2x2, 20))

    def test_place_and_unplace_piece(self):
        deleted_rows, deleted_columns = empty_board.place_piece(piece2x2, 11)
        self.assertEqual(empty_board.board, occupied_start_board, "Piece placed incorrectly!!!")

        # Make sure occupied row and column counts are being increased correctly
        self.assertEqual(empty_board.row_occupied_counts[0], 0)
        self.assertEqual(empty_board.row_occupied_counts[1], 2)
        self.assertEqual(empty_board.row_occupied_counts[2], 2)
        self.assertEqual(empty_board.row_occupied_counts[3], 0)

        self.assertEqual(empty_board.column_occupied_counts[0], 0)
        self.assertEqual(empty_board.column_occupied_counts[1], 2)
        self.assertEqual(empty_board.column_occupied_counts[2], 2)
        self.assertEqual(empty_board.column_occupied_counts[3], 0)

        # Reset the board back to original state
        empty_board.unplace_piece(piece2x2, 11, deleted_rows, deleted_columns)
        self.assertEqual(empty_board.row_occupied_counts[0], 0)
        self.assertEqual(empty_board.row_occupied_counts[1], 0)
        self.assertEqual(empty_board.row_occupied_counts[2], 0)
        self.assertEqual(empty_board.row_occupied_counts[3], 0)

        self.assertEqual(empty_board.column_occupied_counts[0], 0)
        self.assertEqual(empty_board.column_occupied_counts[1], 0)
        self.assertEqual(empty_board.column_occupied_counts[2], 0)
        self.assertEqual(empty_board.column_occupied_counts[3], 0)

        self.assertEqual(empty_board.board, empty_start_board, "Piece not unplaced correctly!!!")

    def test_delete_and_restore_rows(self):

        # Make sure row and column counts are correct
        self.assertEqual(delete_and_restore_rows_and_columns_board.row_occupied_counts[0], 2)
        self.assertEqual(delete_and_restore_rows_and_columns_board.row_occupied_counts[1], 8)
        self.assertEqual(delete_and_restore_rows_and_columns_board.row_occupied_counts[2], 8)
        self.assertEqual(delete_and_restore_rows_and_columns_board.row_occupied_counts[3], 2)

        self.assertEqual(delete_and_restore_rows_and_columns_board.column_occupied_counts[0], 2)
        self.assertEqual(delete_and_restore_rows_and_columns_board.column_occupied_counts[1], 8)
        self.assertEqual(delete_and_restore_rows_and_columns_board.column_occupied_counts[2], 8)
        self.assertEqual(delete_and_restore_rows_and_columns_board.column_occupied_counts[3], 2)

        deleted_rows, deleted_columns = delete_and_restore_rows_and_columns_board.place_piece(piece2x2, 11)
        self.assertEqual(delete_and_restore_rows_and_columns_board.board, empty_start_board)

        # Make sure row and column counts are correct
        self.assertEqual(delete_and_restore_rows_and_columns_board.row_occupied_counts[0], 0)
        self.assertEqual(delete_and_restore_rows_and_columns_board.row_occupied_counts[1], 0)
        self.assertEqual(delete_and_restore_rows_and_columns_board.row_occupied_counts[2], 0)
        self.assertEqual(delete_and_restore_rows_and_columns_board.row_occupied_counts[3], 0)

        self.assertEqual(delete_and_restore_rows_and_columns_board.column_occupied_counts[0], 0)
        self.assertEqual(delete_and_restore_rows_and_columns_board.column_occupied_counts[1], 0)
        self.assertEqual(delete_and_restore_rows_and_columns_board.column_occupied_counts[2], 0)
        self.assertEqual(delete_and_restore_rows_and_columns_board.column_occupied_counts[3], 0)

        delete_and_restore_rows_and_columns_board.unplace_piece(piece2x2, 11, deleted_rows, deleted_columns)

        # Make sure row and column counts are correct
        self.assertEqual(delete_and_restore_rows_and_columns_board.row_occupied_counts[0], 2)
        self.assertEqual(delete_and_restore_rows_and_columns_board.row_occupied_counts[1], 8)
        self.assertEqual(delete_and_restore_rows_and_columns_board.row_occupied_counts[2], 8)
        self.assertEqual(delete_and_restore_rows_and_columns_board.row_occupied_counts[3], 2)

        self.assertEqual(delete_and_restore_rows_and_columns_board.column_occupied_counts[0], 2)
        self.assertEqual(delete_and_restore_rows_and_columns_board.column_occupied_counts[1], 8)
        self.assertEqual(delete_and_restore_rows_and_columns_board.column_occupied_counts[2], 8)
        self.assertEqual(delete_and_restore_rows_and_columns_board.column_occupied_counts[3], 2)

        self.assertEqual(delete_and_restore_rows_and_columns_board.board, delete_and_restore_rows_and_columns_start_board)


if __name__ == "__main__":
    unittest.main()
