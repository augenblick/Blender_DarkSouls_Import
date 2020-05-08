from ds_import.face_set import FaceSet
from ds_import.vertex import Vertex


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
            self.vertices = vertices

        if face_sets is not None:
            self.face_sets = face_sets

    @property
    def vertices(self):
        """List of Vertex objects."""
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        # validate vertices
        if len(vertices) < 3:
            raise ValueError("At least three vertices expected")
        for v in vertices:
            if not isinstance(v, Vertex):
                raise TypeError("Object of type Vertex expected, however type {} was passed".format(type(v)))

        self._vertices = vertices

    @property
    def face_sets(self):
        """List of FaceSet objects."""
        return self._face_sets

    @face_sets.setter
    def face_sets(self, face_sets):
        # validate faces
        for fs in face_sets:
            if not isinstance(fs, FaceSet):
                raise TypeError("Object of type FaceSet expected, however type {} was passed".format(type(fs)))

        self._face_sets = face_sets

    def __str__(self):
        return_string = ''

        for i in range(0, len(self.vertices)):
            return_string += f'vertex[{i}]={self.vertices[i]}\n'

        for i in range(0, len(self.face_sets)):
            return_string += f'face_set[{i}]={self.face_sets[i]}\n'

        return return_string
