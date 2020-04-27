class Vertex:
    """A class that represents a vertex in Blender"""

    position = [0.0, 0.0, 0.0]

    def __init__(self, position=None):
        """

        :param position: List of three float values (x, y, z).
        """
        if position is not None:
            # validate position
            if len(position) < 3:
                raise ValueError("Three floats expected.")
            for i in position:
                if not isinstance(i, float):
                    raise TypeError("Object of type float expected, however type {} was passed".format(type(m)))

            self.position = position
