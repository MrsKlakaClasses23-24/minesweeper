from collections import deque
from typing import Dict, List, Set, Tuple
import random
from game_status import GameStatus

# Represents the result of a move.  Status will tell if the the game is still
# being played or over.  Updates are an update of what cells are now visible 
class MoveResult():
    def __init__(self, 
                 status: GameStatus, 
                 cell_updates: Dict[Tuple[int, int], str]) -> None:
        self.status = status
        self.updates = cell_updates

# Core game logic for minesweeper
class Minesweeper():

    FLAG = "FLAG"
    MINE = "MINE"

    # for testing purposes, an intial board can be passed in
    def __init__(self, 
                 height, 
                 width,
                 mine_count,
                 initial_board: List[List[bool]] = None):

        self._height = height
        self._width = width
        self._mine_count = mine_count
        self._mine_locations = set()
        self._mines_flaged = set()
        self._game_status = GameStatus.ACTIVE

        # offsets to look at the surrounding cells
        self._surrounding_offsets = [       
                    (-1,-1),
                    (-1,0),
                    (-1,1),
                    (0,-1),
                    (0,1),
                    (1,-1),
                    (1,0),
                    (1,1)]

        # create a new board
        if initial_board is None:

            # set default build to False meaning no mines
            self._board: List[List[bool]] = []
            for _ in range(self._height):
                row = []
                for _ in range(self._width):
                    row.append(False)
                self._board.append(row)

            # randomly place mines            
            while len(self._mine_locations) < self._mine_count:
                (i,j) = random.randrange(self._height), random.randrange(self._width)
                if (i,j) not in self._mine_locations:
                    self._board[i][j] = True
                    self._mine_locations.add((i,j))

        else:
            # validate input
            if (self._height != len(initial_board) or 
                self._width != len(initial_board[0])):
                raise ValueError("Height or width does not match input")
            
            # get mintes
            self._board = initial_board
            for i in range(self._height):
                for j in range(self._width):
                    if self._board[i][j]:
                          self._mine_locations.add((i,j))

            # validate mine count
            if self._mine_count != len(self._mine_locations):
                raise ValueError("Incorrect mine count")

    # Marks a mine in the game as flagged
    def flag_possible_mine(self, cell: Tuple[int, int]) -> MoveResult:
        self._mines_flaged.add(cell)
        if self._mines_flaged == self._mine_locations:
            self._game_status = GameStatus.WON
        return MoveResult(self._game_status, {cell: Minesweeper.FLAG})
        

    # Reveals a cell in Minesweeper.  Will return a MoveResult showing
    # status of the game as well all of the updates to known information. If 
    # we uncover a place with 0 nearby mines, we will open up all blank cells
    def reveal_cell(self, cell: Tuple[int, int]) -> MoveResult: 
        updates = {}

        # if we hit a mine, we lost
        if cell in self._mine_locations:
            for mine in self._mine_locations:
                    updates[mine] = Minesweeper.MINE
            return MoveResult(GameStatus.LOST, updates)
        
        # if there are no mines nearby, add all empty cells that are next to 
        # the empty cell to a queue and go until we have no neighbor cells that
        # have 0 neighboring mines. 
        items_explored = set()
        queue = deque()
        queue.append(cell)
        while len(queue) > 0:
            item = queue.popleft()
            items_explored.add(item)
            nearby = self._get_nearyby_mine_count(item)
            updates[item] = str(nearby)
            if nearby == 0:
                neighbors = self._get_neighboring_cells(item)
                for neighbor in neighbors:
                    if neighbor not in items_explored:
                        queue.append(neighbor)


        return MoveResult(GameStatus.WON if len(self._mines_flaged) == self._mine_count else GameStatus.ACTIVE, updates)

    # returns the neighboring cells of a given cell
    def _get_neighboring_cells(self, cell: Tuple[int, int]) -> Set[Tuple[int, int]]:
        cells = set()
        for offset in self._surrounding_offsets:
            (i,j) = cell[0] + offset[0], cell[1] + offset[1]
            if (0 <= i < self._height and
                    0 <= j < self._width):
                cells.add((i,j))
        return cells

    # returns the count of mines in the neighboring cells.
    def _get_nearyby_mine_count(self, cell: Tuple[int, int]) -> int:
        mine_count = 0
        for offset in self._surrounding_offsets:
            (i,j) = cell[0] + offset[0], cell[1] + offset[1]
            if (0 <= i < self._height and
                    0 <= j < self._width and
                    self._board[i][j]):
                mine_count += 1
        return mine_count