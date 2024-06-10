from unittest import TestCase
import json
from game_status import GameStatus
from mine_sweeper import Minesweeper
from mine_sweeper_ai import MinesweeperAI

class AITests(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_basic_case(self) -> None:
        minesweeper = Minesweeper(4, 4, 3, [[False, False, True, False],
                                            [False, False, False, True],
                                            [False, False, False, False],
                                            [False, True, False, False]])
        ai = MinesweeperAI(4, 4)

        result = minesweeper.reveal_cell((1, 2))
        for cell, mine_count in result.updates.items():
            ai.add_knowledge(cell, int(mine_count))
        result = minesweeper.reveal_cell((0, 3))
        for cell, mine_count in result.updates.items():
            ai.add_knowledge(cell, int(mine_count))
        self.assertEqual(2, len(ai.known_mine_cells))
        self.assertEqual(7, len(ai.known_safe_cells))
        self.assertIn((0, 2), ai.known_mine_cells)
        self.assertIn((1, 3), ai.known_mine_cells)
        self.assertIn((0, 1), ai.known_safe_cells)
        self.assertIn((1, 1), ai.known_safe_cells)
        self.assertIn((2, 1), ai.known_safe_cells)
        self.assertIn((2, 2), ai.known_safe_cells)
        self.assertIn((2, 3), ai.known_safe_cells)
        self.assertIn((1, 2), ai.known_safe_cells)
        self.assertIn((0, 3), ai.known_safe_cells)

    def test_complete_game(self) -> None:

        with open("./tests/board.json", "r", encoding="utf-8") as file_data:
            board = json.loads(file_data.read())
        with open("./tests/moves.json", "r", encoding="utf-8") as file_data:
            moves = json.loads(file_data.read())

        minesweeper = Minesweeper(16, 16, 40, board)
        ai = MinesweeperAI(16, 16)

        for move, is_ai in moves:
            if is_ai:
                self.assertTrue(ai.is_safe_move(tuple(move))) 
            result = minesweeper.reveal_cell(tuple(move))
            for cell, mine_count in result.updates.items():
                ai.add_knowledge(cell, int(mine_count))
        
        for mine in ai.known_mine_cells:
            minesweeper.flag_possible_mine(mine) 
        self.assertEqual(minesweeper._game_status, GameStatus.WON)
