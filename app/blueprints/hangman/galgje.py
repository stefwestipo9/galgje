from flask import Blueprint, render_template, jsonify, request
import random


Hangman = Blueprint(
    "galgje", 
    __name__, 
    url_prefix="/hangman", 
    template_folder="templates",
    static_folder="static")

def get_words(filepath="app/blueprints/hangman/woorden.txt"):
    with open(filepath, "r") as read_file:
        words = read_file.read()
        words = words.split("\n")
        return words

def write_word(word, filepath="app/blueprints/hangman/woorden.txt"):
    with open(filepath, "a") as write_file:
            write_file.write(f"\n{word}")

class Galgje:
    def __init__(self):
        self.words = get_words()
        self.current_word = ""
        self.guessed_letters = ""
        self.levens = 6
        self.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.status = None

    def start_game(self):
        if self.current_word:
            # 1. Bij nieuwe spel een ander woord pakken
            choices = [word for word in self.words if word != self.current_word]
            self.current_word = random.choice(choices) if choices else random.choice(self.words)
        
        else:
            # 2. Bij opstarten hoeft niet gecontroleerd te worden op nieuwe woord
            self.current_word = random.choice(self.words)
        self.current_word = self.current_word.upper()
        self.guessed_letters = ""
        self.levens = 6
        self.status = "playing"
    
    def guess_letter(self, letter):
        letter = letter.upper()
        if letter not in self.guessed_letters:
            self.guessed_letters += letter
            if letter not in self.current_word:
                self.levens -= 1
        
    def get_game_state(self):
        display_word = "".join([letter if letter in self.guessed_letters else "_" for letter in self.current_word])
        data = {
            "display_word": display_word, 
            "letters":self.letters,
            "levens": self.levens,
            "guessed": self.guessed_letters,
            }
        if display_word == self.current_word:
            self.status = "won"
        elif self.levens <= 0:
            self.status = "lost"
            data["full_word"] = self.current_word
        data["status"] = self.status
        return data
    
    def restart_game(self):
        self.start_game()
    
    def get_status(self):
        return self.status


galgje_game = Galgje()

@Hangman.route("/play")
def play():
    if galgje_game.get_status() != "playing":
        galgje_game.start_game()
    return render_template("galgje.html", game_state=galgje_game.get_game_state())

@Hangman.route("/guess", methods=["POST"])
def guess():
    # receive the guessed letter from the POST body
    letter = request.form.get("letter", "").lower()
    if letter:
        galgje_game.guess_letter(letter=letter)
    return jsonify(galgje_game.get_game_state())


@Hangman.route("/restart", methods=["POST"])
def restart():
    galgje_game.restart_game()
    return jsonify(galgje_game.get_game_state())
