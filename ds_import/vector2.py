class Vector2:
    """A class that represents a 2D vector."""

    def __init__(self, x=0.0, y=0.0):
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

        self._x = x
        self._y = y

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

    def __str__(self):
        return 'x: {}, y: {}'.format(self.x, self.y)
