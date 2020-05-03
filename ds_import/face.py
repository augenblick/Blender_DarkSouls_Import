from vertex import Vertex


class Face:
    """A class that represents a triangular face in Blender."""

    def __init__(self, vertices=None):
        """

        :param vertices: List of unsigned ints, each representing the index of a list of Vertex objects.
        """
        if vertices is not None:
            # validate vertices
            if len(vertices) != 3:
                raise ValueError('Three unsigned integers expected.')
            for vertex_index in vertices:
                if not isinstance(vertex_index, int):
                    raise TypeError('Objects of type int expected, however type {} was passed'.format(type(vertex_index)))

            self._vertices = vertices
        else:
            self._vertices = None

    @property
    def vertices(self):
        """A list of unsigned integers representing the indexes of an array of Vertex objects"""
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        self._vertices = vertices

    def blender_ordered_vertices(self):
        """Returns the vertices in an order that Blender expects."""
        # TODO
        pass

    def darksouls_ordered_vertices(self):
        """Returns the vertices in an order that Dark Souls expects."""
        # TODO
        pass
