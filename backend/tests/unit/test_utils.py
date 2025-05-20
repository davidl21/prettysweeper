import pytest
from backend.models import Board

class TestReveal:
    @pytest.fixture
    def board_3x3(self) -> Board:
        board = Board(3, 3, 1)
        board.grid[1][1].set_mine()
        for r in range(3):
            for c in range(3):
                if (r, c) != (1, 1):
                    board.grid[r][c].neighbor_mines = 1
        return board
    
    @pytest.fixture
    def empty_board(self) -> Board:
        return Board(3, 3, 0)

    def test_reveal_single_numbered_cell(self, board_3x3):
        """Verify revealing a cell with neighbors only reveals that cell"""
        revealed = board_3x3.reveal(0, 0)
        
        assert len(revealed) == 1
        assert revealed[0].x == 0 and revealed[0].y == 0
        assert revealed[0].neighbor_mines == 1
        assert revealed[0].is_revealed

    def test_reveal_flood_fill(self, empty_board):
        """Verify flood fill behavior on empty board"""
        revealed = empty_board.reveal(0, 0)
        
        # Should reveal all cells since there are no mines/numbers
        assert len(revealed) == 9
        
        # Verify all cells in the grid are revealed
        for row in empty_board.grid:
            for cell in row:
                assert cell.is_revealed

    @pytest.mark.parametrize("coords", [
        (-1, 0),  # left edge
        (3, 0),   # right edge
        (0, -1),  # top edge
        (0, 3),   # bottom edge
    ])
    def test_reveal_out_of_bounds(self, empty_board, coords):
        """Verify out of bounds handling"""
        row, col = coords
        revealed = empty_board.reveal(row, col)
        assert revealed == []

    def test_reveal_visited_cells(self, empty_board):
        """Verify cells aren't revealed multiple times"""
        # First reveal
        first_revealed = empty_board.handle_click(0, 0)
        print(first_revealed)
        
        # Second reveal of already revealed area
        second_revealed = empty_board.handle_click(0, 0)
        assert len(second_revealed) == 0