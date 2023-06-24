import pygame
from othello.constants import WIDTH, HEIGHT, SQUARE_SIZE, GREEN
from othello.board import Othello, Piece
pygame.init()

FPS = 60

font = pygame.font.Font("othello_game/gameFont.ttf", 72)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Othello')

def get_row_col(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return (row, col)


text = font.render('GAME OVER', True, (255, 255, 255))
textRect = text.get_rect()
textRect.center = (WIDTH // 2, HEIGHT // 2)


def main():
    run = True
    clock = pygame.time.Clock()
    board = Othello(WIN)
    bp1 = Piece(4, 5, (0, 0, 0))
    bp2 = Piece(5, 4, (0, 0, 0))
    wp1 = Piece(4, 4, (255, 255, 255))
    wp2 = Piece(5, 5, (255, 255, 255))
    player = True       # black piece starts

    while run:
        clock.tick(FPS)

        board.create_board(WIN)
        wp1.draw(WIN)
        wp2.draw(WIN)
        bp1.draw(WIN)
        bp2.draw(WIN)
        
        if board.return_available_positions is None:
            WIN.fill(GREEN)
            WIN.blit(text, textRect)
            board.update_board(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                rowCol = get_row_col(pos)
                if player is True:
                    play = board.play_game('black', rowCol, WIN)
                    if play is not False:
                        player = False
                else:
                    play = board.play_game('white', rowCol, WIN)
                    if play is not False:
                        player = True
            
            board.update_board(WIN)
            
    pygame.quit()

main()
