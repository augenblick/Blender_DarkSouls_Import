from ds_import.face import Face


class FaceSet:
    """A class that represents a set of Faces."""

    def __init__(self, faces=None):
        """

        :param faces: List of Face objects.
        """
        if faces is not None:
            self._faces = faces
        else:
            self._faces = []

    @property
    def faces(self):
        """A list of Faces."""
        return self._faces

    @faces.setter
    def faces(self, faces):
        """

        :type faces: List of Face objects
        """
        if not isinstance(faces, list):
            raise TypeError('Not a list.')
        for f in faces:
            if not isinstance(f, Face):
                raise TypeError("Object of type Face expected, however type {} was passed".format(type(f)))

        self._faces = faces
