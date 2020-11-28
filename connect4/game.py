import copy


def columns(board):
    return len(board[0])

def rows(board):
    return len(board)   

def moves_available(board) -> list:
    return [c for c in range(columns(board)) if board[0][c] == '-']

def play(board, player:str, column:int):
        
    column_values = [row[column] for row in board]
    row = max([i for i,v in enumerate(column_values) if v=='-']) # the row to which the chip will fall
    new_board = copy.deepcopy(board)
    new_board[row][column] = player
    return new_board


def fourInARow(row, col, board):
    '''
    '''
    if board[row][col] == '-':
        return None
    
    # vertical down: 
    if row < len(board)-3:
        if (board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col]):
            return board[row][col]
    
    # horizontal right:
    if col < len(board[0])-3:
        if (board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3]):
            return board[row][col]

    # right diag: 
    if (row < len(board)-3) & (col < len(board[0])-3):
        if (board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]):
            return board[row][col]

    # left diag: 
    if (row < len(board)-3) & (col > 2):
        if (board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3]):
            return board[row][col]
    return None


def checkWin(board):
    '''
    '''
    for row in range(rows(board)):
        for col in range(columns(board)):
            check_win = fourInARow(row, col, board)
            if check_win: 
                return check_win

    return None


def board2string(board):
    board_string = []
    for row in board:
        board_string.append(''.join([c for c in row]))
    return '\n'.join(board_string)

def string2board(board_string):
    board = []
    for row in board_string.split('\n'):
        board.append([c for c in row])
    return board

