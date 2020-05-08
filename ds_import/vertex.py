from ds_import.vector2 import Vector2
from ds_import.vector3 import Vector3


class Vertex:
    """A class that represents a vertex in Blender"""

    def __init__(self):
        self._position = Vector3()
        self._uv = Vector2()
        self._lightmap_uv = Vector2()
        self._normal = Vector3()
        # TODO: double check bone_weight data type
        self._bone_weight = None

    # Encapsulation of position
    @property
    def position(self):
        """3D position of vertex."""
        return self._position

    @position.setter
    def position(self, position):
        if isinstance(position, Vector3):
            self._position = position
        else:
            raise TypeError('Expecting a Vector3 value.')

    # Encapsulation of uv
    @property
    def uv(self):
        """2D UV coordinates of vertex."""
        return self._uv

    @uv.setter
    def uv(self, uv):
        if isinstance(uv, Vector2):
            self._uv = uv
        else:
            raise TypeError('Expecting a Vector2 value.')

    # Encapsulation of lightmap_uv
    @property
    def lightmap_uv(self):
        """2D lightmap UV coordinates of vertex."""
        return self._lightmap_uv

    @lightmap_uv.setter
    def lightmap_uv(self, lightmap_uv):
        if isinstance(lightmap_uv, Vector2):
            self._lightmap_uv = lightmap_uv
        else:
            raise TypeError('Expecting a Vector2 value.')

    # Encapsulation of normal
    @property
    def normal(self):
        """3D normal of vertex."""
        return self._normal

    @normal.setter
    def normal(self, normal):
        if isinstance(normal, Vector3):
            self._normal = normal
        else:
            raise TypeError('Expecting a Vector3 value.')

    @property
    def bone_weight(self):
        # TODO: Do this correctly, this is just a placeholder.
        return self._bone_weight

    @bone_weight.setter
    def bone_weight(self, bone_weight):
        # TODO: data validation when known
        self._bone_weight = bone_weight

    def __str__(self):
        return f'position=({self.position}) ' \
               f'uv=({self.uv}) ' \
               f'lightmap_uv=({self.lightmap_uv}) ' \
               f'normal=({self.normal}) ' \
               f'bone_weight=({self.bone_weight}) '
