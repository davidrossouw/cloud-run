import json
import os
import random
import time
from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

from game import moves_available, play, checkWin, board2string

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Load ttt lookup table
MOVES_PATH = './connect4_minimax.json'
with open(MOVES_PATH, 'r') as f:
    moves = json.load(f)



@app.route("/")
def index():
    # Initial state
    if "board" not in session:
        session["board"] = [
            ['-','-','-','-'],
            ['-','-','-','-'],
            ['-','-','-','-'],
            ['Y','R','Y','R']
        ]
        session["winner"] = False
        session["turn"] = "Y"
        session["game"] = 'in progress'
        return render_template("game.html", board=session["board"], game=session["game"])

    
    ## Computer turn
    # Check game
    winner = checkWin(session['board'])
    # Check if finished
    if winner in ('Y', 'R'):
        #TODO: tidy up game=winner
        return render_template("game.html", board=session["board"], game=winner)


    board_string = board2string(session["board"])
    move = moves.get(board_string)
    if not move:
        print('move not found!')
        move = random.choice(moves_available(session['board']))
    print(f'computer move found!!!: {move}')

    session['board'] = play(board=session['board'], player='R', column=move)
    

    # Check game
    winner = checkWin(session['board'])
        
    return render_template("game.html", board=session["board"], game=session["game"])


@app.route("/player_move/<int:column>")
def player_move(column):

    session['board'] = play(board=session['board'], player='Y', column=column)

    print(board2string(session['board']))

    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    session.pop('board')
    return redirect(url_for("index"))


if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host='localhost', port=int(
        os.environ.get('PORT', 8080)), debug=True, use_reloader=True)

