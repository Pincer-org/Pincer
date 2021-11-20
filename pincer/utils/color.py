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

    def __init__(self, c: Union[str, int]) -> None:
        if isinstance(c, int):
            self.r = c >> 16 & 255
            self.g = c >> 8 & 255
            self.b = c & 255
            return

        # Conversion modified from this answer
        # https://stackoverflow.com/a/29643643
        if c.startswith("#"):
            c = c[1:]
        self.r, self.g, self.b = (int(c[n:n + 2], 16) for n in (0, 2, 4))

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
