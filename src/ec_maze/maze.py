"""Command-line interface."""
from typing import IO

import click

from ec_maze.aldous_broder import AldousBroder
from ec_maze.grid import Grid
from ec_maze.mask import Mask


def example_gen_png(fp: IO[bytes]) -> None:
    """Generate a maze in png format given a file io."""

    m = Mask.prepare_from_png("src/ec_maze/cat.png")
    grid = AldousBroder.on(Grid.prepare_masked_grid(m))
    grid.render().save(fp, format="PNG")


@click.command()
@click.version_option()
def main() -> None:
    """Generate an example maze."""
    with open("cat_maze.png", mode="wb") as f:
        example_gen_png(f)


if __name__ == "__main__":
    main(prog_name="maze")  # pragma: no cover
