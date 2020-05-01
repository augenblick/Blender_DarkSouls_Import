from vertex import Vertex


class Face:
    """A class that represents a triangular face in Blender."""

    vertices = []

    def __init__(self, vertices=None):
        """

        :param vertices: List of three Vertex objects.
        """
        if vertices is not None:
            # validate vertices
            if len(vertices) == 3:
                raise ValueError('Three vertices expected.')
            for v in vertices:
                if not isinstance(v, Vertex):
                    raise TypeError('Objects of type Vertex expected, however type {} was passed'.format(type(m)))

            self.vertices = vertices

    def blender_ordered_vertices(self):
        """Returns the vertices in an order that Blender expects."""
        # TODO
        pass

    def darksouls_ordered_vertices(self):
        """Returns the vertices in an order that Dark Souls expects."""
        # TODO
        pass
