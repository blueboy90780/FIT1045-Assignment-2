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
        return self.__str__()

    def __str__(self) -> str:
        """
        Written by: Angus Corr
        Description: Returns the representation of the card as a string eg Ace of Spades
        Arguments: self (the card)
        Returns: A string
        """
        return f"{self.rank.name} of {self.suit.name}"

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
        Description: Determines if a card is less than another card
        Arguments: self - the self card, the other card
        Returns: True if the card is less than the other and False otherwise
        """
        if self.suit == other.suit:
            if self.rank < other.rank:
                return True
        elif self.suit < other.suit:
            return True
        return False
