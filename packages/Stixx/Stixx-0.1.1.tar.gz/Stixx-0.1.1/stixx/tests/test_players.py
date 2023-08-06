import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))
from players import Player


class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.player = Player("test_player")
        self.player2 = Player("test_player2")

    def test_player_name(self) -> None:
        self.assertEqual(self.player.name, "test_player")
        self.assertEqual(self.player2.name, "test_player2")

    def test_player_score(self) -> None:
        self.assertEqual(self.player.left, 1)
        self.assertEqual(self.player.right, 1)

    def test_current_hand(self) -> None:
        assert self.player.current_hand() == f"{self.player.left} {self.player.right}"

    def test_update_score(self) -> None:
        self.player.update("L", 2)
        self.assertEqual(self.player.left, 3)

        self.player.update("R", 4)
        self.assertEqual(self.player.right, 0)

    def test_is_both_empty(self) -> None:
        self.player.update("L", 3)
        self.player.update("R", 2)
        self.assertFalse(self.player.is_both_empty())

        self.player.update("L", 1)
        self.player.right = 0
        self.assertTrue(self.player.is_both_empty())

    def test_is_empty(self) -> None:
        self.player.update("L", 3)
        self.assertFalse(self.player.is_empty("L"))

        self.player.update("L", 1)
        self.assertTrue(self.player.is_empty("L"))

        self.player.update("R", 3)
        self.assertFalse(self.player.is_empty("R"))

        self.player.update("R", 1)
        self.assertTrue(self.player.is_empty("R"))
