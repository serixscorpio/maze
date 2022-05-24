"""Maze"""
import tempfile
from random import randrange
from typing import BinaryIO
from typing import Iterable
from typing import Optional

from attrs import define
from attrs import field
from PIL import Image
from PIL import ImageDraw

from maze.mask import Mask


@define(eq=False)
class Cell:
    row: int
    column: int
    north: Optional["Cell"] = field(default=None)
    south: Optional["Cell"] = field(default=None)
    east: Optional["Cell"] = field(default=None)
    west: Optional["Cell"] = field(default=None)
    links: dict[tuple[int, int], bool] = field(factory=dict)

    def link(self, cell: "Cell", bidirection: bool = True) -> None:
        self.links[(cell.row, cell.column)] = True
        if bidirection:
            cell.link(self, False)

    def unlink(self, cell: "Cell", bidirection: bool = True) -> None:
        self.links[(cell.row, cell.column)] = False
        if bidirection:
            cell.unlink(self, False)

    def is_linked_to(self, cell: Optional["Cell"]) -> bool:
        if cell is None:
            return False
        return self.links.get((cell.row, cell.column), False)

    def neighbors(self) -> list["Cell"]:
        return list(filter(None, [self.north, self.south, self.east, self.west]))


@define
class Grid:
    rows: int
    columns: int
    grid: list[list[Optional[Cell]]]

    def get(self, row: int, column: int) -> Optional["Cell"]:
        if row >= self.rows or row < 0:
            return None
        if column >= self.columns or column < 0:
            return None
        return self.grid[row][column]

    def _configure_cells(self) -> None:
        """initialize cells' neighbors"""
        for cell in self.each_cell():
            cell.north = self.get(cell.row - 1, cell.column)
            cell.south = self.get(cell.row + 1, cell.column)
            cell.west = self.get(cell.row, cell.column - 1)
            cell.east = self.get(cell.row, cell.column + 1)

    @classmethod
    def prepare_grid(cls, rows: int, columns: int) -> "Grid":
        mask = Mask(rows=rows, columns=columns)
        return cls.prepare_masked_grid(mask)

    @classmethod
    def prepare_masked_grid(cls, mask: Mask) -> "Grid":
        """Prepare a masked grid
        For now, it seems upon the creation of a grid, the mask no longer need to be kept
        """
        two_d_array_of_cells: list[list[Optional[Cell]]] = [
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
        while True:
            row = randrange(self.rows)
            column = randrange(self.columns)
            if cell := self.grid[row][column]:
                return cell

    def size(self) -> int:
        return len(list(self.each_cell()))

    def each_row(self) -> Iterable[Iterable[Optional[Cell]]]:
        yield from self.grid

    def each_cell(self) -> Iterable[Cell]:
        for row in self.each_row():
            for cell in row:
                if cell:
                    yield cell

    def __repr__(self) -> str:
        output = ["+", "---+" * self.columns, "\n"]
        for row in self.each_row():
            top = ["|"]
            bottom = ["+"]
            for cell in row:
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

    def render(self, cell_size: int = 20, wall_thickness: int = 1) -> Image:
        """render maze as an image
        For making physical mazes, try cell_size=40, wall_thickness=15

        Args:
            cell_size (int, optional): _description_. Defaults to 20.
            wall_thickness (int, optional): _description_. Defaults to 1.
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


def example_gen_png(fp: BinaryIO) -> None:
    from src.maze.aldous_broder import AldousBroder

    m = Mask.prepare_from_png("cat.png")
    grid = AldousBroder.on(Grid.prepare_masked_grid(m))
    grid.render().save(fp, format="PNG")
