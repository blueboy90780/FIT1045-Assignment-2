# Written by Angus Corr
# Last Updated 18/09/2022

from __future__ import annotations 
from task1 import Card, Rank, Suit


class BasicAIPlayer:
    def __init__(self, name: str) -> None:
        self.hand: list[Card] = []
        self.round_score = 0
        self.total_score = 0
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def check_valid_play(self, card: Card, trick: list[Card], broken_hearts: bool) -> tuple(bool, str):
        try:
            trickSuit = trick[0].suit
        except IndexError:
            trickSuit = None
        if card is None:
            raise ValueError("None")
        if (not trickSuit is None):
            for i in trick:
                if i is None:
                    raise ValueError("None")
		# Checking for Two of Clubs
        for i in self.hand:
            if i == Card(Rank.Two, Suit.Clubs) and not card == Card(Rank.Two, Suit.Clubs):
                return (False, "Two of Clubs must be played on the first round.")
		
		# Checking for valid first moves (i.e hearts has been broken)
        if trickSuit == None:
            if card.suit == Suit.Hearts and broken_hearts == False:
                for i in self.hand:
                    if not i.suit == Suit.Hearts:
                        return (False, "Hearts is not broken, cannot lead with hearts.")
                return (True, "")


		# Checking if Queen of Spades on First trick
        if trickSuit == Suit.Clubs and trick[0].rank == Rank.Two and card.rank == Rank.Queen and card.suit == Suit.Spades:
            return (False, "Cannot play Queen of Spades on first trick.")

		# Checking if hearts on first trick
        if trickSuit == Suit.Clubs and trick[0].rank == Rank.Two and card.suit == Suit.Hearts:
            return (False, "Cannot play Hearts on first round.")


		# Checking if suit is valid
        if card.suit == trickSuit:
            return (True, "")
        else:
            for i in self.hand:
                if i.suit == trickSuit:
                    return (False, "Must play valid suit if contained in hand.")
            return (True, "")

    # Playing lowest value card
    def play_card(self, trick: list[Card], broken_hearts: bool) -> Card:
        sortedHand = self.sort_hand_by_value()
        valid = False
        i = 0
        check = self.check_valid_play(sortedHand[i], trick, broken_hearts)
        valid = check[0]
        while not valid:
            i += 1
            check = self.check_valid_play(sortedHand[i], trick, broken_hearts)
            valid = check[0]

        self.hand.remove(sortedHand[i])
        return sortedHand[i]

    # sorting cards in hand from lowest ranking to highest ranking
    def sort_hand_by_value(self) -> list[Card]:
        sortedHand = []
        for i in self.hand:
            sortedHand.append(i)

        doneSort = False
        while not doneSort:
            count = 0
            i = 0
            while i < len(sortedHand) - 1:
                if sortedHand[i + 1] < sortedHand[i]:
                    a = sortedHand[i]
                    sortedHand[i] = sortedHand[i + 1]
                    sortedHand[i + 1] = a
                    count += 1
                i += 1
            if count == 0:
                doneSort = True
        return sortedHand

    def pass_cards(self) -> list[Card]:
        sortedHand = self.sort_hand_by_value()
        returnList = []
        for i in range(-3, 0):
            self.hand.remove(sortedHand[i])
            returnList.append(sortedHand[i])
        return returnList

    def update_total_score(self):
        self.total_score += self.round_score
        self.round_score = 0