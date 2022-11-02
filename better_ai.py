# Written by Angus Corr
# Last Updated 22/09/2022

from __future__ import annotations
from basic_ai import BasicAIPlayer

from cards import Card, Rank, Suit
from player import Player


class BetterAIPlayer(Player):

    def play_card(self, trick: list[Card], broken_hearts: bool) -> Card:
        sortedHand = self.sort_by_rank()
        hasQueenSpades = self.has_queen_spades()
        firstRound = False
        if not len(trick) == 0:
            if trick[0] == Card(Rank(2), Suit(0)):
                broken_hearts = True
                firstRound = True
        # Actions if you are the first player in trick
        if len(trick) == 0:
            # If you are the first player in round
            if Card(Rank.Two, Suit.Clubs) in self.hand:
                self.hand.remove(Card(Rank.Two, Suit.Clubs))
                return Card(Rank.Two, Suit.Clubs)
            elif not broken_hearts:
                for i in range(1, len(sortedHand)+1):
                    if self.check_valid_play(sortedHand[-i], trick, broken_hearts)[0]:
                        self.hand.remove(sortedHand[-i])
                        return sortedHand[-i]
            else:
                self.hand.remove(sortedHand[0])
                return sortedHand[0]

        # If you do not have the playing suit in your hand
        elif not self.check_if_suit_in_hand(trick[0].suit):
            for _ in self.hand:
                # If player has queen of spades and spades is not the leading suit, play it
                if hasQueenSpades[0] and not firstRound:
                    self.hand.remove(sortedHand[hasQueenSpades[1]])
                    return sortedHand[hasQueenSpades[1]]
                # else play card of highest value
                else:
                    for i in range(1, len(self.hand) + 1):
                        if self.check_valid_play(sortedHand[-i], trick, broken_hearts)[0]:
                            self.hand.remove(sortedHand[-i])
                            return sortedHand[-i]
        # If the trick suit is spades
        elif trick[0].suit == Suit.Spades:
            for j, i in enumerate(sortedHand):
                check = self.check_valid_play(i, trick, broken_hearts)
                if check[0]:
                    self.hand.remove(sortedHand[j])
                    return sortedHand[j]
        # If hearts aren't broken
        elif not broken_hearts:
            for i in range(0, -len(sortedHand), -1):
                check = self.check_valid_play(sortedHand[i], trick, broken_hearts)
                if check[0]:
                    self.hand.remove(sortedHand[i])
                    return sortedHand[i]
        else:
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
        suitList: list[list[Card]] = self.get_suitList()
        action = [False, 0]
        changeStrat = False
        for j, i in enumerate(suitList):
            if len(i) == 0:
                changeStrat = False
                action = [True, j]  # First is if empty, second is index
            elif len(i) <= 3:
                changeStrat = True
                if action[0]:
                    pass
                elif len(suitList[action[1]]) > len(i):
                    action = [False, j]

        if not changeStrat:
            sortedHand = self.sort_by_rank()
            returnList = []
            for i in range(-3, 0):
                self.hand.remove(sortedHand[i])
                returnList.append(sortedHand[i])
            return returnList
        else:
            sortedHand = self.sort_by_rank()
            returnList = []
            for i in suitList[action[1]]:
                returnList.append(i)
                self.hand.remove(i)
                sortedHand.remove(i)
            for i in range(-3 + len(suitList[action[1]]), 0):
                self.hand.remove(sortedHand[i])
                returnList.append(sortedHand[i])
        return returnList

    def check_suit_empty(self) -> list[bool, list[int]]:
        suitList: list[list[Card]] = self.get_suitList()
        returning = [False, []]
        indexList = []
        for j, i in suitList:
            if len(i) == 0:
                returning[0] = True
                indexList.append(j)
        returning[1] = indexList
        return returning

    def check_if_suit_in_hand(self, suit: Suit) -> bool:
        suitList: list[list[Card]] = self.get_suitList()
        for i in range(4):
            if suit == Suit(i) and len(suitList[i]) == 0:
                return False
        return True

    # Determines if you have queen of spades and gives an index in sorted list
    def has_queen_spades(self) -> list[bool, int]:
        returning = [False, -1]
        suitList = self.get_suitList()
        for i in suitList[2]:
            if i.rank == Rank.Queen:
                returning[0] = True
        if not returning[0]:
            return returning
        else:
            rankList = self.sort_by_rank()
            index = rankList.index(Card(Rank.Queen, Suit.Spades))
            return [True, index]



