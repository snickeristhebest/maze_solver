from tkinter import Tk, BOTH, Canvas
import time,random

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
        self.canvas.update()  # Update the canvas content
        self.root.update()  # Force the window to redraw

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
    def __init__(self, start, end, window=None, up=False, down=False, left=False, right=False, win=None, visited = False):
        if not isinstance(start, Point) or not isinstance(end, Point):
            raise TypeError("Constructor only takes Point objects as parameters.")
        if not isinstance(window, Window) and window is not None:
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
        self.visited = visited

    def set_up(self, up):
        if not isinstance(up, bool):
            raise TypeError("set_up(self, up): 'up' must be of type bool")
        self.up = up

    def get_up(self):
        return self.up

    # Similar methods for 'down', 'left', and 'right' attributes
    def set_down(self, down):
        if not isinstance(down, bool):
            raise TypeError("set_down(self, down): 'down' must be of type bool")
        self.down = down

    def get_down(self):
        return self.down

    def set_left(self, left):
        if not isinstance(left, bool):
            raise TypeError("set_left(self, left): 'left' must be of type bool")
        self.left = left

    def get_left(self):
        return self.left

    def set_right(self, right):
        if not isinstance(right, bool):
            raise TypeError("set_right(self, right): 'right' must be of type bool")
        self.right = right

    def get_right(self):
        return self.right
    
    def set_visited(self,visited):
        self.visited = visited
    
    def get_visited(self):
        return self.visited
    
    def set_win(self,win):
        self.win = win
    
    def get_win(self):
        return self.win

    def draw(self):
        if not isinstance(self.start, Point) or not isinstance(self.end, Point):
            raise TypeError("start and end must be Point objects")

        # Draw cell boundaries based on wall attributes
        if self.up:
            self.window.draw_line(Line(self.start, Point(self.end.x, self.start.y)))
        else:
            self.window.draw_line(Line(self.start, Point(self.end.x, self.start.y)), fill_color="white")

        if self.down:
            self.window.draw_line(Line(Point(self.start.x, self.end.y), self.end))
        else:
            self.window.draw_line(Line(Point(self.start.x, self.end.y), self.end), fill_color="white")

        if self.left:
            self.window.draw_line(Line(self.start, Point(self.start.x, self.end.y)))
        else:
            self.window.draw_line(Line(self.start, Point(self.start.x, self.end.y)), fill_color="white")

        if self.right:
            self.window.draw_line(Line(Point(self.end.x, self.start.y), self.end))
        else:
            self.window.draw_line(Line(Point(self.end.x, self.start.y), self.end), fill_color="white")


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
        seed=None
    ):
        self.start = start
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self.seed = random.seed(seed) if seed != None else 0
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
                row_cells.append(Cell(Point(x0, y0), Point(x1, y1),  window=self.window, up=True, down=True, left=True, right=True))
            self.cells.append(row_cells)

    def _draw_cell(self, i, j):
        if 0 <= i < self.num_rows and 0 <= j < self.num_cols:
            self.cells[i][j].draw()

    

    def _draw_maze(self):
            for i in range(self.num_rows):
                for j in range(self.num_cols):
                    self._draw_cell(i, j)

    def _break_entrance_and_exit(self):

        entrance = self.cells[0][0]
        exit = self.cells[self.num_rows-1][self.num_cols-1]
        entrance.set_left(False)
        self._draw_cell(0,0)
        exit.set_right(False)
        exit.set_win(True)
        self._draw_cell(self.num_rows,self.num_cols)

    def _animate(self):
        self.window.redraw()
        time.sleep(0.05)

    def get_adjacent_not_visited(self, i, j):
        adj_cell = {'up': None, 'down': None, 'right': None, 'left': None}

        if 0 <= i - 1 < self.num_rows and not self.cells[i-1][j].get_visited():
            adj_cell['up'] = self.cells[i - 1][j]  # Up
        if 0 <= i + 1 < self.num_rows and not self.cells[i+1][j].get_visited():
            adj_cell['down'] = self.cells[i + 1][j]  # Down
        if 0 <= j - 1 < self.num_cols and not self.cells[i][j-1].get_visited():
            adj_cell['left'] = self.cells[i][j - 1]  # Left
        if 0 <= j + 1 < self.num_cols and not self.cells[i][j+1].get_visited():
            adj_cell['right'] = self.cells[i][j + 1]  # Right

        return adj_cell



    def break_walls_r(self, i, j, current=None):
        if not current:
            current = self.cells[i][j]
        current.set_visited(True)
        while True:
            poss_dir = self.get_adjacent_not_visited(i, j)
            if all(value is None for value in poss_dir.values()):
                return  # All directions visited, exit the loop
            unvisited_dirs = {key: value for key, value in poss_dir.items() if value is not None}
            dir, next = random.choice(list(unvisited_dirs.items()))
            match dir:
                case 'up':
                    current.set_up(False)
                    next.set_down(False)
                    self.break_walls_r(i-1,j,next)
                case 'down':
                    current.set_down(False)
                    next.set_up(False)
                    self.break_walls_r(i+1,j,next)
                case 'right':
                    current.set_right(False)
                    next.set_left(False)
                    self.break_walls_r(i,j+1,next)
                case 'left':
                    current.set_left(False)
                    next.set_right(False)
                    self.break_walls_r(i,j-1,next)
            self._draw_maze()
            
    def reset_cells_visited(self):
        for i in range(self.num_rows):
                for j in range(self.num_cols):
                    self.cells[i][j].set_visited(False)
    
    def solve(self):
        return self._solve_r(0,0,self.cells[0][0])
    
    def _solve_r(self,i,j,current=None):
        self._animate()
        if current.get_win() == True:
            return True
        current.set_visited(True)
        poss_dir = self.get_adjacent_not_visited(i, j)
        unvisited_dirs = {key: value for key, value in poss_dir.items() if value is not None}
        for k,cell in unvisited_dirs.items():
            
            if k == "up" and not cell.get_down() and not current.get_up() and i > 0:
                current.draw_move(cell)
                if self._solve_r(i-1,j,cell):
                    return True
                current.draw_move(cell,True)

            elif k == "down" and not cell.get_up() and not current.get_down() and i < self.num_rows:
                current.draw_move(cell)
                if self._solve_r(i+1,j,cell):
                    return True
                current.draw_move(cell,True)
                
            elif k == "right" and not cell.get_left() and not current.get_right() and j < self.num_cols:
                current.draw_move(cell)
                if self._solve_r(i,j+1,cell):
                    return True
                current.draw_move(cell,True)

            elif k == "left" and not cell.get_right() and not current.get_left() and j > 0:
                current.draw_move(cell)
                if self._solve_r(i,j-1,cell):
                    return True
                current.draw_move(cell,True)
        return False


        
        
        
        
        


def main():
    num_cols = 10
    num_rows = 10
    window = Window(1000, 800)  # Create a new Window object
    maze = Maze(Point(20, 20), num_cols, num_rows, 20, 20, window=window)
    maze._break_entrance_and_exit()
    maze.break_walls_r(0,0)
    maze.reset_cells_visited()
    maze._draw_maze()
    solved = maze.solve()
    print(f"maze solved: {solved}")
    window.wait_for_close()

main()
