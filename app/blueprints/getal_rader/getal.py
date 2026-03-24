from flask import Blueprint, render_template, jsonify, request
import random

# Bluprint maken
Bagel = Blueprint(
    "getal",
    __name__,
    url_prefix="/getal", 
    template_folder="templates",
    static_folder="static"
)

class getal_raden():
    """
    Spel dat je een 3 cijferige nummer moet raden met unieke getallen,
    met raden 3 uitkomsten, geen juist cijfer is Bagel,een juist cijfer maar niet
    juiste plek is Pico, juist cijfer en juiste plek is Fermi elke keer raden geeft
    per plek 1 van deze 3 terug. 
    """
    def __init__(self):
        self.getal_lengte = 3
        self.getal = None
        self.levens = 6
        self.status = None
        self.guesses = {"getallen":[], "uitkomsten":[]}
        
    def genereer_getal(self):
        getal = random.randrange(0, 10**self.getal_lengte)
        getal = '{:03}'.format(getal)
        return getal

    def check_uniek(self,getal):
        uniek = True
        if len(str(getal)) > len(set(getal)):
            uniek = False
        print(getal, uniek) 
        return uniek

    def genereeer_uniek_getal(self):
        getal = self.genereer_getal()
        uniek = self.check_uniek(getal)
        while not uniek:
            getal = self.genereer_getal()
            uniek = self.check_uniek(getal)
        self.getal = getal
        return getal
    
    def start_spel(self):
        self.genereeer_uniek_getal()
        self.levens = 6
        self.status = "playing"
        self.guesses = {"getallen":[], "uitkomsten":[]}
    
    def raden(self, guess):
        message = []
        if self.status == "playing":
            self.guesses["getallen"].append(guess)
            # checken of het juiste getal geraden is
            if guess == self.getal:
                self.status = "won"
                message = ["Fermi", "Fermi","Fermi"]

            else:
            # Checken of cijfers wel op juist plekken staan
                guess = tuple(guess)
                getal = tuple(self.getal)
                for i, cijfer in enumerate(guess):
                    if cijfer in getal:
                        if cijfer == getal[i]:
                            message.append("Fermi")
                        else:
                            message.append("Pico")
                    else:
                        message.append("Bagel")
                self.levens -= 1
                if self.levens == 0:
                    self.status = "lost"
            self.guesses["uitkomsten"].append(message)
        
    def get_game_state(self):
        data = {
            "status": self.status,
            "levens": self.levens,
            "geraden": self.guesses["getallen"],
            "uitkomsten": self.guesses["uitkomsten"],
        }
        if self.status != 'playing':
            data["getal"] = self.getal
        return data

spel = getal_raden()

@Bagel.route("/play")
def play():
    if spel.status != "playing":
        spel.start_spel()
    return render_template("getal.html", game_state = spel.get_game_state())

@Bagel.route("/guess", methods=["POST"])
def guess():
    guess = request.form.get("guess")
    if guess:
        spel.raden(guess)
    return jsonify(spel.get_game_state())

@Bagel.route("/restart", methods=["POST"])
def restart():
    spel.start_spel()
    return jsonify(spel.get_game_state())