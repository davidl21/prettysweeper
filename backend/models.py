import random

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
    def __init__(self, cols: int, rows: int, num_mines: int):
        self.cols = cols
        self.rows = rows
        self.num_mines = num_mines
        self.grid = [[Cell(r, c) for c in range(self.cols)] for r in range(self.rows)]

    def place_mines(self):
        all_positions = []

        for r in range(self.rows):
            for c in range(self.cols):
                all_positions.append((r, c))

        mine_positions = random.sample(all_positions, self.num_mines)
        self.mine_positions = mine_positions

        for r, c in mine_positions:
            mine_cell = self.grid[r][c]
            mine_cell.set_mine()
            self.compute_neighbors(r, c)

    def compute_neighbors(self, r: int, c:int) -> None:
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)]

        for r_offset, c_offset in offsets:
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
            # TODO
            cell = self.grid[r][c]

            if cell.is_revealed:
                # do nothing, handle later
                return
        
            if cell.is_flagged:
                # remove flag
                return

            if cell.is_mine:
                # end game, reveal all
                self.reveal_all()
            else:
                revealed_cells.append(cell)
                cell.reveal()
                neighbors = cell.neighbor_mines


            return 
        else:
            # throw out of bounds error
            return

    def reveal_all(self):
        # TODO: reveal all cells on game loss
        return 

    # Helper Functions 
    def is_inbound(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols