class Vector3:
    """A class that represents a 3D vector."""

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """
        :type x: float
        :type y: float

        :param x: x-component
        :param y: y-component
        """
        if not isinstance(x, float):
            raise TypeError('Expects float value.')
        if not isinstance(y, float):
            raise TypeError('Expects float value.')
        if not isinstance(z, float):
            raise TypeError('Expects float value.')

        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        """x-component"""
        return self._x

    @x.setter
    def x(self, x):
        if not isinstance(x, float):
            raise TypeError('Expects float value.')
        self._x = x

    @property
    def y(self):
        """y-component"""
        return self._y

    @y.setter
    def y(self, y):
        if not isinstance(y, float):
            raise TypeError('Expects float value.')
        self._y = y

    @property
    def z(self):
        """z-component"""
        return self._z

    @z.setter
    def z(self, z):
        if not isinstance(z, float):
            raise TypeError('Expects float value.')
        self._z = z
