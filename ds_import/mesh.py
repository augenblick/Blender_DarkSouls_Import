from face_set import FaceSet
from vertex import Vertex


class Mesh:
    """A class that represents a mesh in Blender."""

    def __init__(self, vertices=None, face_sets=None):
        """

        :param vertices: List of Vertex objects
        :param face_sets: List of FaceSet objects
        """

        self._vertices = []
        self._face_sets = []

        if vertices is not None:

            # validate vertices
            if len(vertices) < 3:
                raise ValueError("At least three vertices expected")
            for v in vertices:
                if not isinstance(v, Vertex):
                    raise TypeError("Object of type Vertex expected, however type {} was passed".format(type(v)))

            self._vertices = vertices

        if face_sets is not None:
            # validate faces
            for fs in face_sets:
                if not isinstance(fs, FaceSet):
                    raise TypeError("Object of type FaceSet expected, however type {} was passed".format(type(fs)))

            self._face_sets = face_sets

    @property
    def vertices(self):
        """List of Vertex objects."""
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        self._vertices = vertices

    @property
    def face_sets(self):
        """List of FaceSet objects."""
        return self._face_sets

    @face_sets.setter
    def face_sets(self, face_sets):
        self._face_sets = face_sets
