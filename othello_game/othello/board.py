import pygame
from .constants import WHITE, BLACK, GREEN, ROWS, COLS, SQUARE_SIZE, WIDTH, HEIGHT
pygame.init()

font = pygame.font.Font("othello_game/gameFont.ttf", 72)

class Player:
    """
    Represents a player in the Othello game with a name and a color of either black or white
    """
    def __init__(self, name, color):
        self._name = name
        self._color = color

    def get_name(self):
        """Returns player name"""
        return self._name

    def get_color(self):
        """Returns player color"""
        return self._color

class Piece:
    PADDING = 10
    OUTLINE = 2

    def __init__(self, row, col, color):
        self._row = row
        self._col = col
        self._color = color
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self._col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self._row + SQUARE_SIZE // 2

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, self._color, (self.x, self.y), radius + self.OUTLINE)


class Othello:
    """
    Represents the Othello game board as it is being played
    """
    def __init__(self, win):
        self._win = win
        self._player_list = []
        self._board = [['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', 'O', 'X', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', 'X', 'O', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*']]
        
    def print_board(self):
        """Prints the Othello board"""
        for row in self._board:
            print(*row, sep=' ')

    def update_board(self, win):
        row_coord = -1
        col_coord = -1
        for row in self._board:
            row_coord += 1
            for col in row:
                if col_coord >= 9:
                    col_coord = -1
                col_coord += 1
                if col == '*':
                    place_piece = Piece(row_coord, col_coord, 'black')
                    place_piece.draw(win)

                elif col == 'O':
                    place_piece = Piece(row_coord, col_coord, 'white')
                    place_piece.draw(win)
                elif col == 'X':
                    place_piece = Piece(row_coord, col_coord, 'black')
                    place_piece.draw(win)
        pygame.display.update()

    def create_board(self, win):
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(win, BLACK, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE - 5, SQUARE_SIZE - 5))
                pygame.draw.rect(win, GREEN, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE - 5, SQUARE_SIZE - 5))
        for col in range(COLS):
            pygame.draw.rect(win, BLACK, (0 * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(win, BLACK, (9 * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for row in range(ROWS):
            pygame.draw.rect(win, BLACK, (row * SQUARE_SIZE, 0 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(win, BLACK, (row * SQUARE_SIZE, 9 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def get_player_name(self, color):
        """Given a color, returns the player name associated with it"""
        for player in self._player_list:
            if color == player.get_color():
                name = player.get_name()
                return name

    def create_player(self, name, color):
        """Creates a player object from the Player class with a name and a color piece of either white or black
        and adds them to player_list"""
        if color == 'white':
            white = Player(name, color)
            self._player_list.append(white)
            p1 = Piece()
        else:
            black = Player(name, color)
            self._player_list.append(black)

    def return_winner(self, win):
        """Returns a printed string with the winner of the game and their name, or if there
        equal black and white pieces, returns 'It's a tie'"""
        black_pieces = self.count_pieces('black')
        white_pieces = self.count_pieces('white')
        if black_pieces > white_pieces:                 # Black won
            winner = 'black'
        elif black_pieces < white_pieces:
            winner = 'white'
        else:
            winner = 'tie'
        text = font.render('GAME OVER', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2)
        win.fill(GREEN)
        win.blit(text, textRect)

    def return_available_positions(self, color):
        """Given the color of the player's pieces, returns a list of available positions
        for the player to place their piece on the current board"""
        board = self._board
        available_positions = []
        row = -1
        col = -1
        for row_line in board:
            col = -1
            row += 1
            for col_line in row_line:
                col += 1
                if color == 'black' and col_line == 'X':
                    directions = {'up': (row - 1, col), 'down': (row + 1, col), 'left': (row, col - 1),
                                  'right': (row, col + 1), 'up left':(row - 1, col - 1), 'up right':
                                  (row - 1, col + 1), 'down left': (row + 1, col - 1), 'down right': (row + 1, col + 1)}
                    for direction in directions:
                        piece_position = directions[direction]
                        potential = self.check_move(color, piece_position, direction)
                        if potential is not False:
                            if potential not in available_positions:
                                available_positions.append(potential)
                if color == 'white' and col_line == 'O':
                    directions = {'up': (row - 1, col), 'down': (row + 1, col), 'left': (row, col - 1),
                                  'right': (row, col + 1), 'up left':(row - 1, col - 1), 'up right':
                                  (row - 1, col + 1), 'down left': (row + 1, col - 1), 'down right': (row + 1, col + 1)}
                    for direction in directions:
                        piece_position = directions[direction]
                        potential = self.check_move(color, piece_position, direction)
                        if potential is not False:
                            if potential not in available_positions:
                                available_positions.append(potential)
        available_positions.sort()
        return available_positions

    def make_move(self, color, piece_position, count=0):
        """Given the color of the player's piece and a position on the board, the function
        places the piece at the position and calls check_flip to see if we can flip in that direction, and if
         so, calls flip_pieces to update the board. Function is called by play_game() only if the move is allowed"""
        row, col = piece_position
        board = self._board
        if count == 0:
            if color == 'black':
                board[row][col] = 'X'
            else:
                board[row][col] = 'O'
        count = 1
        if board[row][col] == '.':
            return False
        if board[row][col] == '*':  # If we have hit the border
            return False
        if color == 'black':
            directions = {'up': (row - 1, col), 'down': (row + 1, col), 'left': (row, col - 1),
                          'right': (row, col + 1), 'up left': (row - 1, col - 1), 'up right':
                              (row - 1, col + 1), 'down left': (row + 1, col - 1), 'down right': (row + 1, col + 1)}
            for direction in directions:
                piece_position = directions[direction]
                potential = self.check_flip(color, piece_position, direction)
                if potential is not False:
                    self.flip_pieces(color, piece_position, direction)
        if color == 'white':
            directions = {'up': (row - 1, col), 'down': (row + 1, col), 'left': (row, col - 1),
                          'right': (row, col + 1), 'up left': (row - 1, col - 1), 'up right':
                              (row - 1, col + 1), 'down left': (row + 1, col - 1), 'down right': (row + 1, col + 1)}
            for direction in directions:
                piece_position = directions[direction]
                potential = self.check_flip(color, piece_position, direction)
                if potential is not False:
                    self.flip_pieces(color, piece_position, direction)
        return self._board

    def check_flip(self, color, piece_position, direction, count=0):
        """Called by make_move to check the direction in which to flip the pieces. Takes a direction as a parameter
        and returns True if the pieces in that direction from the piece_position can be flipped, otherwise False."""
        board = self._board
        row, col = piece_position
        if board[row][col] == '.':
            return False
        if board[row][col] == '*':
            return False
        directions = {'up': (row - 1, col), 'down': (row + 1, col), 'left': (row, col - 1),
                      'right': (row, col + 1), 'up left': (row - 1, col - 1), 'up right':
                          (row - 1, col + 1), 'down left': (row + 1, col - 1), 'down right': (row + 1, col + 1)}
        if color == 'black':
            if count == 0:
                if board[row][col] == 'X':          # If it's not adjacent to a white piece
                    return False
                count = 1
            if board[row][col] == 'X':
                return True
            piece_position = directions[direction]
            return self.check_flip(color, directions[direction], direction, count)
        if color == 'white':
            if count == 0:
                if board[row][col] == 'O':          # If it's not adjacent to a black piece
                    return False
                count = 1
            if board[row][col] == 'O':
                return True
            piece_position = directions[direction]
            return self.check_flip(color, directions[direction], direction, count)

    def flip_pieces(self, color, piece_position, direction):
        """Given a color and a piece position, the function flips the piece to the specified color. Called
        by make_move if the direction to flip the pieces is valid."""
        board = self._board
        row, col = piece_position
        directions = {'up': (row - 1, col), 'down': (row + 1, col), 'left': (row, col - 1),
                      'right': (row, col + 1), 'up left': (row - 1, col - 1), 'up right':
                          (row - 1, col + 1), 'down left': (row + 1, col - 1), 'down right': (row + 1, col + 1)}
        if color == 'black':
            if board[row][col] != 'O':
                return
            else:
                board[row][col] = 'X'
        if color == 'white':
            if board[row][col] != 'X':
                return
            else:
                board[row][col] = 'O'
        self.flip_pieces(color, directions[direction], direction)
        self._board = board
        

    def check_move(self, color, piece_position, direction, count=0):
        """Given a color, row, col, direction, and count of 0, the function will
        recursively call itself to move in the specified direction to see if the move
        is valid. If the position is adjacent to a piece of the opposite color and there
        is a piece of the same color at the end of the line, the function returns True.
        Otherwise, false."""
        row, col = piece_position
        board = self._board
        if count == 0:
            if board[row][col] == '.':
                return False
        count += 1
        if board[row][col] == '.':
            return piece_position
        if board[row][col] == '*':
            return False
        if color == 'black':
            if board[row][col] == 'X':
                return False
            directions = {'up': (row - 1, col), 'down': (row + 1, col), 'left': (row, col - 1),
                          'right': (row, col + 1), 'up left': (row - 1, col - 1), 'up right':
                              (row - 1, col + 1), 'down left': (row + 1, col - 1), 'down right': (row + 1, col + 1)}
            piece_position = directions[direction]
            return self.check_move(color, piece_position, direction, count)
        if color == 'white':
            if board[row][col] == 'O':
                return False
            directions = {'up': (row - 1, col), 'down': (row + 1, col), 'left': (row, col - 1),
                          'right': (row, col + 1), 'up left': (row - 1, col - 1), 'up right':
                              (row - 1, col + 1), 'down left': (row + 1, col - 1), 'down right': (row + 1, col + 1)}
            piece_position = directions[direction]
            return self.check_move(color, piece_position, direction, count)

    def count_pieces(self, color):
        """Counts and returns the number of pieces of the specified color on the board"""
        board = self._board
        black_pieces = 0
        white_pieces = 0
        for row in board:
            for col in row:
                if col == 'X':
                    black_pieces += 1
                if col == 'O':
                    white_pieces += 1
        if color == 'black':
            return black_pieces
        else:
            return white_pieces

    def play_game(self, color, piece_position, win):
        """Given a piece color and position, the function checks if the position is valid via
        the available_positions method. If it is valid, the move is made. Otherwise, returns an
        invalid moves message. If there are no valid positions, the function checks if
        the game is over. If so, it prints a message and calls return_winner."""
        board = self._board
        row, col = piece_position
        available_positions = self.return_available_positions(color)
        if piece_position not in available_positions:
            print("Invalid move. Here are the valid moves:" + str(available_positions))
            return False
        self.make_move(color, piece_position)
        available_positions = self.return_available_positions(color)
        if not available_positions:
            white_pieces = str(self.count_pieces('white'))
            black_piece = str(self.count_pieces('black'))
            if color == 'black':
                if not self.return_available_positions('white'):    # Game is over
                    print("Game is ended white piece: " + white_pieces + "black piece: " + black_piece)
                    self.return_winner(win)
            if color == 'white':
                if not self.return_available_positions('black'):    # Game is over
                    print("Game is ended white piece: " + white_pieces + "black piece: " + black_piece)
                    self.return_winner(win)