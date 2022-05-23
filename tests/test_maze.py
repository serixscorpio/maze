from src.maze import Cell
from src.maze import Grid
from src.maze.mask import Mask

from maze.binary_tree import BinaryTree


def test_neighbors() -> None:
    c_north = Cell(row=0, column=1)
    c_south = Cell(row=2, column=1)
    c_east = Cell(row=1, column=2)
    c_west = Cell(row=1, column=0)
    c = Cell(row=1, column=1, north=c_north, south=c_south, east=c_east, west=c_west)
    assert c.neighbors() == [c_north, c_south, c_east, c_west]
    c.north = None
    assert c.neighbors() == [c_south, c_east, c_west]


def test_link() -> None:
    c1 = Cell(row=0, column=1)
    c2 = Cell(row=0, column=0)
    c1.link(c2)
    assert c1.is_linked_to(c2)
    assert c2.is_linked_to(c1)
    assert not c1.is_linked_to(c1)
    assert not c2.is_linked_to(c2)
    c2.unlink(c1)
    assert not c1.is_linked_to(c2)
    assert not c2.is_linked_to(c1)


def test_grid_creation() -> None:
    g = Grid.prepare_grid(2, 3)
    assert g.rows == 2
    assert g.columns == 3
    assert len(g.grid) == 2
    assert g.size() == 6


def test_grid_access() -> None:
    g = Grid.prepare_grid(2, 3)
    assert g.get(2, 3) is None
    assert g.get(1, 2) is not None
    assert g.get(1, 1).north == g.get(0, 1)
    assert g.get(1, 1).south == g.get(2, 1)
    assert g.get(1, 1).west == g.get(1, 0)
    assert g.get(1, 1).east == g.get(1, 2)
    assert g.get(1, 2).south is None
    for cell in g.each_cell():
        assert type(cell) is Cell


def test_grid_random_cell() -> None:
    g = Grid.prepare_grid(2, 3)
    assert g.random_cell() is not None


def test_grid_ascii_output() -> None:
    g = BinaryTree.on(Grid.prepare_grid(2, 3))
    print(g)


def test_mask_initialization() -> None:
    m = Mask.prepare_simple()
    assert m.bits[0][0] == False
    assert m.bits[1][0] == False
    assert m.bits[0][1] == False
