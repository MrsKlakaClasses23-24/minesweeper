from enum import Enum

# Enum to represent the three states of the game
# ACTIVE - Game is in progress
# WON - Game is over and user won
# LOST - Game is over and user lost
class GameStatus(Enum):
    ACTIVE = 1
    WON = 2
    LOST = 3