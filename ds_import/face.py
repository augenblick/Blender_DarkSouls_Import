class Face:
    """A class that represents a triangular face in Blender."""

    def __init__(self, vertices=None):
        """

        :param vertices: List of unsigned ints, each representing the index of a list of Vertex objects.
        """
        if vertices is not None:
            self.vertices = vertices
        else:
            self.vertices = [0, 0, 0]

    @property
    def vertices(self):
        """A list of unsigned integers representing the indexes of an array of Vertex objects"""
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):

        # Verify the list is exactly 3 elements long
        if len(vertices) != 3:
            raise ValueError('List of three unsigned integers expected.')
        else:
            # Verify each element in the list is an unsigned int
            for vertex_index in vertices:
                if not isinstance(vertex_index, int):
                    raise TypeError('Objects of type int expected, however type {} was passed'.format(type(vertex_index)))
                else:
                    if vertex_index < 0:
                        raise ValueError('Expecting unsigned ints')
                    else:
                        self._vertices = vertices

    # TODO: Implement vertex order methods below.

    def blender_ordered_vertices(self):
        """Returns the vertices in an order that Blender expects."""
        pass

    def darksouls_ordered_vertices(self):
        """Returns the vertices in an order that Dark Souls expects."""
        pass
