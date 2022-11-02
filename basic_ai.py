# Written by Angus Corr
# Last Updated 18/09/2022

from __future__ import annotations

from cards import Card, Rank, Suit
from player import Player


class BasicAIPlayer(Player):
    def __init__(self, name: str) -> None:
        Player.__init__(self, name)

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

    def pass_cards(self) -> list[Card]:
        sortedHand = self.sort_hand_by_value()
        returnList = []
        for i in range(-3, 0):
            self.hand.remove(sortedHand[i])
            returnList.append(sortedHand[i])
        return returnList


if __name__ == "__main__":
    cards = []
    for i in range(13):
        for j in range(4):
            cards.append(Card(Rank[i], Suit[j]))
