from random import randrange

from src.maze import Grid


class BinaryTree:
    @classmethod
    def on(cls, grid: Grid) -> Grid:
        for cell in grid.each_cell():
            neighbors = list()
            if cell.north:
                neighbors.append(cell.north)
            if cell.east:
                neighbors.append(cell.east)
            if neighbors:
                index = randrange(len(neighbors))
                cell.link(neighbors[index])
        return grid
