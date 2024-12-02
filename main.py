from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Initialize players and tasks
players = []
tasks = [
    {"text": "Ota huikka", "image": "images/birbdrink.webp"},
    {"text": f"Kerro vitsi, jos  nauraa hän juo, jos ei sie juot. idiootti.", "image": "images/temp.webp"},
    {"text": "Kertokaa lempparielokuvanne, jos jollain on sama he juo 2", "image": "images/shrek.jpg"},
    {"text": "Laita BÄNGERI biisi jonoon", "image": "images/catdj.webp"},
    {"text": f"Tarjoa hörppy pelaajalle  ", "image": "images/huikka.webp"},
    {"text": f"Arvaa pelaajan  lempiväri, jos oikein valitse 2 pelaajaa jotka juo 1, jos väärin, juo 1", "image": "images/huikka.webp"},
    {"text": f"Ylävitonen w/  ", "image": "images/heilfive.webp"},
    {"text": f"Akat juo", "image": "images/sigmafemale.jpg"},
    {"text": f"Ukot juo", "image": "images/sigmamale.jpg"}, 
    {"text": f"Tantut juo", "image": "images/huikka.webp"},
    {"text": f"Tantut juottaa", "image": "images/temp.webp"},
    {"text": f"Tee 3 aineksen drinkki,  juo sen", "image": "images/wd40.webp"},
    {"text": "Kaikki ketkä on soittanut kitaraa illan aikana juo", "image": "images/kitara.webp"},
    {"text": "äänestäkää kuka on eniten kännissä, hän juo vettä", "image": "images/temp.webp"},
    {"text": "äänestäkää kuka on vähiten kännissä, hän juo shotin, jos kaikki on hyvässä maistissa ota hörö", "image": "images/temp.webp"},
    {"text": "Kaikille välivesi", "image": "images/kitara.webp"},
    {"text": f"Kädenvääntö pelaajaa  vastaan", "image": "images/temp.webp"},
    {"text": f"Kissanomistajat juo", "image": "images/kissastrong.webp"},
    {"text": f"Koiranomistajat juo", "image": "images/koira.webp"},
    
 # Chatgpt based
    {"text": f"Keksi sääntö", "image": "images/temp.webp"},
    {"text": "Kaikki, joilla on siniset vaatteet, juo 2.", "image": "images/temp.webp"},
    {"text": "Kaikki ketkä juo lasista, juo.", "image": "images/glasses.webp"},
    {"text": f"Pelaaja  valitsee kuka juo 1", "image": "images/temp.webp"},
    {"text": f"Keksi kielto! Se, joka rikkoo sitä seuraavaksi, juo 3.", "image": "images/temp.webp"},
    {"text": "Kaikki ottavat huikan yhtä aikaa.", "image": "images/temp.webp"},
    {"text": "Nimeä nainen. Ensimmäinen, joka ei keksi naista, juo 2.", "image": "images/temp.webp"},
    {"text": f"Arvaa pelaajan  syntymäkuukausi, jos väärin, juo 1.", "image": "images/temp.webp"},
    {"text": "Kaikki, joilla on puhelin kädessä, juo.", "image": "images/temp.webp"},
    {"text": f"Tanssi humppaa tai juo", "image": "images/temp.webp"},
    {"text": "Kerro nolo tarina itsestäsi tai juo 2.", "image": "images/temp.webp"},
    {"text": f"Esitä kysymys pelaajalle , jos hän kieltäytyy vastaamasta, hän juo 2.", "image": "images/temp.webp"},
    {"text": "Kaikki, jotka ovat myöhästyneet jostain tänä vuonna, juo.", "image": "images/temp.webp"},
    {"text": "Kaikki kertovat jotain mitä he ovat oppineet tänään. Jos et keksi mitään, juot.", "image": "images/temp.webp"},
    {"text": "Valitse kategoria (esim. hedelmät). Pelaajat nimeävät asioita kategoriasta. Joka mokaa, juo.", "image": "images/temp.webp"},
    {"text": "Kaikki, jotka ovat ottaneet selfien tänään, juo.", "image": "images/temp.webp"},
    {"text": "Ota huikka ja valitse toinen, joka tekee saman.", "image": "images/temp.webp"},
    
    {"text": "Paljasta jokin erikoinen taitosi, tai juo 2.", "image": "images/temp.webp"},
    {"text": f"Keksi pelaajalle  lempinimi. Jos muut eivät hyväksy sitä, juot 2.", "image": "images/temp.webp"},
    {"text": f"Valitse elokuva tai TV-sarja ja kuvaile se kolmella sanalla.  arvaa ja juokaa vaikka molemmat emt", "image": "images/temp.webp"},
    {"text": f"Arvaa tykkääkö enemmän pizzasta vai hampurilaisista. Jos se on väärin, juo 1.", "image": "images/temp.webp"},
    {"text": "yksi totuus ja kaksi valhetta", "image": "images/temp.webp"},
    {"text": "Kaikki kertokaa yksi asia bucket listiltäsi. Jos et halua kertoa, juo 2.", "image": "images/temp.webp"},
    {"text": "Valitse juomakaveri, jonka kanssa juot seuraavan kierroksen yhteen.", "image": "images/temp.webp"},
    {"text": "Jaa hauska meemisi tai juo 2.", "image": "images/temp.webp"},
    {"text": "Valitse eläin, joka kuvaa sinua parhaiten. Jos muut ovat eri mieltä, juo 1.", "image": "images/temp.webp"}
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
    task_template = random.choice(tasks)
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
