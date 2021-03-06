from random import random
import pygame
import board
import piece_selector
import time
import itertools

# Define global colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
WOOD_COLOR_LIGHT = (252, 235, 197)
WOOD_COLOR_DARK = (129, 84, 56)
WOOD_COLOR_LIGHT_HIGHLIGHTED = (202, 185, 147)
WOOD_COLOR_DARK_HIGHLIGHTED = (179, 134, 106)
YELLOW_HIGHLIGHT = (255, 255, 0)

display_width = 1000
display_height = 700
board_rows = 10
board_columns = 10
score_panel_width = 200
piece_bar_height = 200
piece_bar_width = display_width - score_panel_width
game_board_width = display_width - score_panel_width
game_board_height = display_height - piece_bar_height
num_random_pieces = 3
random_piece_space = 10
random_piece_width = (piece_bar_width - random_piece_space * (num_random_pieces + 1)) // num_random_pieces
random_piece_height = piece_bar_height - 2 * random_piece_space
random_piece_tile_space =  2
max_random_piece_tiles = 5
random_piece_tile_side_length = (min(random_piece_width, random_piece_height) - (max_random_piece_tiles + 1) * random_piece_tile_space) // max_random_piece_tiles
random_piece_tile_width = random_piece_tile_side_length
random_piece_tile_height = random_piece_tile_side_length

quit_button_width = 150
quit_button_height = 50
tile_spacing = 1
tile_edge = 2

num_random_pieces = 3

def gen_perms(perm_length):
    perm_list = []
    for i in range(perm_length):
        perm_list.append(i)
    return list(itertools.permutations(perm_list))

