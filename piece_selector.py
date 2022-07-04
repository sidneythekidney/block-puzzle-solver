import piece
import random
from datetime import datetime
random.seed(datetime.now())

# Construct all pieces for the puzzle

# 1.  1 x 1
piece1x1 = piece.Piece([[0, 0]], 1, 1)

# 2. 1 x 2
piece1x2 = piece.Piece([[0, 0], [0, 1]], 1, 2)

# 3. 2 x 1
piece2x1 = piece.Piece([[0, 0], [1, 0]], 2, 1)

# 4. 2 x 2
piece2x2 = piece.Piece([[0, 0], [0, 1], [1, 0], [1, 1]], 2, 2)

# 5. 1 x 3
piece1x3 = piece.Piece([[0, 0], [0, 1], [0, 2]], 1, 3)

# 6. 3 x 1
piece3x1 = piece.Piece([[0, 0], [1, 0], [2, 0]], 3, 1)

# 7. 3 x 3
piece3x3 = piece.Piece([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]], 3, 3)

# 8. 1 x 4
piece1x4 = piece.Piece([[0, 0], [0, 1], [0, 2], [0, 3]], 1, 4)

# 9. 4 x 1
piece4x1 = piece.Piece([[0, 0], [1, 0], [2, 0], [3, 0]], 4, 1)

# 10. 1 x 5
piece1x5 = piece.Piece([[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]], 1, 5)

# 11. 5 x 1
piece5x1 = piece.Piece([[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]], 5, 1)

# 12. small l top left corner
piece_small_l_top_left_corner = piece.Piece([[0, 0], [0, 1], [1, 0]], 2, 2)

# 13. small l top right corner
piece_small_l_top_right_corner = piece.Piece([[0, 0], [0, 1], [1, 1]], 2, 2)

# 14. small l bottom left corner
piece_small_l_bottom_left_corner = piece.Piece([[0, 0], [1, 0], [1, 1]], 2, 2)

# 15. small l bottom left corner
piece_small_l_bottom_right_corner = piece.Piece([[0, 1], [1, 0], [1, 1]], 2, 2)

# 16. big l top left corner
piece_big_l_top_left_corner = piece.Piece([[0, 0], [0, 1], [0, 2], [1, 0], [2, 0]], 3, 3)

# 17. big l top right corner
piece_big_l_top_right_corner = piece.Piece([[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]], 3, 3)

# 18. big l bottom left corner
piece_big_l_bottom_left_corner = piece.Piece([[0, 0], [2, 1], [2, 2], [1, 0], [2, 0]], 3, 3)

# 19. big l bottom right corner
piece_big_l_bottom_right_corner = piece.Piece([[2, 0], [2, 1], [2, 2], [1, 2], [0, 2]], 3, 3)

class PieceSelector():
    def __init__(self):
        self.pieces = [
            piece1x1,
            piece1x2,
            piece2x1,
            piece2x2,
            piece1x3,
            piece3x1,
            piece3x3,
            piece1x4,
            piece4x1,
            piece1x5,
            piece5x1,
            piece_small_l_top_left_corner,
            piece_small_l_top_right_corner,
            piece_small_l_bottom_left_corner,
            piece_small_l_bottom_right_corner,
            piece_big_l_top_left_corner,
            piece_big_l_top_right_corner,
            piece_big_l_bottom_left_corner,
            piece_big_l_bottom_right_corner
        ]
    
    def get_random_pieces(self, number_of_random_pieces):
        selected_pieces = []
        for i in range(number_of_random_pieces):
            selected_pieces.append(self.pieces[random.randint(0, len(self.pieces) - 1) % len(self.pieces)])
        return selected_pieces