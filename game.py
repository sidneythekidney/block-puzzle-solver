from logging import exception
from operator import truediv
from random import random
import pygame
import board
import piece_selector
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
        self.perms = []
        for perm in gen_perms(num_random_pieces):
            self.perms.append(list(perm))
        print(self.perms)

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

    def play_game_no_gui(self, num_games):
        for _ in range(num_games):
            game_over = False

            while not game_over:
                random_selected_pieces = self.piece_selector.get_random_pieces(num_random_pieces)
                print("Thinking of best moves...")
                optimal_perm, optimal_piece_placement = self.determine_optimal_piece_placement_helper(random_selected_pieces)
                if optimal_perm != None and optimal_piece_placement != None:
                    print("Best score: " + str(self.min_cost))
                    print("Optimal perm: " + str(optimal_perm))
                    for idx, perm_entry in enumerate(optimal_perm):
                        deleted_rows, deleted_columns = self.game_board.place_piece(random_selected_pieces[perm_entry], optimal_piece_placement[idx])
                        self.update_score_no_gui(len(random_selected_pieces[perm_entry].piece_squares), len(deleted_rows), len(deleted_columns))
                        print("Score: " + str(self.game_score))
                    self.game_board.print_board()
                else:
                    game_over = True

            print("Final score: " + str(self.game_score))

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
            pygame.event.pump()
            random_selected_pieces = self.piece_selector.get_user_pieces()
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
        # Determine optimal piece placements
        optimal_perm, optimal_piece_placement = self.determine_optimal_piece_placement_helper(random_selected_pieces)

        if optimal_perm == None:
            print("Game over!")
            exit()

        print("Determined optimal piece placement, attempting to place pieces...")

        for move_idx in range(len(optimal_perm)):
            # Get random piece selection from user
            random_piece_num = optimal_perm[move_idx]

            # Get square from optimal piece placements
            optimal_placement = optimal_piece_placement[move_idx]
            optimal_row, optimal_column = self.game_board.get_row_and_column_from_square(optimal_placement)

            # Display random piece to board
            if self.game_board.can_place_piece(random_selected_pieces[random_piece_num], optimal_placement):
                deleted_rows, deleted_columns = self.game_board.place_piece(random_selected_pieces[random_piece_num], 
                    optimal_placement)
                
                # Highlight moved piece squares
                self.place_block_animation(optimal_row, optimal_column, random_selected_pieces[random_piece_num])

                # Cover up placed piece
                placed_piece_left =  random_piece_num * random_piece_width + (random_piece_num + 1) * random_piece_space + random_piece_width // 2
                placed_piece_top = self.display_height - piece_bar_height // 2
                _ = self.draw_rectangle(
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
            else:
                print("Error cannot place piece here!")
                exit(1)

    def determine_optimal_piece_placement_helper(self, random_selected_pieces):
        self.min_cost = float('inf')
        self.optimal_perm = None
        self.optimal_piece_placement = None
        for perm in self.perms:
            print("perm: " + str(perm))
            self.determine_optimal_piece_placement(random_selected_pieces, [], perm, perm)

        return self.optimal_perm, self.optimal_piece_placement

    def determine_optimal_piece_placement(self, random_selected_pieces, piece_placements, perm, original_perm):
        if len(perm) == 0:
            # Calculate board score
            board_score = self.game_board.calculate_board_score()
            if board_score < self.min_cost:
                self.min_cost = board_score
                self.optimal_piece_placement = piece_placements
                self.optimal_perm = original_perm
            return

        for i in range(self.game_board.board_rows * self.game_board.board_columns):
            if self.game_board.can_place_piece(random_selected_pieces[perm[0]], i):
                deleted_rows, deleted_columns = self.game_board.place_piece(random_selected_pieces[perm[0]], i)

                self.determine_optimal_piece_placement(random_selected_pieces, piece_placements + [i], perm[1:], original_perm)
                
                self.game_board.unplace_piece(random_selected_pieces[perm[0]], i, deleted_rows, deleted_columns)

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

    def update_score_no_gui(self, piece_size, num_rows_deleted, num_columns_deleted):
        # Update game score based on parameters
        self.game_score += piece_size + self.board_columns * num_rows_deleted + self.board_rows * num_columns_deleted

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

        print("Press space bar to continue with pygame window selected...")
        # Wait until space bar is pressed to let user place piece on app
        spacebar_not_pressed = True
        while spacebar_not_pressed:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        spacebar_not_pressed = False

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
    '.', '*', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '*', '.', '.', '*', '*', '*', '.', '*', '*',
    '*', '*', '*', '.', '.', '*', '*', '.', '*', '*',
    '*', '.', '.', '.', '*', '*', '.', '.', '*', '*',
    '*', '.', '.', '.', '*', '*', '.', '.', '*', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '*', '*', '*', '*', '.', '.', '.', '.', '.', '.',
    '*', '*', '*', '.', '.', '.', '.', '.', '.', '.',
    '.', '*', '.', '.', '.', '.', '.', '.', '.', '.',
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

game = Game(display_width, display_height, board_rows, board_columns, start_board)
game.play_game()
# game.play_game_no_gui(1)