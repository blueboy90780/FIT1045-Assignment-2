from cards import Card, Rank, Suit
from player import Player
from basic_ai import BasicAIPlayer
from better_ai import BetterAIPlayer
from human import HumanPlayer
from round import Round
from hearts import Hearts

def generate_players(numberOfPlayers):
    players = []
    players.append(HumanPlayer())
    for i in range(numberOfPlayers - 2):
        players.append(BasicAIPlayer(f"Player {i + 1}"))
    players.append(BetterAIPlayer(f"Player {numberOfPlayers - 1}"))
    return players

if __name__ == "__main__":
    playing = True
    while playing:
        print("Welcome to ♥ HEARTS ♥")
        game = Hearts()
        game.players = generate_players(game.numOfPlayers)
        game.round_check()
        enter = input("Play again? Enter 'y' to play again.")
        if enter == "y":
            playing = True
        else:
            playing = False