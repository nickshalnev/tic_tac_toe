import logging
from flask import Blueprint, render_template
from flask_socketio import emit, join_room, leave_room
from . import socketio

main = Blueprint('main', __name__)

games = {}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_win(board):
    for row in board:
        if row[0] == row[1] == row[2] != '':
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    return None


@main.route('/')
def index():
    logger.info("User accessed the homepage")
    return render_template('index.html')


@socketio.on('join')
def on_join(data):
    room = data['room']
    player = data['player']
    join_room(room)

    if room not in games:
        games[room] = {
            'board': [['', '', ''], ['', '', ''], ['', '', '']],
            'turn': 'X',
            'players': []
        }

    if player in [p['symbol'] for p in games[room]['players']]:
        emit('join_error', {'message': 'This symbol is already taken. Choose another one.'}, room=room)
        logger.warning(f"Player {player} attempted to join room {room}, but symbol is already taken")
    else:
        games[room]['players'].append({'symbol': player})
        emit('game_state', games[room], room=room)
        logger.info(f"Player {player} joined room {room}")


@socketio.on('leave')
def on_leave(data):
    room = data['room']
    player = data['player']
    leave_room(room)

    if room in games:
        games[room]['players'] = [p for p in games[room]['players'] if p['symbol'] != player]
        if len(games[room]['players']) == 0:
            del games[room]
            logger.info(f"Room {room} has been deleted as there are no players left")


@socketio.on('make_move')
def on_make_move(data):
    room = data['room']
    row = data['row']
    col = data['col']
    player = data['player']
    game = games[room]

    if game['turn'] == player and game['board'][row][col] == '':
        game['board'][row][col] = player
        winner = check_win(game['board'])
        if winner:
            emit('game_over', {'winner': winner}, room=room)
            del games[room]
            logger.info(f"Player {player} won the game in room {room}")
        else:
            game['turn'] = 'O' if game['turn'] == 'X' else 'X'
            emit('game_state', game, room=room)
            logger.info(f"Player {player} made a move in room {room}")
    else:
        emit('invalid_move', {'message': 'Not your turn or invalid move'}, room=player)
        logger.warning(f"Player {player} attempted an invalid move in room {room}")
