import random
from typing import Optional

class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0

    def reveal(self):
        self.is_revealed = True
    
    def toggle_flag(self):
        self.is_flagged = not self.is_flagged

    def set_mine(self):
        self.is_mine = True

    def add_neighbor(self):
        self.neighbor_mines += 1

class Board:
    offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)]

    def __init__(self, cols: int, rows: int, num_mines: int):
        self.cols = cols
        self.rows = rows
        self.num_mines = num_mines
        self.grid = [[Cell(r, c) for c in range(self.cols)] for r in range(self.rows)]

    def get_all_positions(self) -> list[tuple[int, int]]:
        return [(r, c) for r in range(self.rows) for c in range(self.cols)]

    def place_mines(self) -> None:
        all_positions = self.get_all_positions()

        mine_positions = random.sample(all_positions, self.num_mines)
        self.mine_positions = mine_positions

        for r, c in mine_positions:
            mine_cell = self.grid[r][c]
            mine_cell.set_mine()
            self.increment_neighbor_mine_counts(r, c)

    def increment_neighbor_mine_counts(self, r: int, c:int) -> None:
        for r_offset, c_offset in self.offsets:
            new_r, new_c = r + r_offset, c + c_offset

            if self.is_inbound(r, c):
                neighbor_cell = self.grid[new_r][new_c]

                if not neighbor_cell.is_mine:
                    neighbor_cell.add_neighbor() 
            else:
                # throw error
                return None

    def handle_click(self, r: int, c:int) -> list[Cell]:
        revealed_cells = []

        if self.is_inbound(r, c):
            cell = self.grid[r][c]

            if cell.is_revealed:
                return []
        
            if cell.is_flagged:
                cell.toggle_flag()

            if cell.is_mine:
                revealed_cells = self.reveal_all()
            else:
                revealed_cells = self.reveal(r, c) 

            return revealed_cells 
        else:
            return []

    def reveal(self, r: int, c: int) -> list[Cell]:
        if not self.is_inbound(r, c):
            return []
            
        revealed_cells = []
        stack = [(r, c)]
        visited = set()

        while stack:  
            cell_row, cell_col = stack.pop()
            
            if (cell_row, cell_col) in visited:
                continue
                
            if not self.is_inbound(cell_row, cell_col):
                continue
                
            cell = self.grid[cell_row][cell_col]
            cell.reveal()
            revealed_cells.append(cell)
            visited.add((cell_row, cell_col))

            if cell.neighbor_mines == 0:
                for r_offset, c_offset in self.offsets:
                    new_row = cell_row + r_offset
                    new_col = cell_col + c_offset
                    stack.append((new_row, new_col))
        
        return revealed_cells

    def reveal_all(self):
        # TODO: reveal all cells on game loss
        return 

    # Helper Functions 
    def is_inbound(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols