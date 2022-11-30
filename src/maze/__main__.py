"""Command-line interface."""
import click

from maze import example_gen_png


@click.command()
@click.version_option()
def main() -> None:
    """Generate an example maze."""
    with open("cat_maze.png", mode="wb") as f:
        example_gen_png(f)


if __name__ == "__main__":
    main(prog_name="maze")  # pragma: no cover
