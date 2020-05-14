from ds_import.mesh import Mesh


class Model:
    """A class that represents a Model in Blender."""

    def __init__(self, meshes=None):
        """

        :param meshes: List of Mesh objects.
        """

        self._meshes = []

        if meshes is not None:
            self.meshes = meshes

    @property
    def meshes(self):
        """A list of Mesh objects."""
        return self._meshes

    @meshes.setter
    def meshes(self, meshes):
        if not isinstance(meshes, list):
            raise TypeError("Object of type list expected, however type {} was passed".format(type(meshes)))
        for mesh in meshes:
            if not isinstance(mesh, Mesh):
                raise TypeError("Object of type Mesh expected, however type {} was passed".format(type(mesh)))

        self._meshes = meshes

    def __str__(self):
        return_string = ''

        for i in range(0, len(self.meshes)):
            return_string += f'mesh[{i}]={self.meshes[i]}\n'

        return return_string