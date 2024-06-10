import pygame
from controls.button import Button
from controls.mine_field import Minefield
from controls.title import Title
from game_status import GameStatus
from mine_sweeper import Minesweeper, MoveResult
from mine_sweeper_ai import MinesweeperAI

class GameWindow():
    ROWS = 16
    COLS = 16
    MINES = 40
    HEIGHT = 600
    WIDTH = 800

    def __init__(self) -> None:
        self.sprites = pygame.sprite.LayeredUpdates()
        self.screen = pygame.display.set_mode((GameWindow.WIDTH, GameWindow.HEIGHT))
        pygame.display.set_caption("Minesweeper AI")
        
        # Add UI elements
        self.sprites.add(Button(610, 25, 175, 50, "Restart", self.restart_game))
        self.dead_text = Title(610, 100, 175, 50, "", None)
        self.sprites.add(Title(610, 200, 175, 50, "AI Options", None))
        self.sprites.add(Button(610, 275, 175, 50, "Make Move", self.ai_click_handler))
        self.sprites.add(Button(610, 350, 175, 50, "Show Known Mines", self.show_ai_knowledge))
        self.sprites.add(self.dead_text)
        self.restart_game()

    # draw both the mine field and the buttons
    def draw(self) -> None:
        dirty = self.mine_field.cell_sprites.draw(self.screen)
        pygame.display.update(dirty)

        dirty = self.sprites.draw(self.screen)
        pygame.display.update(dirty)
        

    def update(self, event) ->None:
        self.sprites.update(event)
        self.mine_field.update(event)
      
    def click_hander(self, i: int , j: int) -> MoveResult:
        if self.game_state == GameStatus.ACTIVE:
            result =  self.minesweeper.reveal_cell((i,j))
            self.game_state = result.status
            if result.status == GameStatus.LOST:
                self.dead_text.update_text("You Lost")
            elif result.status == GameStatus.ACTIVE:
                if self.dead_text.text != "":
                    self.dead_text.update_text("")
                for k, a in result.updates.items():
                    self.ai.add_knowledge(k, int(a))
            return result
        return None
    
    def ai_click_handler(self) -> None:
        if self.game_state == GameStatus.ACTIVE:
            move = self.ai.get_safe_move()
            if move is None:
                self.dead_text.update_text("No safe moves")  
                return
 
            ac= self.minesweeper.reveal_cell(move)
            self.game_state = ac.status
            if ac.status == GameStatus.LOST:
                self.dead_text.update_text("You Lost")
            else:
                if self.dead_text.text != "":
                    self.dead_text.update_text("")                
                self.mine_field.update_cells(ac.updates)

                for k, a in ac.updates.items():
                    self.ai.add_knowledge(k, int(a))

    def show_ai_knowledge(self)-> None:

        mine_locations = {}
        for mine in self.ai.known_mine_cells:
            result = self.minesweeper.flag_possible_mine(mine)
            if result.status == GameStatus.WON:
                self.dead_text.update_text("You Won!")        
            for key,value in result.updates.items():
                mine_locations[key] = value
        
        if len(mine_locations) > 0:
            self.mine_field.update_cells(mine_locations)

    def restart_game(self)-> None:
        self.minesweeper = Minesweeper(GameWindow.ROWS, GameWindow.COLS, GameWindow.MINES)
        self.mine_field = Minefield(GameWindow.HEIGHT, 
                                    GameWindow.WIDTH, 
                                    GameWindow.ROWS, 
                                    GameWindow.COLS, 
                                    self.click_hander)
        self.ai = MinesweeperAI(GameWindow.ROWS, GameWindow.COLS)
        self.dead_text.update_text("")
        self.game_state = GameStatus.ACTIVE