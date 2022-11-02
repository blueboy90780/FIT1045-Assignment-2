# Written by Angus Corr
# Last Updated 18/09/2022

from player import Player
from cards import Card, Rank, Suit
from time import sleep

class Round:

	# Players will have their cards in their class
	def __init__(self, playerList : list[Player]) -> None:
		self.players = playerList
		self.gameSize = len(playerList)
		self.leaderIndex = self.get_first_leader()
		roundComplete = False
		self.brokenHearts = False
		self.shootMoonIndex = None

		while not roundComplete:

			self.leaderIndex = self.run_trick(self.leaderIndex)
			roundComplete = self.check_complete()

		# Checking for shooting the moon
		try:
			self.shootMoonIndex = self.shoot_moon_check()
		except ValueError:
			pass

		else:
			for j, i in enumerate(self.players):
				if j == self.shootMoonIndex:
					i.round_score = 0
				else:
					i.round_score = 26
		self.end_of_round_stats()


	# returns index in playerList corresponding to the first player in a trick, previousLeader is an integer index
	def get_first_leader(self) -> int:
		for i in range(len(self.players)):
			for j in self.players[i].hand:
				if j == Card(Rank.Two, Suit.Clubs):
					return i


	
	# Gets the index of the next player
	def get_next_player(self, previous) -> int:
		if previous == self.gameSize-1:
			return 0
		else:
			return previous + 1

	# checking if round is complete
	def check_complete(self) -> bool:
		cardsLeft = 0
		# Running through each player checking how many cards are left
		for i in self.players:
			cardsLeft += len(i.hand)

		if cardsLeft == 0:
			return True
		else:
			return False

	# Runs through one trick
	def run_trick(self, leaderIndex):
		playerNumber = 0
		playerIndex = leaderIndex
		trick : list[Card] = []
		bestPlayer = playerIndex
		# Loops through the players starting at leaderIndex
		while playerNumber < self.gameSize:
			# Below is logic for if valid plays are not implemented in basic_ai

			# Get the card that the player is playing and prints
			playCard = self.players[playerIndex].play_card(trick, self.brokenHearts)
			if playerNumber == 0:
				print(f"{self.players[playerIndex].name} leads with \n{playCard}")
				sleep(0.7)
			else:
				print(f"{self.players[playerIndex].name} plays \n{playCard}")
				sleep(0.7)
			
			# Checks if hearts is broked
			if (not self.brokenHearts) and (playCard.suit == Suit.Hearts or playCard == Card(Rank.Queen, Suit.Spades)):
				print("Hearts have been broken!")
				self.brokenHearts = True

			# Updates the best player
			if len(trick) == 0:
				bestPlayer = playerIndex
				bestCard = playCard
			elif playCard.suit == trick[0].suit:
				if bestCard < playCard:
					bestCard = playCard
					bestPlayer = playerIndex
			# Adds the card to the trick
			trick.append(playCard)
			# Gets the next player
			playerIndex = self.get_next_player(playerIndex)
			playerNumber += 1
		# Calculating the trick score and printing results
		trickScore = self.get_score(trick)
		print(f"{self.players[bestPlayer].name} takes the trick. Points received: {trickScore}")
		self.players[bestPlayer].round_score += trickScore # Adding trick score to player score
		return bestPlayer
		
	def get_score(self, trick:list[Card]):
		trickScore = 0
		for i in trick:
			if i.suit == Suit.Hearts:
				trickScore += 1
			elif i.suit == Suit.Spades and i.rank == Rank.Queen:
				trickScore += 13
		return trickScore

	# returns an integer of the player if they have shot the moon
	def shoot_moon_check(self) -> int:
		for j, i in enumerate(self.players):
			if i.round_score == 26:
				return j
		raise ValueError

	def end_of_round_stats(self):
		for player in self.players:
			player.update_total_score()