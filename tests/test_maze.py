"""Test maze."""
from maze import Cell, Grid
from maze.aldous_broder import AldousBroder
from maze.binary_tree import BinaryTree
from maze.mask import Mask


def test_neighbors() -> None:
    """Test a cell's presence/absence of neighbors."""
    c_north = Cell(row=0, column=1)
    c_south = Cell(row=2, column=1)
    c_east = Cell(row=1, column=2)
    c_west = Cell(row=1, column=0)
    c = Cell(row=1, column=1, north=c_north, south=c_south, east=c_east, west=c_west)
    assert c.neighbors() == [c_north, c_south, c_east, c_west]
    c.north = None
    assert c.neighbors() == [c_south, c_east, c_west]


def test_link() -> None:
    """Test a cell's link to other cells."""
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
    """Test creating a grid."""
    g = Grid.prepare_grid(2, 3)
    assert g.rows == 2
    assert g.columns == 3
    assert len(g.grid) == 2
    assert g.size() == 6


def test_grid_access() -> None:
    """Test a cell's north/south/west/east in various scenarios."""
    g = Grid.prepare_grid(2, 3)
    assert g.get(2, 3) is None
    neighborly_cell = g.get(1, 1)
    assert neighborly_cell is not None
    assert neighborly_cell.north is g.get(0, 1)
    assert neighborly_cell.south is g.get(2, 1)
    assert neighborly_cell.west is g.get(1, 0)
    assert neighborly_cell.east is g.get(1, 2)
    south_east_corner = g.get(1, 2)
    assert south_east_corner is not None
    assert south_east_corner.south is None
    for cell in g.each_cell():
        assert type(cell) is Cell


def test_grid_random_cell() -> None:
    """Test retrieving a random cell from a grid."""
    g = Grid.prepare_grid(2, 3)
    assert g.random_cell() is not None


def test_grid_ascii_output() -> None:
    """Test ascii output from a grid."""
    g = BinaryTree.on(Grid.prepare_grid(1, 1))
    output = "+---+\n|   |\n+---+\n"
    assert g.__repr__() == output


def test_mask_initialization() -> None:
    """Test creating a mask."""
    m = Mask.prepare_simple()
    assert m.bits[0][0] is False
    assert m.bits[1][0] is False
    assert m.bits[0][1] is False


def test_create_masked_grid() -> None:
    """Test creating a masked grid."""
    m = Mask.prepare_from_png("src/maze/cat.png")
    grid = AldousBroder.on(Grid.prepare_masked_grid(m))
    grid.render()