class Game():
    def __init__(self, display_width, display_height, board_rows, board_columns, starting_board):
        self.display_width = display_width
        self.display_height = display_height
        self.board_rows = board_rows
        self.board_columns = board_columns

        self.tile_height = (game_board_height - (self.board_rows + 1) * tile_spacing) // self.board_rows
        self.tile_width = self.tile_height

        self.game_score = 0

        self.game_board = board.Board(starting_board, board_rows, board_columns)
        self.piece_selector = piece_selector.PieceSelector()
        self.tile_centers = []

        # Accepts a list of randomly selected pieces and returns the optimal piece placements
        self.perms = gen_perms(num_random_pieces)

    def play_game(self):
        pygame.init()

        self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Block Puzzle Solver")
        pygame.display.flip()

        while True:
            self.display_introduction()
            self.main_game()

    def display_introduction(self):
        self.game_display.fill(WOOD_COLOR_LIGHT)
        self.write_text("Welcome to the Block Puzzle AI", 30, WOOD_COLOR_DARK, (self.display_width // 2, self.display_height // 5))

        get_started_rectangle_width = 200
        get_started_rectangle_height = 50

        get_started_rectangle = self.draw_rectangle(get_started_rectangle_width, 
            get_started_rectangle_height, 
            (self.display_width // 2, self.display_height // 2), 
            WOOD_COLOR_DARK, 
            border_radius=5)
        
        self.write_text("Get Started", 20, WOOD_COLOR_LIGHT, (self.display_width // 2, self.display_height // 2))

        game_selected = False
        while not game_selected:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    if get_started_rectangle.collidepoint(event.pos):
                        get_started_rectangle = self.draw_rectangle(get_started_rectangle_width, 
                            get_started_rectangle_height, 
                            (self.display_width // 2, 
                            self.display_height // 2), 
                            WOOD_COLOR_DARK_HIGHLIGHTED, 
                            border_radius=5)
                        
                        self.write_text("Get Started", 20, WOOD_COLOR_LIGHT_HIGHLIGHTED, (self.display_width // 2, self.display_height // 2))
                    else:
                        get_started_rectangle = self.draw_rectangle(get_started_rectangle_width,
                            get_started_rectangle_height,
                            (self.display_width // 2, self.display_height // 2),
                            WOOD_COLOR_DARK,
                            border_radius=5)
                        
                        self.write_text("Get Started", 20, WOOD_COLOR_LIGHT, (self.display_width // 2, self.display_height // 2))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if get_started_rectangle.collidepoint(event.pos):
                        game_selected = True
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.display.update()

    def main_game(self):
    
        # Display main game elements
        self.display_game_space()

        # Display quit button
        quit_button_rectangle = self.draw_rectangle(
            quit_button_width, 
            quit_button_height, 
            (display_width - score_panel_width // 2, display_height - 100), 
            WOOD_COLOR_DARK, 
            border_radius=5)
        self.write_text("Main Menu", 25, WOOD_COLOR_LIGHT, (display_width - score_panel_width // 2, display_height - 100))

        game_over = False
        while not game_over:
            # Get and display random pieces
            random_selected_pieces = self.piece_selector.get_random_pieces(num_random_pieces)
            self.display_random_pieces(random_selected_pieces)
            pygame.display.update()

            self.get_cpu_move_and_update_board(random_selected_pieces)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button_rectangle.collidepoint(event.pos):
                        return
                elif event.type == pygame.MOUSEMOTION:
                    if quit_button_rectangle.collidepoint(event.pos):
                        # Update quit button color
                        quit_button_rectangle = self.draw_rectangle(
                            quit_button_width, 
                            quit_button_height, 
                            (display_width - score_panel_width // 2, display_height - 100), 
                            WOOD_COLOR_DARK_HIGHLIGHTED, 
                            border_radius=5)
                        self.write_text("Main Menu", 25, WOOD_COLOR_LIGHT_HIGHLIGHTED, (display_width - score_panel_width // 2, display_height - 100))
                    else:
                        quit_button_rectangle = self.draw_rectangle(
                            quit_button_width, 
                            quit_button_height,
                            (display_width - score_panel_width // 2, display_height - 100), 
                            WOOD_COLOR_DARK, 
                            border_radius=5)
                        self.write_text("Main Menu", 25, WOOD_COLOR_LIGHT, (display_width - score_panel_width // 2, display_height - 100))
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.display.update()

    def get_cpu_move_and_update_board(self, random_selected_pieces):
        for _ in range(num_random_pieces):
            move_selected = False
            while not move_selected:
                # Get random piece selection from user
                move_random_piece = input("Select which piece to move (l, c, r): ")
                random_piece_num = -1
                if (move_random_piece == "l"):
                    random_piece_num = 0
                elif (move_random_piece == "c"):
                    random_piece_num = 1
                else:
                    random_piece_num = 2

                print("piece squares: ")
                print(random_selected_pieces[random_piece_num].piece_squares)

                # Get row and column from the user
                row = int(input("Enter row number between 0 and " + str(board_rows-1) + " inclusive: "))
                column = int(input("Enter column number between 0 and " + str(board_columns-1) + " inclusive: "))

                # Display random piece to board
                if self.game_board.can_place_piece(random_selected_pieces[random_piece_num], self.game_board.get_square_from_row_and_column(row ,column)):
                    deleted_rows, deleted_columns = self.game_board.place_piece(random_selected_pieces[random_piece_num], 
                        self.game_board.get_square_from_row_and_column(row, column))
                    
                    # Highlight moved piece squares
                    self.place_block_animation(row, column, random_selected_pieces[random_piece_num])

                    # Cover up placed piece
                    placed_piece_left =  random_piece_num * random_piece_width + (random_piece_num + 1) * random_piece_space + random_piece_width // 2
                    placed_piece_top = self.display_height - piece_bar_height // 2
                    display_individual_piece_rectangle = self.draw_rectangle(
                        random_piece_width - 2,
                        random_piece_height - 2,
                        (placed_piece_left, placed_piece_top),
                        WOOD_COLOR_DARK_HIGHLIGHTED,
                        border_radius=5
                    )
                    pygame.display.update()

                    # Highlight the rows and columns to delete
                    if len(deleted_rows) + len(deleted_columns) > 0:
                        self.delete_rows_and_columns_animation(deleted_rows, deleted_columns)

                    # Update the game score
                    self.update_score(len(random_selected_pieces[random_piece_num].piece_squares), len(deleted_rows), len(deleted_columns))

                    move_selected = True
                else:
                    print("Error cannot place piece here! Try Again....")

    def determine_optimal_piece_placement(self, random_selected_pieces):
        # Want to minimize cost to find the bets placement
        min_cost = float('inf')

        for perm in self.perms:
            for piece_idx, piece in enumerate(perm):
                for i in range(self.board_rows):
                    for j in range(self.columns):
                        # Attempt to place piece
                        if self.game_board.can_place_piece(random_selected_pieces[piece], self.game_board.get_square_from_row_and_column(i, j)):
                            # Update board as necessary
                            deleted_rows, deleted_columns = self.game_board.place_piece(
                                random_selected_pieces[piece], self.game_board.get_square_from_row_and_column(i, j))
                            
                            self.game_board.delete_rows_and_columns(deleted_rows, deleted_columns)

                            # If this is the last piece to place update the bets move as necessary
                            if piece_idx == self.num_random_pieces - 1:
                                board_score = self.game_board.calculate_board_score()
                                if (board_score < min_cost):
                                    min_cost = board_score


    def display_game_space(self):
        # Display the game board and score
        game_board_rectangle = self.draw_rectangle(
            game_board_width, 
            game_board_height, 
            (game_board_width // 2, game_board_height // 2), 
            WOOD_COLOR_DARK, 
            border_radius=5)

        self.write_text("Score", 25, WOOD_COLOR_DARK, (display_width - score_panel_width // 2, self.display_height // 4))
        self.write_text(str(self.game_score), 25, WOOD_COLOR_DARK, (display_width - score_panel_width // 2, self.display_height // 3))

        piece_display_rectangle = self.draw_rectangle(
            piece_bar_width,
            piece_bar_height,
            (piece_bar_width // 2, self.display_height - piece_bar_height // 2),
            WOOD_COLOR_DARK_HIGHLIGHTED,
            border_radius=5
        )

        # Draw squares to display random pieces
        for i in range(num_random_pieces):
            left =  i * random_piece_width + (i + 1) * random_piece_space + random_piece_width // 2
            top = self.display_height - piece_bar_height // 2
            _ = self.draw_rectangle(
                random_piece_width,
                random_piece_height,
                (left, top),
                BLACK,
                edge_width=1,
                border_radius=5
            )

        self.display_all_tiles()
        self.display_occupied_tiles()

    def update_score(self, piece_size, num_rows_deleted, num_columns_deleted):
        # Update game score based on parameters
        self.game_score += piece_size + self.board_columns * num_rows_deleted + self.board_rows * num_columns_deleted

        self.draw_rectangle(
            display_width - game_board_width,
            30,
            (display_width - score_panel_width // 2, self.display_height // 3),
            WOOD_COLOR_LIGHT,
        )


        # Display the updated score
        self.write_text(str(self.game_score), 25, WOOD_COLOR_DARK, (display_width - score_panel_width // 2, self.display_height // 3))
        pygame.display.update()

    def display_all_tiles(self):
        # Calculate offset for tiles
        tile_left_offset = (game_board_width - self.tile_width * self.board_columns - tile_spacing * (self.board_columns - 1)) // 2
        for row in range(0, self.board_rows):
            for column in range(0, self.board_columns):
                # Calculate center
                tile_top = (row + 1) * tile_spacing + row * self.tile_height + self.tile_height // 2
                tile_left = tile_left_offset + (column + 1) * tile_spacing + column * self.tile_width + self.tile_width // 2
                tile = self.draw_rectangle(self.tile_width, self.tile_height, (tile_left, tile_top), BLACK, edge_width=tile_edge, border_radius=5)
                # Add to tile centers
                self.tile_centers.append((tile_left, tile_top))

    def display_occupied_tiles(self):
        # tile_width = (game_board_width - (self.board_columns + 1) * tile_spacing) // self.board_columns
        for row in range(0, self.board_rows):
            for column in range(0, self.board_columns):
                # Calculate center
                if (self.game_board.board[self.game_board.get_square_from_row_and_column(row, column)] == self.game_board.OCCUPIED_SQUARE):
                    tile_center = self.tile_centers[self.game_board.get_square_from_row_and_column(row, column)]
                    _ = self.draw_rectangle(self.tile_width - 2 * tile_edge, self.tile_height - 2 * tile_edge, tile_center, WOOD_COLOR_LIGHT, border_radius=5)

    def display_random_pieces(self, random_pieces):
        for i, piece in enumerate(random_pieces):
            # Determine absolute center of random shape
            absolute_center_left = (i + 1) * random_piece_space + i * random_piece_width + random_piece_width // 2
            absolute_center_top = self.display_height - piece_bar_height // 2

            for square in piece.piece_squares:
                # Determine center for left of square
                square_center_left = -1
                square_center_top = -1
                if piece.max_columns % 2:
                    # Odd number of columns
                    square_center_left = absolute_center_left + (random_piece_tile_width + random_piece_tile_space) * (square[1] - piece.max_columns // 2)
                else:
                    # Even number of columns
                    middle_column = piece.max_columns // 2 - 0.5
                    square_center_left = absolute_center_left + (square[1] - middle_column) * (random_piece_tile_width + random_piece_tile_space)

                # Determine center for top of square
                if piece.max_rows % 2:
                    # Odd number of rows
                    square_center_top = absolute_center_top + (random_piece_tile_height + random_piece_tile_space) * (square[0] - piece.max_rows // 2)
                else:
                    # Even number of rows
                    middle_row = piece.max_rows // 2 - 0.5
                    square_center_top = absolute_center_top + (square[0] - middle_row) * (random_piece_tile_height + random_piece_tile_space)

                # Draw the square given this center location
                self.draw_rectangle(
                    random_piece_tile_width,
                    random_piece_tile_height,
                    (square_center_left, square_center_top),
                    WOOD_COLOR_LIGHT,
                    border_radius=5
                )

    def place_block_animation(self, row, column, piece):
        # Get centers for relevant piece
        piece_square_centers = []
        for square in piece.piece_squares:
            piece_square_centers.append(self.tile_centers[self.game_board.get_square_from_row_and_column(row + square[0], column + square[1])])

        # Add hightlighted blocks to game surface
        for center in piece_square_centers:
            _ = self.draw_rectangle(self.tile_width - 2 * tile_edge, self.tile_height - 2 * tile_edge, center, YELLOW_HIGHLIGHT, border_radius=5)
        
        pygame.event.pump()
        pygame.display.update()
        pygame.time.delay(1000)

        # Add piece blocks to the surface
        for center in piece_square_centers:
            _ = self.draw_rectangle(self.tile_width - 2 * tile_edge, self.tile_height - 2 * tile_edge, center, WOOD_COLOR_LIGHT, border_radius=5)

        pygame.event.pump()
        pygame.display.update()

    def delete_rows_and_columns_animation(self, deleted_rows, deleted_columns):
        piece_square_centers = []
        # Get the centers of all rows to delete
        for deleted_row in deleted_rows:
            for column in range(self.board_columns):
                piece_square_centers.append(self.tile_centers[self.game_board.get_square_from_row_and_column(deleted_row, column)])
        for deleted_column in deleted_columns:
            for row in range(self.board_rows):
                piece_square_centers.append(self.tile_centers[self.game_board.get_square_from_row_and_column(row, deleted_column)])

        # Highlight all deleted squares
        for center in piece_square_centers:
            _ = self.draw_rectangle(self.tile_width - 2 * tile_edge, self.tile_height - 2 * tile_edge, center, GREEN, border_radius=5)
        
        pygame.event.pump()
        pygame.display.update()
        pygame.time.delay(1000)

        # Show empty blocks fro deleted rows and columns
        for center in piece_square_centers:
            _ = self.draw_rectangle(self.tile_width - 2 * tile_edge, self.tile_height - 2 * tile_edge, center, WOOD_COLOR_DARK, border_radius=5)

        pygame.event.pump()
        pygame.display.update()

    def write_text(self, text, size, color, center_pos):
        font = pygame.font.Font('freesansbold.ttf', size)
        text = font.render(text, True, color)
        textRect = text.get_rect()
        textRect.center = center_pos
        self.game_display.blit(text, textRect)

    def draw_rectangle(self, width, height, center, color, edge_width=0, border_radius=0):
        rectangle = pygame.Rect(0, 0, width, height)
        rectangle.center = center
        pygame.draw.rect(self.game_display, color, rectangle, edge_width, border_radius)
        return rectangle

start_board = [
    '*', '*', '.', '.', '.', '.', '.', '.', '.', '.',
    '*', '*', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
]

test_start_board = [
    '.', '.', '*', '*', '*', '*', '*', '*', '*', '*',
    '.', '.', '*', '*', '*', '*', '*', '*', '*', '*',
    '*', '*', '.', '.', '.', '.', '.', '.', '.', '.',
    '*', '*', '.', '.', '.', '.', '.', '.', '.', '.',
    '*', '*', '.', '.', '.', '.', '.', '.', '.', '.',
    '*', '*', '.', '.', '.', '.', '.', '.', '.', '.',
    '*', '*', '.', '.', '.', '.', '.', '.', '.', '.',
    '*', '*', '.', '.', '.', '.', '.', '.', '.', '.',
    '*', '*', '.', '.', '.', '.', '.', '.', '.', '.',
    '*', '*', '.', '.', '.', '.', '.', '.', '.', '.',
]

game = Game(display_width, display_height, board_rows, board_columns, test_start_board)
game.play_game()