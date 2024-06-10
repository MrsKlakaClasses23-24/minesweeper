import pygame
from windows.game_window import GameWindow

# Simple game class for running the PyGame
class MinesweeperGame():
    def __init__(self) -> None:
        pygame.init()
        self.current_window:GameWindow = GameWindow()
        self.running = True
        self.clock = pygame.time.Clock()

    # main loop that will run intil game is exited
    def start(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # send events to the current window 
                self.current_window.update(event)
            
            # redraw the windows
            self.current_window.draw()  
            self.clock.tick(60)

    def quit(self) -> None:
        pygame.quit()

game = MinesweeperGame()
game.start()
game.quit()