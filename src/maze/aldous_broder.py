from random import choice

from src.maze import Cell
from src.maze import Grid


class AldousBroder:
    @classmethod
    def on(cls, grid: Grid) -> Grid:
        cell: Cell = grid.random_cell()
        unvisited = grid.size() - 1

        while unvisited > 0:
            neighbor = choice(cell.neighbors())
            if len(neighbor.links) == 0:
                cell.link(neighbor)
                unvisited -= 1
            cell = neighbor

        return grid
