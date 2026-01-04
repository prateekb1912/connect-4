from dataclasses import dataclass
from enum import Enum


MAX_CONSECUTIVES = 4

class GameState(str, Enum):
    IN_PROGRESS = "In Progress"
    WON = "Won"
    DRAW = "Draw"

class DiscColor(str, Enum):
    RED = 1
    BLUE = 2

@dataclass
class Player:
    color: DiscColor

class Game:
    def __init__(self, player1: "Player", player2: "Player", board: "Board"):
        self.player1 = player1
        self.player2 = player2
        self.board = board

        self.currentPlayer = player1
        self.winner = None
        self.gameState = GameState.IN_PROGRESS
    
    def makeMove(self, player, col):
        if self.gameState != GameState.IN_PROGRESS:
            return False

        if player != self.currentPlayer:
            return False

        row =  self.board.dropPointer(col, player)

        if row == -1:
            return False

        if self.board.checkWin(row, col, player):
            self.gameState = GameState.WON
            self.winner = player
        elif self.board.isFull():
            self.gameState = GameState.DRAW
        else: 
            self.currentPlayer = self.player2 if (player == self.player1) else self.player1

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getGameState(self):
        return self.gameState.value

    def getBoard(self):
        return self.board

class Board:
    def __init__(self, rows: int, cols: int):
        self.cells = [[0 for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.cols = cols
    
    def placePointer(self, x: int, y: int, player: Player):
        self.cells[x][y] = player.color.value
    
    def dropPointer(self, col: int, player: Player):
        if col < 0 or col >= self.cols:
            return -1

        for i in range(self.rows-1, -1, -1):
            if not self.cells[i][col]:
                self.placePointer(i, col, player)
                return i
        
        return -1
    
    def isFull(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j] == 0:
                    return False
        
        return True

    def checkWin(self, lastX: int, lastY: int, lastPlayer: int):
        consecutive = 0
        for i in range(self.rows):
            if self.cells[i][lastY] == lastPlayer:
                consecutive += 1
            else:
                consecutive = 0
            if consecutive == MAX_CONSECUTIVES:
                return True
        
        for j in range(self.cols):
            if self.cells[lastX][j] == lastPlayer:
                consecutive += 1
            else:
                consecutive = 0
            if consecutive == MAX_CONSECUTIVES:
                return True
        
        min_ = min(lastX, lastY)
        i, j = lastX - min_, lastY - min_

        while i < self.rows and j < self.cols:
            if self.cells[i][j] == lastPlayer:
                consecutive += 1
            else:
                consecutive = 0
            if consecutive == MAX_CONSECUTIVES:
                return True
            i += 1
            j += 1

        min_ = min(lastX, self.cols - lastY - 1)
        i, j = lastX - min_, lastY + min_

        while i < self.rows and j >= 0:
            if self.cells[i][j] == lastPlayer:
                consecutive += 1
            else:
                consecutive = 0
            if consecutive == MAX_CONSECUTIVES:
                return True
            i += 1
            j -= 1
        
        return False

    def __repr__(self) -> str:
        grid = ""
        for i in range(self.rows):
            for j in range(self.cols):
                grid += (str(self.cells[i][j]) + "\t")
            grid += "\n"

        return grid

def main():
    grid = Board(5, 5)

    player1 = Player(DiscColor.BLUE)
    player2 = Player(DiscColor.RED)

    game = Game(player1, player2, grid)

    game.makeMove(player1, 0)
    game.makeMove(player2, 4)
    game.makeMove(player2, 2)

    print(game.getBoard())



if __name__ == '__main__':
    main()