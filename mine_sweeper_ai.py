from typing import List, Set, Tuple

# The KnowledgeSentence class represents knowledge that is aquired while 
# playing the game. Knowledge is represented by a set of tuples representing
# the cells and the count of mines in that set. For example, cells 
# {(1,2), (1,3)} and a count of 1 means that either (1,2) or (1,3) is a mine.
class KnowledgeSentence():

    def __init__(self, cells:Set[Tuple[int, int]], mine_count: int) -> None:
        self.cells: Set = set(cells)
        self.mine_count:int = mine_count
        self.known_mine_cells: Set[Tuple[int, int]] = set()
        self.known_safe_cells: Set[Tuple[int, int]] = set()

    def __eq__(self, other: "KnowledgeSentence"):
        return self.cells == other.cells and self.mine_count == other.mine_count

    # TODO: Implement "mark_mine"
    # **********************************
    # Updates this knowledge sentence with the fact that the given cell is a mine. If the cell is in 
    # this knowledge set, mark it as a mine and decrease mine_count by 1 
    # cell: Coordinates of the cell that should be marked as a mine
    def mark_mine(self, cell: Tuple[int, int]):
        raise NotImplementedError

    # TODO: Implement "mark_safe"
    # **********************************
    # Updates this knowledge sentence with the fact that the cell is safe and not a mine.
    # If the cell is in this knowledge set, mark it as safe 
    # cell: Coordinates of the cell that should be marked as a mine
    def mark_safe(self, cell: Tuple[int, int]):
        raise NotImplementedError

