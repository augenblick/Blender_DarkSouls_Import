from mesh import Mesh

class Model:
    """A class that represents a Model in Blender."""

    meshes = []

    def __init__(self, meshes=None):
        """

        :param meshes: List of Mesh objects.
        """

        # validate meshes
        for m in meshes:
            if not isinstance(m, Mesh):
                raise TypeError("Objects of type Mesh expected, however type {} was passed".format(type(m)))

        self.meshes = meshes