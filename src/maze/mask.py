"""Mask implementation."""
from attrs import define
from attrs import Factory
from attrs import field
from PIL import Image


@define
class Mask:
    """A Mask to define the shape of a maze's grid."""

    rows: int
    columns: int
    bits: list[list[bool]] = field(
        default=Factory(
            lambda self: [
                [True for column in range(self.columns)] for row in range(self.rows)
            ],
            takes_self=True,
        )
    )

    @classmethod
    def prepare_simple(cls) -> "Mask":
        """Prepare a simple mask, primarily for testing purposes.

        Returns:
            Mask: a simple 3x3 mask
        """
        mask = Mask(rows=3, columns=3)
        mask.bits[0][0] = False
        mask.bits[1][0] = False
        mask.bits[0][1] = False
        return mask

    @classmethod
    def prepare_from_png(cls, path: str) -> "Mask":
        """Make a mask from a png."""
        with Image.open(path) as image:
            mask = Mask(rows=image.height, columns=image.width)
            for x in range(image.width):
                for y in range(image.height):
                    if image.getpixel((x, y)) == (0, 0, 0):
                        mask.bits[y][x] = False
            return mask