# Main AI that adds knowledge to the knowledge base as well as tries to find
# any new knowledge that can be found
class MinesweeperAI():

    def __init__(self, height: int, width: int)-> None:
        #dimensions of the board
        self.height:int = height 
        self.width:int = width

        self.known_mine_cells:Set[Tuple[int,int]] = set() # set of cells that are mines
        self.known_safe_cells:Set[Tuple[int,int]] = set() # set of cells that are safe
        self.moves_made:Set[Tuple[int,int]] = set() # set of cells that have been clicked

        # List of sentences about the game known to be true
        self.knowledge_base: List[KnowledgeSentence] = []

        # create a set of all possible cells
        self.all_cells = set()
        for i in range(self.height):
            for j in range(self.width):
                self.all_cells.add((i,j))

        self.surrounding_offsets = [       
                    (-1,-1),
                    (-1,0),
                    (-1,1),
                    (0,-1),
                    (0,1),
                    (1,-1),
                    (1,0),
                    (1,1)]

    # Helper Function: _calculate_neighbor_cells_and_count (do not modify)
    # ************************************************
    # Returns a set of cell tuples that surround the given cell that are not already
    # known to be a mine or a safe cell     
    def _calculate_neighbor_cells_and_count(self, cell: Tuple[int, int], mine_count:int )->Tuple[Set[Tuple[int,int]], int]:
        cells = set()

        # Look at all of the neighboring cells
        for offset in self.surrounding_offsets:
            (i,j) = cell[0] + offset[0], cell[1] + offset[1]
 
            # Ensure that the cell is in bounds and not already a known safe cell
            if (0 <= i < self.height and
                    0 <= j < self.width and
                    (i,j) not in self.known_safe_cells):
                
                # At this point there are two options.  
                # 1.  It is not a known mine.  Add it to out list of possible mines
                # 2.  It is a known mine, so subtract 1 from the mine count
                if (i,j) not in self.known_mine_cells:
                    cells.add((i,j))
                else:
                    mine_count -= 1

        return (cells, mine_count)
    
    # mark_mine (do not modify)
    # **************************
    # Adds the given cell to the set of known mines and marks it as a mine on all knowledge
    # sentences in the game.
    def mark_mine(self, cell: Tuple[int, int])-> None:
        self.known_mine_cells.add(cell)
        for sentence in self.knowledge_base:
            sentence.mark_mine(cell)

    # mark_safe (do not modify)
    # **************************
    # Adds the given cell to the set of known safe cells and marks it as safe on all knowledge
    # sentences in the game.
    def mark_safe(self, cell: Tuple[int, int])-> None:
        self.known_safe_cells.add(cell)
        for sentence in self.knowledge_base:
            sentence.mark_safe(cell)

    # TODO: Implement add_knowledge
    # ********************************** 
    # Called everytime a cell is revealed to be safe. The game will pass in
    # a tuple for the safe cell and how many mines are around it. This method will update the
    # appropriate instance variables for this object and creates a new knowledge sentence to 
    # reflect what we know about the cells surrounding the safe cell. It then infers new 
    # knowledge (i.e. updates all knowledge sentences to not include the safe cell) by 
    # marking the cell as safe and iterating through all knowledge sentences to check if we know
    # of any new mines or safe cells. It will then find the difference between knowledge 
    # sentences that are subsets of other sentences to build new sentences until there are no more
    # changes.
    def add_knowledge(self, safe_cell: Tuple[int, int], mine_count: int)-> None:
        # 1) Mark the incoming cell as safe
        self.mark_safe(safe_cell)

        # 2) Add the cell to the set of moves that have been made
        self.moves_made.add(safe_cell)

        # 3) Add new knowledge to our knowledge base
        # a) Use _calculate_neighbor_cells_and_count to get a set of cells and create a new KnowledgeSentence object
        neighbor_cells, count = self._calculate_neighbor_cells_and_count(safe_cell, len(self.known
        knowledge_sentence = KnowledgeSentence(neighbor_cells, count)

        # b) Add the knowledge sentence to self.knowledge_base
        self.knowledge_base.append(knowledge_sentence)

        # 4) Infer new knowledge, now that we have included our new sentence in our knowledge base
        # We need to do this repeatedly until no knew knowledge is created
        changes = True # flag to indicate when we infer new knowledge
        while (changes):
            changes = False

            # for each knowledge sentence:

                # a) if the mine count equals the number of cells, mark all of those cells as a known mine
                # and set the changes flag to True
                # NOTE: you will need to create a copy of the set of cells in the knowledge sentence to iterate 
                # through, since marking mine cells will remove those cells from that set. 
                # NOTE: Equality for knowledge senteces are based on cells in it, so empty sentences can cause 
                # inifinte loops if you are not careful
                if mine_count == len(self.all_cells):
                    for cell in neighbor_cells:
                        self.known_mine_cells.add(cell)
                        changes = True

                # b) if the count is 0, mark all of those mines as safe and set the changes flag to True
                # NOTE: you will need to create a copy of the set of cells in the knowledge sentence to iterate 
                # through, since marking safe cells will remove those cells from that set.
                # NOTE: Equality for knowledge senteces are based on cells in it, so empty sentences can cause 
                # inifinte loops if you are not careful
                if mine_count == 0:
                    cells = neighbor_cells
                    for cell in cells:
                        self.mark_safe(cell)
                        changes = True
                # c) Compare each knowledge sentence against each other sentence. if sentence1 is a 
                # subset of sentence2, add a new sentence that takes the difference sentence2-sentence1 for both
                # cells and mine_count and and set the changes flag to True.  Then break out of the inner loop 
                for sentence_1 in self.knowledge_base:
                    cells_1 = sentence_1.known_mine_cells
                    for sentence_2 in self.knowledge_baase:
                        cells_2 = sentence_2.known_mine_cells
                        if cells_1 in cells_2:
                            self.knowledge_base.append(KnowledgeSentence(cells_2-cells_1, len(cells_2)-1))
                            changes = True
                            break


    # TODO: Implement get_safe_move
    # *************************************
    # This function will see if there is a possible safe move.  If there is it will return
    # that safe cell, if there is not, it will return None.
    def get_safe_move(self) -> Tuple[int, int]:
        if len(self.known_safe_cells) > 0:
            return self.known_safe_cells[0]
        else:
            return None
    

    # TODO: Implement is_safe_move
    # *************************************
    # This function will see if the current cell is a safe move.  If there is it will return
    # True, otherwise it will return False.
    def is_safe_move(self, cell: Tuple[int, int]) -> bool:
        if cell in self.known_mine_cells:
            return False
        else:
            return True
