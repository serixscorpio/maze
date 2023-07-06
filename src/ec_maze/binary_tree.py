"""Binary Tree Algorithm."""
from random import randrange

from ec_maze.grid import Grid


class BinaryTree:
    """Binary Tree Algorithm to generate a maze."""

    @classmethod
    def on(cls, grid: Grid) -> Grid:
        """Run binary tree algorithm on a grid."""
        for cell in grid.each_cell():
            neighbors = list()
            if cell.north:
                neighbors.append(cell.north)
            if cell.east:
                neighbors.append(cell.east)
            if neighbors:
                index = randrange(len(neighbors))  # nosec: B311
                cell.link(neighbors[index])
        return grid
