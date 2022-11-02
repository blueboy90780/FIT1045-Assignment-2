# Written by Angus Corr 
# Last Updated 18/09/2022
# Also written by Sarah Jasper, updated 25/09/2022

from cards import Card, Rank, Suit
import copy

class Player:

	CARD_ART = {
			2: ["┌─────┐", "│2    │", "│     │", "│    2│", "└─────┘"],
			3: ["┌─────┐", "│3    │", "│     │", "│    3│", "└─────┘"],
			4: ["┌─────┐", "│4    │", "│     │", "│    4│", "└─────┘"],
			5: ["┌─────┐", "│5    │", "│     │", "│    5│", "└─────┘"],
			6: ["┌─────┐", "│6    │", "│     │", "│    6│", "└─────┘"],
			7: ["┌─────┐", "│7    │", "│     │", "│    7│", "└─────┘"],
			8: ["┌─────┐", "│8    │", "│     │", "│    8│", "└─────┘"],
			9: ["┌─────┐", "│9    │", "│     │", "│    9│", "└─────┘"],
			10: ["┌─────┐", "│10    │", "│     │", "│    10│", "└─────┘"],
			11: ["┌─────┐", "│J    │", "│     │", "│    J│", "└─────┘"],
			12: ["┌─────┐", "│Q    │", "│     │", "│    Q│", "└─────┘"],
			13: ["┌─────┐", "│K    │", "│     │", "│    K│", "└─────┘"],
			14: ["┌─────┐", "│A    │", "│     │", "│    A│", "└─────┘"]
			}#this creates the look of the card


	def __init__(self, name: str) -> None:
		self.hand : list[Card] = []
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

	# sorting cards in hand from lowest ranking to highest ranking
	def sort_hand_by_value(self) -> list[Card]:
		# Modified by David
		sorted_hand = sorted(copy.deepcopy(self.hand))
		return sorted_hand

	def sort_by_rank(self) -> list(Card):
		# Modified by David
		sorted_hand = sorted(copy.deepcopy(self.hand))
		return sorted_hand




	# Returns a List of Lists, with each list containing cards of a certain suit.
	# Similar to sort_by_suit but instead of returning one list it returns a list of lists
	def get_suitList(self) -> list(list(Card)):
		suitList = [[],[],[],[]]
		for i in range(4):
			for j in self.hand:
				if j.suit == Suit(i):
					suitList[i].append(j)
		save = self.hand
		for j,i in enumerate(suitList):
			self.hand = i
			self.sort_hand_by_value()
			suitList[j] = self.hand
		self.hand = save
		return suitList


	# Updates total score at conclusion of round
	def update_total_score(self) -> None:
		self.total_score += self.round_score
		self.round_score = 0
	
	def show_card(self):
		i = self.rank
		if self.suit == 0:
			Player.CARD_ART[i][2] = "│  ♣  │" #card is a club
		elif self.suit == 1:
			Player.CARD_ART[i][2] = "│  ♦  │" #card is a diamond
		elif self.suit == 2:
			Player.CARD_ART[i][2] = "│  ♠  │" #card is a spade
		else:
			Player.CARD_ART[i][2] = "│  ♥  │" #card is a heart
		
		display_card_art = "{0}\n{1}\n{2}\n{3}\n{4}\n".format(
			Player.CARD_ART[i][0],
			Player.CARD_ART[i][1],
			Player.CARD_ART[i][2],
			Player.CARD_ART[i][3],
			Player.CARD_ART[i][4]
			) #this ensures that the card is lined up correctly
		return display_card_art

	def show_hand(self, hand):
		#Variable declaration: empty lists so that card art can be properly formatted
		top_brackets = [] 
		second_row = []
		suit_row = []
		fourth_row = []
		bottom_brackets = []
		indicie_row = []
		i=0
		while i <= len(hand):
			top_brackets.append ("┌─────┐") #adds top brackets of cards as needed
			i+=1
		i=0
		while i <= len(hand):
			if hand[i].rank == Rank.Two:
				second_row.append ("│2    │") #each of these adds each number as needed to each row of the hand display
				fourth_row.apppend ("│    2│")
				i+=1
			elif hand[i].rank == Rank.Three:
				second_row.append ("│3    │")
				fourth_row.apppend ("│    3│")
				i+=1
			elif hand[i].rank == Rank.Four:
				second_row.append ("│4    │")
				fourth_row.apppend ("│    4│")
				i+=1
			elif hand[i].rank == Rank.Five:
				second_row.append ("│5    │")
				fourth_row.apppend ("│    5│")
				i+=1			
			elif hand[i].rank == Rank.Six:
				second_row.append ("│6    │")
				fourth_row.apppend ("│    6│")
				i+=1
			elif hand[i].rank == Rank.Seven:
				second_row.append ("│7    │")
				fourth_row.apppend ("│    7│")
				i+=1
			elif hand[i].rank == Rank.Eight:
				second_row.append ("│8    │")
				fourth_row.apppend ("│    8│")
				i+=1
			elif hand[i].rank == Rank.Nine:
				second_row.append ("│9    │")
				fourth_row.apppend ("│    9│")
				i+=1
			elif hand[i].rank == Rank.Ten:
				second_row.append ("│10   │")
				fourth_row.apppend ("│   10│")
				i+=1
			elif hand[i].rank == Rank.Jack:
				second_row.append ("│J    │")
				fourth_row.apppend ("│    J│")
				i+=1
			elif hand[i].rank == Rank.Queen:
				second_row.append ("│Q    │")
				fourth_row.apppend ("│    Q│")
				i+=1
			elif hand[i].rank == Rank.King:
				second_row.append ("│K    │")
				fourth_row.apppend ("│    K│")
				i+=1
			else:
				second_row.append ("│A    │")
				fourth_row.apppend ("│    A│")
				i+=1
		i=0
		while i <= len(hand):
			if hand[i].rank == Suit.Clubs:
				suit_row.append ("│  ♣  │") #these add the suit onto the card display of your hand
				i+=1
			elif hand[i].rank == Suit.Diamonds:
				suit_row.append ("│  ♦  │")
				i+=1
			elif hand[i].rank == Suit.Spades:
				suit_row.append ("│  ♠  │")
				i+=1
			else: #must be a heart
				suit_row.append ("│  ♥  │")
				i+=1
		i=0
		while i <= len(hand):
			bottom_brackets.append ("└─────┘")
			i+=1
		i=0
		while i <= len(hand):
			indicie_row.append (" ")
			indicie_row.append (i)
			indicie_row.append (" ")

		hand_display= "{0}\n{1}\n{2}\n{3}\n{4}\{5}\n".format(
			top_brackets,
			second_row,
			suit_row,
			fourth_row,
			bottom_brackets,
			indicie_row
		) #this ensures that the hand is displayed with cards alongside each other
		return hand_display
		


	def print_card(self, card : Card) -> None:
		print(self.show_card(card.rank, card.suit))
