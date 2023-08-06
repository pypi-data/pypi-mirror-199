""" Game module """

import players
from players import Player
import random


# TODO: Create is_valid method for Player class to check if the move is valid
# TODO: Add an extra move for the players


class Game:
    """Game class"""

    def __init__(self, player1: players.Player, player2: players.Player) -> None:
        """Initialize a new game"""
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.coin_toss()
        self.opponent = self.player1 if self.current_player == self.player2 else self.player2
        self.winner = None

    def coin_toss(self) -> players.Player:
        """Randomly select who goes first"""
        return random.choice([self.player1, self.player2])

    def is_over(self) -> bool:
        """Check if the game is over"""
        return self.player1.is_both_empty() or self.player2.is_both_empty()

    def get_winner(self) -> None:
        """Get the winner of the game"""
        if self.player1.is_both_empty():
            self.winner = self.player2.name
        elif self.player2.is_both_empty():
            self.winner = self.player1.name

    def valid_input(self, hand: str) -> bool:
        """Check if the hand is valid"""
        if hand != "L" and hand != "R":
            return False
        return True

    def switch_players(self) -> None:
        """Switch players"""
        self.current_player, self.opponent = self.opponent, self.current_player

    def prompt_dialog(self, which_dialog: str) -> None:
        """Print the dialog of the game"""
        LINE = "-" * 80
        if which_dialog == "start":
            print(LINE + f"\n{self.current_player.name} goes first!")

        elif which_dialog == "turn":
            line_1 = f"\n{self.current_player.name} it's your turn!"
            line_2 = f"\nYour current hand is: {self.current_player.current_hand()}"
            line_3 = f"\n{self.opponent.name}'s hand is: {self.opponent.current_hand()}\n"
            dialog = LINE + line_1 + line_2 + line_3
            print(dialog)

        elif which_dialog == "over":
            self.get_winner()

            line_1 = "\nGame over!" + f"\n{self.winner} wins!\n"
            line_2 = "\nFinal Hands: "
            line_3 = f"\n{self.player1.name}: {self.player1.current_hand()}"
            line_4 = f"\n{self.player2.name}: {self.player2.current_hand()}\n"

            dialog = LINE.replace("-", "*") + line_1 + line_2 + line_3 + line_4 + LINE.replace("-", "*")
            print(dialog)

    def play(self) -> None:
        """Play the game"""

        # Print the start dialog
        self.prompt_dialog("start")

        # Play the game
        while True:
            # Print the dialog of the game
            self.prompt_dialog("turn")

            # Get the current player's move
            while True:
                which_hand = input("Which hand? (L/R): ").strip().upper()
                if not self.valid_input(which_hand):
                    print("Invalid input!\nPlease type \"R\" or \"L\"")
                elif self.current_player.is_empty(which_hand):
                    print("Hand is empty!\nPlease try again.")
                else:
                    if which_hand == "L":
                        value = self.current_player.left
                    else:
                        value = self.current_player.right
                    break

            # Get the opponent's move
            while True:
                opponent_hand = input("Which opponent's hand? (L/R): ").strip().upper()
                if not self.valid_input(opponent_hand):
                    print("Invalid input!\nPlease type \"R\" or \"L\"")
                elif self.opponent.is_empty(opponent_hand):
                    print("Opponent's hand is empty!\nPlease try again.")
                else:
                    self.opponent.update(opponent_hand, value)
                    break

            # Check if the game is over
            if self.is_over():
                self.prompt_dialog("over")
                break

            # Switch players
            self.switch_players()


if __name__ == "__main__":
    player_1 = Player(input("Player 1 name: ").strip())
    player_2 = Player(input("Player 2 name: ").strip())
    stixx_game = Game(player_1, player_2)
    stixx_game.play()
