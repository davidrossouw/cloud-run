import copy
import networkx as nx


def columns(board):
    return len(board[0])


def rows(board):
    return len(board)


def moves_available(board) -> list:
    return [c for c in range(columns(board)) if board[0][c] == '-']


def play(board, player: str, column: int):

    column_values = [row[column] for row in board]
    # the row to which the chip will fall
    row = max([i for i, v in enumerate(column_values) if v == '-'])
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


def columns(board):
    return len(board[0])


def rows(board):
    return len(board)


def moves_available(board) -> list:
    return [c for c in range(columns(board)) if board[0][c] == '-']


def play(board, player: str, column: int):
    column_values = [row[column] for row in board]
    # the row to which the chip will fall
    row = max([i for i, v in enumerate(column_values) if v == '-'])
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


def move_preferences(moves_available: list):
    if 3 in moves_available:
        return 3
    elif 2 in moves_available:
        return 2
    elif 4 in moves_available:
        return 4
    elif 1 in moves_available:
        return 1
    elif 5 in moves_available:
        return 5
    elif 0 in moves_available:
        return 0
    elif 6 in moves_available:
        return 6
    else:
        return None


def search(board, max_depth=4):  # -> DiGraph
    """
    Run game simulations from current game state to a maximum number
    of moves ahead (max_depth)
    Return the graph of possible moves and outcomes
    Assume current player is player to be maximized
    """

    depth = 0
    n = 0  # node label which also serves as a node counter
    player = 'R'
    non_player = 'Y'
    G = nx.DiGraph()
    winner = checkWin(board)
    G.add_node(0, winner=winner, board=board, n=n)
    # First branch in look ahead
    child_nodes = []

    for move in moves_available(board):
        # Do move
        new_board = play(board, player=player, column=move)
        winner = checkWin(new_board)
        # Add move node to graph
        n = n+1
        G.add_node(n, winner=winner, board=new_board, n=n)
        G.add_edge(0, n, move=move, player=player)

        if winner:
            ##
            print(f'Winner: {winner}, {n}')
            continue
        child_nodes.append(n)

    depth += 1
    # Subsequent branches
    while depth < max_depth:
        # switch turns
        player, non_player = non_player, player
        child_node_subtree = child_nodes[:]
        child_nodes = []
        for child in child_node_subtree:
            # Get parent state
            parent_board = G.nodes(data=True)[child]['board']
            for move in moves_available(parent_board):
                # Do move
                new_board = play(parent_board, player=player, column=move)
                winner = checkWin(new_board)
                # Add move node to graph
                n = n+1
                G.add_node(n, winner=winner, board=new_board, n=n)
                G.add_edge(child, n, move=move, player=player)
                if winner:
                    continue
                child_nodes.append(n)
        depth = depth+1
    return G


def minimax(G: nx.Graph):
    """
    Perform minimax from node n on a NetworkX graph G.

    Return graph with scores for moves and best move
    """
    maxplayer = True
    minplayer = False

    G = G.copy()
    G.nodes[0].update({'player': 'max'})

    # Recursive tree search
    def _minimax(G, n, player):

        # Base case, winning node found
        if G.out_degree(n) == 0:
            if G.nodes[n]['winner'] == 'R':
                score = 100
            elif G.nodes[n]['winner'] == 'Y':
                score = -100
            else:
                score = 0
            G.nodes[n].update({'score': score})
            return score

        if player == maxplayer:
            bestv = -1
            for child in G.successors(n):
                v = _minimax(G, child, minplayer)
                G.nodes[child].update({'score': v, 'player': 'min'})
                bestv = max(bestv, v)
        else:
            bestv = 1
            for child in G.successors(n):
                v = _minimax(G, child, maxplayer)
                G.nodes[child].update({'score': v, 'player': 'max'})
                bestv = min(bestv, v)
        return bestv

    # Find the best first move from the given node
    # Assume given node n is a maximiser node.
    best_node = None
    bestv = -1

    for child in G.successors(0):
        v = _minimax(G, child, minplayer)
        G.nodes[child].update({'score': v, 'player': 'min'})
        if v > bestv:
            best_node = child
            bestv = v

    # Add best minimax move to each node
    for n in G.nodes():
        scores = [(v, c['move'], G.nodes[v]['score'])
                  for (u, v, c) in G.out_edges(n, data=True)]
        if scores:
            best_move = max(scores, key=lambda t: t[2])[1]
            G.nodes[n]['best_move'] = best_move

    # Analyze next move
    move_scores = [(v, c['move'], G.nodes[v]['score'])
                   for (u, v, c) in G.out_edges(0, data=True)]
    # If all next moves (G[0]) have zero score, try center moves
    if set([n[2] for n in move_scores]) == {0}:
        return None

    else:
        return G.nodes[0]['best_move']
