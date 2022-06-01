# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

import string
from typing import Union


class Color:
    """
    A color in RGB.

    Parameters
    ---------
    c : Union[:class:`str`,:class:`int`]
        The hex color can be a string that optionally starts with an ``#`` or
        an int with the RGB values.
    Attributes
    ---------
    r : :class:`int`
        The red value for this color.
    g : :class:`int`
        The green value for this color.
    b : :class:`int`
        The blue value for this color.
    """

    _MIN_VALUE = 0
    _MAX_VALUE = 1 << 24

    def __init__(self, c: Union[str, int]) -> None:
        if isinstance(c, int):
            if c < self._MIN_VALUE or c >= self._MAX_VALUE:
                raise ValueError("The color must be between 0 and 16777215")

            self.r = c >> 16 & 255
            self.g = c >> 8 & 255
            self.b = c & 255
            return

        # Conversion modified from this answer
        # https://stackoverflow.com/a/29643643
        if c.startswith("#"):
            c = c[1:]

        if len(c) != 6:
            raise ValueError("Hex value must be 6 characters.")

        if any(digit not in string.hexdigits for digit in c):
            raise ValueError("Illegal hex digit character.")

        self.r, self.g, self.b = (int(c[n : n + 2], 16) for n in (0, 2, 4))

    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b

    def __repr__(self):
        return f"Color(r={self.r}, g={self.g}, b={self.b})"

    def __str__(self) -> str:
        return f"#{self.hex}"

    @property
    def rbg(self):
        """
        Returns
        -------
        Tuple[:class:`int`, :class:`int` :class:`int`]
            Tuple value for rgb.
        """
        return self.r, self.g, self.b

    @property
    def hex(self):
        """
        Returns
        ---------
        str
            Str value for hex.
        """
        return f"{self.r:02x}{self.g:02x}{self.b:02x}"
