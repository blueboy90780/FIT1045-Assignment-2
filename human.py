# Written by Angus Corr
# Last Updated 18/09/2022

from __future__ import annotations

from cards import Card, Rank, Suit
from player import Player


class HumanPlayer(Player):

    def __init__(self) -> None:
        name = input("Please enter your name: ")
        Player.__init__(self, name)

    def play_card(self, trick, broken_hearts) -> Card:
        valid = False
        self.hand = self.sort_hand_by_value()
        self.print_hand()
        # Checking for a valid input
        while not valid:
            # Checking if user input is within the valid range and is an integer
            cardIndex = self.get_user_input()

            check = self.check_valid_play(self.hand[cardIndex], trick, broken_hearts)
            if check[0]:
                valid = True
            else:
                print(check[1])
        returning = self.hand[cardIndex]
        self.hand.remove(self.hand[cardIndex])
        return returning

    def pass_cards(self) -> list[Card]:
        valid = False
        self.hand = self.sort_hand_by_value()
        self.print_hand()

        while not valid:
            try:
                cardIndices = input("Select three cards to pass, (x,y,z eg: 1,2,3): ")
                for i in cardIndices:
                    if not ((ord(i) == 44) or (ord(i) > 47 and ord(i) < 58)):
                        raise ValueError
                cardIndices = cardIndices.split(",")
                returning = []
                indexList = []
                for i in range(len(cardIndices)):
                    index = int(cardIndices[i])
                    if not (index >= 0 and index < len(self.hand)):
                        raise IndexError
                    indexList.append(index)
                    returning.append(self.hand[index])
                valid = True
            except ValueError:
                print("Please enter only valid integers seperated by commas as shown in the example below.")
            except IndexError:
                print("Please enter valid indices.")
        indexList.sort()
        for i in range(len(indexList)):
            self.hand.remove(self.hand[indexList[i] - i])
        return returning

    # Returns an integer corresponding to the index of a card chosen by a player in the list
    # checks to ensure user input is within valid range and is an integer
    def get_user_input(self) -> int:
        rightInput = False
        while not rightInput:
            try:
                cardIndex = int(input("Select a card to play: "))
                if cardIndex < 0 or cardIndex >= len(self.hand):
                    raise IndexError
            except ValueError:
                print("You must enter an integer.")
            except IndexError:
                print("Invalid card index.")
            else:
                rightInput = True
        return cardIndex

    # To be completed
    def print_hand(self) -> None:
        stringList = ["", "", "", "", "", ""]
        for k, i in enumerate(self.hand):
            for j in range(len(stringList)-1):
                stringList[j] = stringList[j] + str(i).split("\n")[j]
            if k < 10:
                stringList[5] = stringList[5] + f"   {k}   "
            else:
                stringList[5] = stringList[5] + f"   {k}  "
        for i in stringList:
            print(i)
