# Written by Angus Corr
# Last Updated 17/09/2022
# Docu header template
"""
Written by: Angus Corr
Description:
Arguments:
Returns:
"""

from __future__ import annotations  # for type hints of a class in itself

from enum import Enum


class Rank(Enum):
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14

    def __lt__(self, other: Rank) -> bool:
        """
        Written by: Angus Corr
        Description: Determines if a rank is less than another rank
        Arguments: self - the self rank, the rank of the other card
        Returns: True if the self rank is less than the other and False otherwise
        """
        if self.value < other.value:
            return True
        else:
            return False


class Suit(Enum):
    Clubs = 0
    Diamonds = 1
    Spades = 2
    Hearts = 3

    def __lt__(self, other: Suit) -> bool:
        """
        Written by: Angus Corr
        Description: Determines if a suit is less than another suit
        Arguments: self - the self suit, the suit of the other card
        Returns: True if the self suit is less than the other and False otherwise
        """
        if self.value < other.value:
            return True
        else:
            return False


class Card:
    
    CARD_UPPER = "┌─────┐"

    RANK_DICTIONARY = {
        2 : "│2    │.│    2│",
        3 : "│3    │.│    3│",
        4 : "│4    │.│    4│",
        5 : "│5    │.│    5│",
        6 : "│6    │.│    6│",
        7 : "│7    │.│    7│",
        8 : "│8    │.│    8│",
        9 : "│9    │.│    9│",
        10 : "│10   │.│   10│",
        11 : "│J    │.│    J│",
        12 : "│Q    │.│    Q│",
        13 : "│K    │.│    K│",
        14 : "│A    │.│    A│"
    }

    SUIT_DICTIONARY = {
        0 : "│  ♣  │",
        1 : "│  ♦  │",
        2 : "│  ♠  │",
        3 : "│  ♥  │"
    }    

    CARD_LOWER = "└─────┘"      
				

    def __init__(self, rank: Rank, suit: Suit) -> None:
        """
        Written by: Angus Corr
        Description: Initialises an instance of the card class
        Arguments: self, rank (the rank of the card eg: two, three etc.), suit (the suit of the card eg: spades, diamonds etc)
        Returns: None
        """
        self.rank = rank
        self.suit = suit

    def __repr__(self) -> str:
        """
        Written by: Angus Corr
        Description: Returns the representation of the card as a string
        Arguments: self (the card)
        Returns: A string
        """
        return f"{self.rank.name} of {self.suit.name}"

    def __str__(self) -> str:
        """
        Written by: Angus Corr
        Description: Returns the representation of the card as a string eg Ace of Spades
        Arguments: self (the card)
        Returns: A string
        """
        rank = Card.RANK_DICTIONARY[self.rank.value].split(".")
        card = f"{Card.CARD_UPPER}\n{rank[0]}\n{Card.SUIT_DICTIONARY[self.suit.value]}\n{rank[1]}\n{Card.CARD_LOWER}"
        return card

    def __eq__(self, other: Card) -> bool:
        """
        Written by: Angus Corr
        Description: Returns if one card is equal to another card
        Arguments: self, other. one card and another card
        Returns: True is equal False otherwise
        """
        if self.rank == other.rank and self.suit == other.suit:
            return True
        else:
            return False

    def __lt__(self, other: Card) -> bool:
        """
        Written by: Angus Corr
        Modified by: Nguyen Tien Dung
        Description: Determines if a card is less than another card
        Arguments: self - the self card, the other card
        Returns: True if the card is less than the other and False otherwise
        """

        # Re-implementation by David
        # Rank precedes Suit. A 2 of Hearts is less than 3 of Spades, rank should take precedence

        if self.rank < other.rank:
            return True  # Does not matter what the suit is, if the rank is less, then the value of the card is less
        elif self.rank == other.rank:
            # If it's equal, we then take into account of the card suit
            if self.suit < other.suit:
                return True
        else: # If self.rank > other.rank
            return False

        # Angus's implementation
        # if self.suit == other.suit:
        #     if self.rank < other.rank:
        #         return True
        # elif self.suit < other.suit:
        #     return True
        # return False

    def __gt__(self, other: Card):
        if self.rank > other.rank:
            return True  # Does not matter what the suit is, if the rank is less, then the value of the card is less
        elif self.rank == other.rank:
            # If it's equal, we then take into account of the card suit
            if self.suit > other.suit:
                return True
        else: # If self.rank < other.rank
            return False


if __name__ == "__main__":
    print(Card(Rank(2), Suit(0)))
