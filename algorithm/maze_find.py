

class MazeFind(object):
    def __init__(self, maze_map: list):
        self.maze_map = maze_map
        self.success = False
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.trajectory_x = list()
        self.trajectory_y = list()
        self.trajectory_size = 0

    def visit(self, start_x: int, start_y: int, end_x: int, end_y: int):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

        self._recursive_visit(start_x, start_y)
        if self.success is False:
            print("There is no solution")
        else:
            print("Wow")
            for i in range(self.trajectory_size):
                print("({}, {})".format(self.trajectory_x[i], self.trajectory_y[i]))

    def _recursive_visit(self, i: int, j: int):
        self.maze_map[i][j] = 1

        self.trajectory_x.append(i)
        self.trajectory_y.append(j)
        self.trajectory_size += 1

        if i == self.end_x and j == self.end_y:
            self.success = True

        if self.success is not True and self.maze_map[i][j+1] == 0:
            self._recursive_visit(i, j+1)
        if self.success is not True and self.maze_map[i+1][j] == 0:
            self._recursive_visit(i+1, j)
        if self.success is not True and self.maze_map[i][j-1] == 0:
            self._recursive_visit(i, j-1)
        if self.success is not True and self.maze_map[i-1][j] == 0:
            self._recursive_visit(i-1, j)

        if self.success is False:
            self.trajectory_x.pop()
            self.trajectory_y.pop()
            self.trajectory_size -= 1

        if self.success is True:
            print(" ({},{})".format(i, j))

        return self.success

