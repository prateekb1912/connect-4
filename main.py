MAX_CONSECUTIVES = 4

class Grid:
    def __init__(self, rows: int, cols: int):
        self.cells = [[0 for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.cols = cols
    
    def placePointer(self, x: int, y: int, player: int):
        self.cells[x][y] = player
    
    def dropPointer(self, col: int, player: int):
        for i in range(self.rows-1, 0, -1):
            if not self.cells[i][col]:
                self.placePointer(i, col, player)
                break
    
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
    grid = Grid(5, 5)

    grid.placePointer(0, 4, 1)
    grid.placePointer(1, 3, 1)
    grid.placePointer(2, 2, 1)
    grid.placePointer(3, 1, 1)


if __name__ == '__main__':
    main()