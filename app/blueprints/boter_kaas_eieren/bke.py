from flask import Blueprint, request, jsonify, render_template

bke = Blueprint(
    "bke",
    __name__,
    url_prefix="/bke",
    template_folder="templates",
    static_folder="static"

    )

class TicTacToe:
    def __init__(self):
        """ Initialiseer het bord en de huidige speler. Definieer ook de winnende combinaties. """
        self.board = [' '] * 9
        self.current_player = 'X'
        # 1. Definieer de winnende combinaties (3 op een rij, kolom of diagonaal)
        self.winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # Rijen
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # Kolommen
            (0, 4, 8), (2, 4, 6) # Diagonalen
        ]

    def make_move(self, position):
        """ Probeer een zet te maken op de gegeven positie. Retourneer True als de zet succesvol is, anders False. """
        # 1. Controle op positie leeg is, zo ja zet de huidige speler op die positie
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False
    
    def check_winner(self):
        """ Controleer of er een winnaar is, een gelijkspel of dat het spel nog bezig is. 
        Retourneer 'X', 'O', 'Gelijkspel' of None. """
        # 1. Controleer alle winnende combinaties, als er een combinatie is waarbij alle drie de posities hetzelfde zijn en niet leeg, dan is er een winnaar
        for combo in self.winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return self.board[combo[0]]
            
        # 2. Gelijkspel als er geen lege posities meer zijn
        if " " not in self.board:
            return 'Tie'
          
        # 3. Geen winnaar of gelijkspel, dus probleem met de status van het spel
        return None

    def get_winning_combination(self):
        """ Retourneer de winnende combinatie als er een winnaar is, anders None. """
        for combo in self.winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return combo
        return None
        
    def reset(self):
        """ Reset het bord en de huidige speler. """
        self.board = [' '] * 9
        self.current_player = 'X'
        
game = TicTacToe()

@bke.route('/play')
def play():
    return render_template('bke.html', board=game.board, current_player=game.current_player)

@bke.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    position = data['position']
    if game.make_move(position):
        winner = game.check_winner()
        winning_combination = game.get_winning_combination()
        return jsonify({'status': 'success', 'winner': winner, 'board': game.board, 'winning_combination': winning_combination})
    else:
        return jsonify({'status': 'error', 'message':'Invalid move'})

@bke.route('/reset', methods=['POST'])
def reset():
    game.reset()
    return jsonify({'status': 'success', 'board': game.board, 'current_player': game.current_player})
