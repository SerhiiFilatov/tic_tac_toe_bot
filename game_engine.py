import copy
import random


def is_winner(let, g_f):
    return (
        # horizontal
        (g_f[0][0] == let and g_f[0][1] == let and g_f[0][2] == let) or
        (g_f[1][0] == let and g_f[1][1] == let and g_f[1][2] == let) or
        (g_f[2][0] == let and g_f[2][1] == let and g_f[2][2] == let) or
        # vertical
        (g_f[0][0] == let and g_f[1][0] == let and g_f[2][0] == let) or
        (g_f[0][1] == let and g_f[1][1] == let and g_f[2][1] == let) or
        (g_f[0][2] == let and g_f[1][2] == let and g_f[2][2] == let) or
        # diagonal
        (g_f[0][0] == let and g_f[1][1] == let and g_f[2][2] == let) or
        (g_f[0][2] == let and g_f[1][1] == let and g_f[2][0] == let)
    )


def turn_move(letter):
    return 'player' if letter == 1 else 'bot'


def get_field_copy(game_field):
    return copy.deepcopy(game_field)


def isSpaceFree(game_field, x: int, y: int):
    return game_field[x][y] == 0


def full_board(game_field):
    return all(g != 0 for i in game_field for g in i)


def chooseRandomMoveFromList(board, movesList):
    possibleMoves = []
    for x in movesList:
        if isSpaceFree(board, x[0], x[1]):
            possibleMoves.append([x[0], x[1]])
    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None


def makeMove(board, letter, x, y):
    board[x][y] = letter


def bot_move(game_field, bot_letter, player_letter):
    bot_letter = bot_letter
    player_letter = player_letter

    for x in range(len(game_field)):
        for y in range(len(game_field[x])):
            board = get_field_copy(game_field)
            if isSpaceFree(game_field=board, x=x, y=y):
                makeMove(board=board, letter=bot_letter, x=x, y=y)
                if is_winner(g_f=board, let=bot_letter):
                    return [x, y]

    for i in range(len(game_field)):
        for j in range(len(game_field[i])):
            board = get_field_copy(game_field)
            if isSpaceFree(game_field=board, x=i, y=j):
                makeMove(board=board, letter=player_letter, x=i, y=j)
                if is_winner(g_f=board, let=player_letter):
                    return [i, j]

    if isSpaceFree(game_field, 1, 1):
        return [1, 1]

    move = chooseRandomMoveFromList(game_field, [[0,0], [0,2], [2,0], [2,2]])
    if move != None:
        return move

    return chooseRandomMoveFromList(board, [[2,1], [1,0], [0,1], [1,2]])

