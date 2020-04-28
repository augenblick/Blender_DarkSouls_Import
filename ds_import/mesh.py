from blender_darksouls_import import  face
from blender_darksouls_import import  vertex


class Mesh:
    """A class that represents a mesh in Blender."""

    vertices = []
    faces = []

    def __init__(self, vertices=None, faces=None):
        """

        :param vertices: List of Vertex objects
        :param faces: List of Face objects
        """

        if vertices is not None:

            # validate vertices
            if len(vertices) < 3:
                raise ValueError("At least three vertices expected")
            for v in vertices:
                if not isinstance(v, Vertex):
                    raise TypeError("Object of type Vertex expected, however type {} was passed".format(type(m)))

            self.vertices = vertices

        if faces is not None:
            # validate faces
            for f in faces:
                if not isinstance(f, Face):
                    raise TypeError("Object of type Face expected, however type {} was passed".format(type(m)))

            self.faces = faces

