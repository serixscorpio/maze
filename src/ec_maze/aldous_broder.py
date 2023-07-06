"""Aldous Broder Algorithm to generate maze."""
from random import choice

from ec_maze.grid import Cell, Grid


class AldousBroder:
    """Aldous Broder Algorithm to generate maze."""

    @classmethod
    def on(cls, grid: Grid) -> Grid:
        """Run Aldous Broder to generate maze."""
        cell: Cell = grid.random_cell()
        unvisited = grid.size() - 1

        while unvisited > 0:
            neighbor = choice(cell.neighbors())  # nosec: B311
            if len(neighbor.links) == 0:
                cell.link(neighbor)
                unvisited -= 1
            cell = neighbor

        return grid
