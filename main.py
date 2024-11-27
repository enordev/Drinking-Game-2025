from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Initialize players and tasks
players = []
tasks = [
    {"text": "Ota huikka", "image": "images/huikka.webp"},
    {"text": "Kerro vitsi", "image": "images/pushups_image.png"},
    {"text": "Kertokaa lempparielokuvanne, jos jollain on sama he juo 2", "image": "images/shrek.jpg"},
    {"text": "Laita BÄNGERI biisi jonoon", "image": "images/catdj.webp"},
    {"text": "Tarjoa hörppy", "image": "images/huikka.webp"},
]
current_player_index = 0

@app.route("/")
def home():
    return render_template("index.html", players=players, tasks_left=len(tasks))

@app.route("/add_player", methods=["POST"])
def add_player():
    name = request.form["player_name"]
    if name:
        players.append(name)
    return redirect(url_for("home"))

@app.route("/start_game")
def start_game():
    if not players or not tasks:
        return redirect(url_for("home"))
    return redirect(url_for("next_turn"))

@app.route("/next_turn")
def next_turn():
    global current_player_index
    if not tasks:
        return render_template("game_over.html")
    current_player = players[current_player_index]
    task = random.choice(tasks)
    current_player_index = (current_player_index + 1) % len(players)
    return render_template("task.html", player=current_player, task=task)

if __name__ == "__main__":
    app.run(debug=True)
