from tkinter import Tk, BOTH, Canvas
import time

class Window:

    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title("maze solver")
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.running = True
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        while self.running == True:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self,line,fill_color="black"):
        if not isinstance(line,Line):
            raise TypeError("draw_line(self,line,fill_color=\"black\", canvas param must be Canvas object")
        if not isinstance(fill_color,str):
            raise TypeError("draw_line(self,line,fill_color=\"black\", fill_color must be type string")

        line.draw(self.canvas,fill_color)



class Point:
    def __init__(self, x, y):
        if not isinstance(x, (float, int)) or not isinstance(y, (float, int)):
            raise TypeError("Constructor only takes floats or integers as parameters.")
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"


class Line:
    def __init__(self, start, end):
        if not isinstance(start, Point) or not isinstance(end, Point):
            raise TypeError("Constructor only takes Point objects as parameters.")
        self.start = start
        self.end = end
    
    def draw(self,canvas,fill_color="black"):
        if not isinstance(canvas,Canvas):
            raise TypeError("canvas param must be Canvas object")
        if not isinstance(fill_color,str):
            raise TypeError("fill_color must be type string")
        
        canvas.create_line(
            self.start.x, self.start.y,
            self.end.x,self.end.y, 
            fill=fill_color, width=2
            )
        canvas.pack()
        
        

    def __repr__(self):
        return f"Line(start={self.start}, end={self.end})"

class Cell:
    def __init__(self, start, end, window=None, up=False, down=False, left=False, right=False, win=None):
        if not isinstance(start, Point) or not isinstance(end, Point):
            raise TypeError("Constructor only takes Point objects as parameters.")
        if not isinstance(window, Window):
            raise TypeError("window param takes Window object")
        if not isinstance(win, bool) and win is not None:
            raise TypeError("win param takes boolean")
        self.start = start
        self.end = end
        self.window = window 
        self.win = win if win is not None else False
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    def draw(self):
        if not isinstance(self.start, Point) or not isinstance(self.end, Point):
            raise TypeError("start and end must be Point objects")

        # Draw cell boundaries based on wall attributes
        if self.up:
            self.window.draw_line(Line(self.start, Point(self.end.x, self.start.y)))
        if self.down:
            self.window.draw_line(Line(Point(self.start.x, self.end.y), self.end))
        if self.left:
            self.window.draw_line(Line(self.start, Point(self.start.x, self.end.y)))
        if self.right:
            self.window.draw_line(Line(Point(self.end.x, self.start.y), self.end))

    def draw_move(self, to_cell, undo=False):
        if not isinstance(to_cell,Cell):
            raise TypeError("draw_move(self, to_cell, undo=False) method to_cell must be a cell")
          
        starting_center = Point((self.start.x  + self.end.x) / 2, (self.start.y + self.end.y) / 2)
        ending_center = Point((to_cell.start.x + to_cell.end.x) / 2, (to_cell.start.y + to_cell.end.y) / 2)

        fill_color = "grey" if undo else "red"
        self.window.draw_line(Line(starting_center, ending_center), fill_color=fill_color)

class Maze:
    def __init__(
        self,
        start,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        window=None,
    ):
        self.start = start
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self._create_cells()

    def _create_cells(self):
        self.cells = []
        for row in range(self.num_rows):
            row_cells = []
            for col in range(self.num_cols):
                # Calculate the coordinates of the cell
                x0 = self.start.x + col * self.cell_size_x
                y0 = self.start.y + row * self.cell_size_y
                x1 = x0 + self.cell_size_x
                y1 = y0 + self.cell_size_y
                # Create a cell object and store it in the cells list
                row_cells.append(Cell(Point(x0, y0), Point(x1, y1), self.window))
            self.cells.append(row_cells)

    def _draw_cell(self, i, j):
        if 0 <= i < self.num_rows and 0 <= j < self.num_cols:
            self.cells[i][j].draw()

    def _animate(self):
        self.window.redraw()
        time.sleep(0.05)


def main():
    window = Window(1000, 800)
    start = Point(20, 20)
    maze = Maze(start, 1, 1, 20, 20, window)
    maze._draw_cell(2, 3)  # Example cell at row 2, column 3
    maze._animate()
    window.wait_for_close()

main()
