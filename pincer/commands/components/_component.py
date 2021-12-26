# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from copy import copy

from ...utils.api_object import APIObject


class _Component(APIObject):
    """Represents a message component with attributes that can be modified inline"""

    def with_attrs(self, **kwargs) -> _Component:
        """
        Modifies attributes are returns an object with these attributes.

        .. code-block:: python

            some_button.with_attrs(label="A new label")

        \\*\\*kwargs
            Attributes to modify and their values.
        """
        copied_obj = copy(self)

        for key, value in kwargs.items():
            setattr(copied_obj, key, value)

        return copied_obj
