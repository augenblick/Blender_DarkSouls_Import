from vector2 import Vector2
from vector3 import Vector3


class Vertex:
    """A class that represents a vertex in Blender"""

    position = Vector3()
    uv = Vector2()
    lightmap_uv = Vector2()
    normal = Vector3()
    # TODO: double check bone_weight data type
    bone_weight = 0.0