if __name__ == "__main__":
    """
    Test cases:
    [Four of Spades, Nine of Spades, Ace of Spades, Six of Clubs, Seven of Clubs, Queen of Clubs, 
    Three of Hearts, Ten of Hearts, King of Hearts, Six of Diamonds, Eight of Diamonds, Ace of Diamonds]
    Broken Hearts = False
    Trick = []
    
    """
    """
    player = BetterAIPlayer("Angus")
    player.hand = [Card(Rank(6), Suit(0)), Card(Rank(5), Suit(2)), Card(Rank(3), Suit(1)), 
                   Card(Rank(3), Suit(0)), Card(Rank(14), Suit(1)),
                   Card(Rank(3), Suit(1)), Card(Rank(5), Suit(3)),
                   Card(Rank(9), Suit(1)), Card(Rank(14), Suit(3)), Card(Rank(4), Suit(2)),
                   Card(Rank(13), Suit(2)), Card(Rank(2), Suit(3)), Card(Rank(3), Suit(3))
                   ]
    trick = [Card(Rank(2), Suit(0)), Card(Rank(10), Suit(0))]
    brokenHearts = False
    print(player.hand)
    print(player.play_card(trick, brokenHearts))
    
    import random
    """
    """
    for _ in range(1000000):
        deck = []
        for i in range(2,15):
            for j in range(4):
                deck.append(Card(Rank(i), Suit(j)))
        trick = [Card(Rank(2), Suit(0))]
        deck.remove(Card(Rank(2), Suit(0)))
        for _ in range(0, random.randint(0,2)):
            indexToAdd = random.randint(0, len(deck)-1)
            trick.append(deck[indexToAdd])
            deck.remove(deck[indexToAdd])
        player = BasicAIPlayer("Angus")
        player.hand = []
        for _ in range(0, len(deck)//3):
            indexToAdd = random.randint(0, len(deck)-1)
            player.hand.append(deck[indexToAdd])
            deck.remove(deck[indexToAdd])
        brokenHearts = False

        print(player.hand)
        print(f"Broken Hearts = {brokenHearts}")
        print(f"Trick = {trick}")
        try:
            answer = player.play_card(trick, brokenHearts)
            if not isinstance(answer, Card):
                raise ValueError
            if not player.check_valid_play(answer, trick, brokenHearts)[0]:
                raise ValueError
            print(answer)
        except ValueError:
            print("Stopped on problem!")
            break
        except Exception:
            print("Internal problem!")
            break
"""
"""
    for _ in range(1000000):
        deck = []
        for i in range(2,15):
            for j in range(4):
                deck.append(Card(Rank(i), Suit(j)))
        trick = []
        deck.remove(Card(Rank(2), Suit(0)))
        for _ in range(0, random.randint(0,3)):
            indexToAdd = random.randint(0, len(deck)-1)
            trick.append(deck[indexToAdd])
            deck.remove(deck[indexToAdd])
        player = BasicAIPlayer("Angus")
        player.hand = []
        for _ in range(0, len(deck)//3):
            indexToAdd = random.randint(0, len(deck)-1)
            player.hand.append(deck[indexToAdd])
            deck.remove(deck[indexToAdd])
        if random.randint(0,1) == 0:
            brokenHearts = False
        else:
            brokenHearts = True

        print(player.hand)
        print(f"Broken Hearts = {brokenHearts}")
        print(f"Trick = {trick}")
        try:
            answer = player.play_card(trick, brokenHearts)
            if not isinstance(answer, Card):
                raise ValueError
            if not player.check_valid_play(answer, trick, brokenHearts)[0]:
                raise ValueError
            print(answer)
        except ValueError:
            print("Stopped on problem!")
            break
        except Exception:
            print("Internal problem!")
            break
"""