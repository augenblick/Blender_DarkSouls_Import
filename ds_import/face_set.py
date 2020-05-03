from face import Face


class FaceSet:
    """A class that represents a set of Faces."""

    def __init__(self, vertices=None):
        """

        :param vertices: List of three Vertex objects.
        """

        self._faces = []

    @property
    def faces(self):
        """A list of Faces."""
        return self._faces

    @faces.setter
    def faces(self, faces):
        self._faces = faces
