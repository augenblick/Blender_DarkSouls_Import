import pytest
from ds_import.vertex import Vertex
from ds_import.vector2 import Vector2
from ds_import.vector3 import Vector3


def test_vertex():
    # TODO: bone_weight assertions

    v = Vertex()

    assert isinstance(v.position, Vector3)
    assert isinstance(v.uv, Vector2)
    assert isinstance(v.lightmap_uv, Vector2)
    assert isinstance(v.normal, Vector3)

    v.position = Vector3()
    v.uv = Vector2()
    v.lightmap_uv = Vector2()
    v.normal = Vector3()

    assert isinstance(v.position, Vector3)
    assert isinstance(v.uv, Vector2)
    assert isinstance(v.lightmap_uv, Vector2)
    assert isinstance(v.normal, Vector3)

    with pytest.raises(TypeError):
        v.position = None
    with pytest.raises(TypeError):
        v.uv = None
    with pytest.raises(TypeError):
        v.lightmap_uv = None
    with pytest.raises(TypeError):
        v.normal = None

    with pytest.raises(TypeError):
        v.position = (0.0, 0.0, 0.0)
    with pytest.raises(TypeError):
        v.uv = (0.0, 0.0)
    with pytest.raises(TypeError):
        v.lightmap_uv = (0.0, 0.0)
    with pytest.raises(TypeError):
        v.normal = (0.0, 0.0, 0.0)

