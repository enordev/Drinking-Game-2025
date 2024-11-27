import random

players = []
tasks = ["Sing a song", "Do 10 push-ups", "Tell a joke"]

# Add player names
num_players = int(input("Enter the number of players: "))
for i in range(num_players):
    name = input(f"Enter name for player {i + 1}: ")
    players.append(name)

# Task game loop
while tasks:
    for player in players:
        if not tasks:
            break
        task = random.choice(tasks)
        print(f"{player}, your task is: {task}")
        input("Press Enter when you've completed the task.")
        tasks.remove(task)

print("Game Over!")
