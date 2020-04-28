class Vertex:
    """A class that represents a vertex in Blender"""

    x = 0.0
    y = 0.0
    z = 0.0

    def __init__(self, x: float = None, y: float = None, z: float = None):
        """

        :param x: float x-coordinate value
        :param y: float y-coordinate value
        :param z: float z-coordinate value
        """

        if x is not None:
            if not isinstance(x, (float, int)):
                raise TypeError("Expecting numeric value.")
            self.x = x
        if y is not None:
            if not isinstance(y, (float, int)):
                raise TypeError("Expecting numeric value.")
            self.y = y
        if z is not None:
            if not isinstance(z, (float, int)):
                raise TypeError("Expecting numeric value.")
            self.z = z
