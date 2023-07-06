"""Maze."""
from __future__ import annotations

from random import randrange
from typing import Iterable

from attrs import define, field
from PIL import Image, ImageDraw

from ec_maze.mask import Mask


__version__ = "0.0.4"

from ec_maze.maze import main  # noqa: F401


@define(eq=False)
class Cell:
    """Cell represents a single unit within a Grid."""

    row: int
    column: int
    north: Cell | None = field(default=None)
    south: Cell | None = field(default=None)
    east: Cell | None = field(default=None)
    west: Cell | None = field(default=None)
    links: dict[tuple[int, int], bool] = field(factory=dict)

    def link(self, cell: Cell, bidirection: bool = True) -> None:
        """Link this Cell to a target Cell.

        bidirection: whether or not target cell should link back.
        """
        self.links[(cell.row, cell.column)] = True
        if bidirection:
            cell.link(self, False)

    def unlink(self, cell: Cell, bidirection: bool = True) -> None:
        """Unlink this Cell from a target Cell.

        bidirection: whether or not target cell should unlink.
        """
        self.links[(cell.row, cell.column)] = False
        if bidirection:
            cell.unlink(self, False)

    def is_linked_to(self, cell: Cell | None) -> bool:
        """Return if this cell is linked to a target cell."""
        if cell is None:
            return False
        return self.links.get((cell.row, cell.column), False)

    def neighbors(self) -> list[Cell]:
        """Return this cell's neighboring cells."""
        return list(filter(None, [self.north, self.south, self.east, self.west]))


@define
class Grid:
    """Grid representing a maze."""

    rows: int
    columns: int
    grid: list[list[Cell | None]]

    def get(self, row: int, column: int) -> Cell | None:
        """Retrieve a Cell given a coordinate."""
        if row >= self.rows or row < 0:
            return None
        if column >= self.columns or column < 0:
            return None
        return self.grid[row][column]

    def _configure_cells(self) -> None:
        """Initialize cells' neighbors."""
        for cell in self.each_cell():
            cell.north = self.get(cell.row - 1, cell.column)
            cell.south = self.get(cell.row + 1, cell.column)
            cell.west = self.get(cell.row, cell.column - 1)
            cell.east = self.get(cell.row, cell.column + 1)

    @classmethod
    def prepare_grid(cls, rows: int, columns: int) -> Grid:
        """Prepare a grid without masking any cells."""
        mask = Mask(rows=rows, columns=columns)
        return cls.prepare_masked_grid(mask)

    @classmethod
    def prepare_masked_grid(cls, mask: Mask) -> Grid:
        """Prepare a masked grid."""
        two_d_array_of_cells: list[list[Cell | None]] = [
            [
                Cell(row_index, column_index) if bit else None
                for column_index, bit in enumerate(row)
            ]
            for row_index, row in enumerate(mask.bits)
        ]
        grid = cls(rows=mask.rows, columns=mask.columns, grid=two_d_array_of_cells)
        grid._configure_cells()
        return grid

    def random_cell(self) -> Cell:
        """Return a random cell."""
        while True:
            row = randrange(self.rows)  # nosec: B311
            column = randrange(self.columns)  # nosec: B311
            if cell := self.grid[row][column]:
                return cell

    def size(self) -> int:
        """Return number of cells within this grid."""
        return len(list(self.each_cell()))

    def each_row(self) -> Iterable[Iterable[Cell | None]]:
        """Yield each row from this grid."""
        yield from self.grid

    def each_cell(self) -> Iterable[Cell]:
        """Yield each cell from this grid."""
        for row in self.each_row():
            for cell in row:
                if cell:
                    yield cell

    def __repr__(self) -> str:
        """Return an ascii representation of this grid."""
        output = ["+", "---+" * self.columns, "\n"]
        for row in self.each_row():
            top = ["|"]
            bottom = ["+"]
            for cell in row:
                if not cell:
                    cell = Cell(-1, -1)
                top.append("   ")
                if cell.is_linked_to(cell.east):
                    top.append(" ")
                else:
                    top.append("|")
                if cell.is_linked_to(cell.south):
                    bottom.append("   +")
                else:
                    bottom.append("---+")
            top.append("\n")
            bottom.append("\n")
            output.extend(top)
            output.extend(bottom)
        return "".join(output)

    def render(self, cell_size: int = 20, wall_thickness: int = 1) -> Image.Image:
        """Render maze as an image.

        For making physical mazes, try cell_size=40, wall_thickness=15.
        """
        img_width = cell_size * self.columns + 1
        img_height = cell_size * self.rows + 1
        img = Image.new(mode="RGB", size=(img_width, img_height), color="white")
        draw = ImageDraw.Draw(img)

        for cell in self.each_cell():
            x1 = cell.column * cell_size
            y1 = cell.row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            if not cell.north:
                draw.line((x1, y1, x2, y1), fill="black", width=wall_thickness)
            if not cell.west:
                draw.line((x1, y1, x1, y2), fill="black", width=wall_thickness)

            if not cell.is_linked_to(cell.east):
                draw.line((x2, y1, x2, y2), fill="black", width=wall_thickness)
            if not cell.is_linked_to(cell.south):
                draw.line((x1, y2, x2, y2), fill="black", width=wall_thickness)

        # img.show() # for debugging purposes
        return img


