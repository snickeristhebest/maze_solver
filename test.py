import unittest
from app import Maze, Point, Window

class Tests(unittest.TestCase):

    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        # window = Window(1000, 800)  # Create a new Window object
        m1 = Maze(Point(20, 20), num_cols, num_rows, 20, 20)#, window=window)  # Pass the window to Maze constructor
        # m1._draw_maze()
        self.assertEqual(len(m1.cells), num_cols)
        self.assertEqual(len(m1.cells[0]), num_rows)
        # window.wait_for_close()

    def test_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        window = Window(1000, 800)  # Create a new Window object
        m1 = Maze(Point(20, 20), num_cols, num_rows, 20, 20, window=window)  # Pass the window to Maze constructor
        m1._break_entrance_and_exit()
        m1._draw_maze()
        self.assertEqual(m1.cells[0][0].get_left(), False)
        # window.wait_for_close()

    def test_reset_cells_visited(self):
        num_cols = 12
        num_rows = 10
        window = Window(1000, 800)  # Create a new Window object
        m1 = Maze(Point(20, 20), num_cols, num_rows, 20, 20, window=window)  # Pass the window to Maze constructor
        m1._break_entrance_and_exit()
        m1.break_walls_r(0,0)
        m1.reset_cells_visited()
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertEqual(m1.cells[i][j].get_visited(), False)
        window.wait_for_close()

if __name__ == "__main__":
    unittest.main()
