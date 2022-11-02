# Written by Nguyen Tien Dung
# Last Updated 25/09/22
from __future__ import annotations

import random
from typing import Any

from cards import Card, Rank, Suit
from human import HumanPlayer
from basic_ai import BasicAIPlayer
from better_ai import BetterAIPlayer
from round import Round



# Sources Used:
# https://www.geeksforgeeks.org/enum-in-python/
# https://www.w3schools.com/python/ref_random_shuffle.asp
# https://visualgit.readthedocs.io/en/latest/pages/naming_convention.html
# https://stackoverflow.com/questions/4528740/wrapping-around-a-list-as-a-slice-operation

class Hearts:
    # Variable Declaration
    numOfPlayers: int = 0
    targetScore: int = 0
    deck: list[Card] = []
    players: list[BasicAIPlayer] = []

    def __init__(self) -> None:
        # Variable Initialization
        self.get_user_input()
        self.players = None

    def get_user_input(self) -> None:
        """
        Written By: David
        Ask for user input until a valid input is given. Method will ask for input again if an invalid input is given
        """
        while True:
            try:
                self.targetScore = int(input("Please enter a target score to end the game: "))
                break
            except ValueError:
                print("Please enter a number")

        while True:
            try:
                self.numOfPlayers = int(input("Please enter the number of players (3-5): "))
                if self.numOfPlayers < 3 or self.numOfPlayers > 5:
                    raise TypeError
                break
            except ValueError:
                print("Please enter a number")
            except TypeError:
                print("Please enter a number between 3 and 5")

    def generate_players(self) -> list[BasicAIPlayer]:
        """
        Written By: David
        Generate a list of players based on numOfPlayers.
        """

        players: list[BasicAIPlayer] = []
        # Generate players
        for i in range(1, self.numOfPlayers + 1):
            players.append(BasicAIPlayer("Player " + str(i)))

        return players

    def generate_deck(self) -> list[Card]:
        """
        Generate a standard deck of 52 playing cards, this function will always return the same set of cards in the same order, rank and suit. The only exception is unless there are 3 or 5 players. For the sake of efficiency, this entire function could be replaced with one variable initialized with a list of Card Objects. This eliminates the need for loops and any function calls entirely, saving massive CPU time.
        """
        deck: list[Card] = []
        # generate a standard deck of 52 playing cards
        for i in range(2, 13 + 2):
            for j in range(4):
                deck.append(Card(Rank(i), Suit(j)))

        # If the game is starting with 3 players, remove the Two of Diamonds. If 5, remove spades as well
        if self.numOfPlayers == 3: deck.remove(Card(Rank.Two, Suit.Diamonds))
        if self.numOfPlayers == 5:
            deck.remove(Card(Rank.Two, Suit.Diamonds))
            deck.remove(Card(Rank.Two, Suit.Spades))

        return deck

    def deal_cards(self) -> None:
        """
        Written By: David
        This functions assigns each self.players.hand a set of cards object from the deck list.

        It DOES NOT:
        Order the cards in each player's hand in ascending order. That is done in round.py

        IT DOES:
        - huffles the deck such that all cards switch index with another card in the list
        - Ensure every player has at least one card that isn't the Queen of Spades or from Hearts
        """
        valid_hands: int = 0
        # Shuffle it using random
        random.shuffle(self.deck)
        # Deal them out to the player one by one
        for i in range(1, len(self.deck) + 1):
            self.players[i % self.numOfPlayers].hand.append(
                self.deck[i - 1])  # Modulus by numOfPlayers to warp around when i > numOfPlayers

        # Ensure every player has at least one card that isn't the Queen of Spades or from Hearts
        for player in self.players:
            for card in player.hand:
                if card.suit != Suit.Hearts or card == Card(Rank.Queen, Suit.Spades):
                    # If a single card is found that is not hearts or queen of spades, player has valid hand,
                    # immediately skip to next player \ Instead of checking for the rest of the hands, saving time =
                    # performance
                    valid_hands += 1
                    break  # breaks out of this nested loop, but still continue with the first loop

        if valid_hands != len(self.players):
            self.deal_cards()  # Recursively shuffles deck until all players have valid hands

    def pass_cards(self, game_round) -> list[tuple[str, list[Card], str]]:
        """
        Written By: David
        Returns a list of size-3 tuples, with
        1) The player name passing the card
        2) The list of cards being passed
        3) The receiving player

        To be used exclusively with self.check_round(). This function will not work unless there exist an instance of a round class. 
        """
        # Initialize Variables
        cards_to_pass: list[
            list[Card]] = []  # A list of list of cards for each player. E.g Index 0 = list[Cards] of Player 1
        # A dictionary logging all the names of each player and the cards they got passed
        dealt_cards_dict: list[tuple[str, list[Card], str]] = []  # List of size 3 tuples
        pass_number: int | Any = game_round % len(
            self.players)  # The number of players away from current player to pass the cards to

        # Players then have to choose 3 cards to pass
        for i in range(len(self.players)):
            cards_to_pass.append(self.players[i].pass_cards())

        # Then pass to the corresponding player based on number of rounds played
        for i in range(len(self.players)):
            player_passing = self.players[i].name
            # Gets the wrapped list with the players[i] as index 0 of that list
            wrapped_list = self.players[i:] + self.players[:i]
            # The player to pass to, for example if Player 1's turn to pass and round #1, then this variable is Player 2
            player_to_pass = self.players[
                self.players.index(wrapped_list[pass_number])]  # Player_to_pass being a BasicAI Object
            card_dealt = cards_to_pass[i]
            player_to_pass.hand.extend(card_dealt)
            dealt_cards_dict.append((player_passing, card_dealt, player_to_pass.name))

        return dealt_cards_dict

    def round_check(self) -> None:
        """
        Written By: David
        Executes the entire game from start to end.
        This function calls self.generate_deck(), self.deal_cards() and self.pass_cards()
        It takes the role of setting up the game, tallying user's score and determining if the game ends and who the winner is

        IT DOES NOT
        Have any code pertaining to the round itself.
        """
        winning_player: str = ""
        game_round: int = 0
        while True:

            # Setting up round
            game_round += 1
            self.deck = self.generate_deck()
            self.deal_cards()

            # Start of round
            print(f"========= Starting round {game_round} =========")
            
            self.pass_cards(game_round)
            

            match: Round = Round(self.players)  # Go through one round

            # End of round
            print(f"========= End of round {game_round} =========")
            # If a plyer shoots the moon, print player's name
			
            if match.shootMoonIndex is not None:
                print(f"{self.players[match.shootMoonIndex]} has shot the moon! Everyone else receives 26 points")
            for player in self.players:
                print(
                    f"{player}'s total score: {player.total_score}")  # Round() will always update player.total_score every time it's called without resetting

            score_list: list[int] = [player.total_score for player in
                                     self.players]  # Each index + 1 corresponds to a player, e.g index 0 = player 1
            game_highest_score: int = max(score_list)  # Creates a list of all player's
            # score in the game and find the maximum in one line

            # If a player reaches the targetScore
            if game_highest_score >= self.targetScore:
                # Find player(s) with the lowest score
                if score_list.count(min(score_list)) > 1:
                    continue  # If there are multiple players with the lowest score, rounds continue until a winner is
                    # decided.
                else:
                    winning_player = self.players[score_list.index(min(score_list))].name
                    break  # Break the infinite loop, end of game

        print(f"{winning_player} is the winner!")

if __name__ == "__main__":
    """
    Written By: David
    I like cheese
    """
    Hearts()
