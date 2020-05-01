class Vector3:
    """A class that represents a 3D vector."""

    x = 0.0
    y = 0.0
    z = 0.0

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        """
        :type x: float
        :type y: float

        :param x: x-component
        :param y: y-component
        """
        if not isinstance(x, (int, float)):
            raise TypeError('Expects numeric value.')
        if not isinstance(y, (int, float)):
            raise TypeError('Expects numeric value.')
        if not isinstance(z, (int, float)):
            raise TypeError('Expects numeric value.')

        self.x = x
        self.y = y
        self.z = z
