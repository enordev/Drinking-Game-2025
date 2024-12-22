from flask import Flask, render_template, request, redirect, url_for
import random
import json

app = Flask(__name__)

# Initialize players and tasks
players = []
used_tasks = []

# Load tasks from the JSON file
with open("tasks.json", "r", encoding="utf-8") as file:
    tasks = json.load(file)

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
    if not players or not (tasks or used_tasks):
        return redirect(url_for("home"))
    return redirect(url_for("next_turn"))

@app.route("/next_turn")
def next_turn():
    global current_player_index, tasks, used_tasks
    
    if not tasks and not used_tasks:
        return render_template("game_over.html")  # All tasks have been completed

    current_player = players[current_player_index]

    # Decide whether to pick from used tasks (10% chance)
    if used_tasks and random.random() < 0.1:  # 10% chance
        task_template = random.choice(used_tasks)
    else:
        if tasks:
            task_template = random.choice(tasks)
            tasks.remove(task_template)  # Remove from tasks
            used_tasks.append(task_template)  # Add to used_tasks
        else:
            # Fallback to used_tasks if tasks is empty
            task_template = random.choice(used_tasks)

    task_text = task_template["text"]
    
    # Replace placeholders in the task text with dynamic player names
    if "pelaajalle" in task_text or "pelaajan" in task_text:
        random_player = random.choice([p for p in players if p != current_player])  # Exclude current player
        task_text = task_text.replace("pelaajalle", f"pelaajalle {random_player}").replace("pelaajan", f"pelaajan {random_player}")
    
    current_player_index = (current_player_index + 1) % len(players)
    return render_template("task.html", player=current_player, task={"text": task_text, "image": task_template["image"]})

@app.route("/reset_players", methods=["POST"])
def reset_players():
    global players
    players = []  # Clear the players list
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=False)
