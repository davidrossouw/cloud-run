import json
import os
import random
import time
from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

from game import moves_available, play, checkWin, board2string, search, minimax

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

MAX_DEPTH = 7

Session(app)


@app.route("/")
def index():
    # Initial state
    if "board" not in session:
        session["board"] = [
            ['-', '-', '-', '-'],
            ['-', '-', '-', '-'],
            ['-', '-', '-', '-'],
            ['-', '-', '-', '-']
        ]
        session["turn"] = "Y"
        session["winner"] = None
        return render_template("game.html", board=session["board"], winner=session["winner"])

    # Computer turn (Red='R')
    session['winner'] = checkWin(session['board'])
    # Check if player one with their move
    if session['winner'] in ('Y', 'R'):
        # TODO: tidy up game=winner
        return render_template("game.html", board=session["board"], winner=session["winner"])
    # Minimax
    G = search(board=session["board"], max_depth=MAX_DEPTH)
    G, move = minimax(G)

    if move == None:
        print('best move not found!')
        move = random.choice(moves_available(session['board']))

    session['board'] = play(board=session['board'], player='R', column=move)

    # Check if computer one with their move
    session['winner'] = checkWin(session['board'])
    if session['winner'] in ('Y', 'R'):
        return render_template("game.html", board=session["board"], winner=session["winner"])

    return render_template("game.html", board=session["board"], winner=session["winner"])


@app.route("/player_move/<int:column>")
def player_move(column):
    session['board'] = play(board=session['board'], player='Y', column=column)
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
