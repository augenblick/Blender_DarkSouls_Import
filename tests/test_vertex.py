import pytest
from ds_import.vertex import Vertex
from ds_import.vector2 import Vector2
from ds_import.vector3 import Vector3


def test_vertex():
    # TODO: bone_weight assertions

    v = Vertex()

    assert v.position is None
    assert v.uv is None
    assert v.lightmap_uv is None
    assert v.normal is None

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


# test the __str__() method
@pytest.mark.parametrize('position, uv, lightmap_uv, normal, bone_weight', [
    (Vector3(), Vector2(), Vector2(), Vector3(), None),
    (Vector3(0.0, 1.0, -25.2), Vector2(1.0, 0.0), Vector2(1.0, 0.0), Vector3(1.0, 1.0, 1.0), None),
])
def test_str(position, uv, lightmap_uv, normal, bone_weight):
    vertex = Vertex()
    vertex.position = position
    vertex.uv = uv
    vertex.lightmap_uv = lightmap_uv
    vertex.normal = normal
    vertex.bone_weight = bone_weight

    expected_string = f'position=({position}) ' \
                      f'uv=({uv}) ' \
                      f'lightmap_uv=({lightmap_uv}) ' \
                      f'normal=({normal}) ' \
                      f'bone_weight=({bone_weight}) '

    assert str(vertex) == expected_string


def test_reset():
    vertex = Vertex(Vector3(0.0, 1.0, -25.2), Vector2(1.0, 0.0), Vector2(1.0, 0.0), Vector3(1.0, 1.0, 1.0), None)
    assert vertex.position.x == 0.0
    assert vertex.position.y == 1.0
    assert vertex.position.z == -25.2
    assert vertex.uv.x == 1.0
    assert vertex.uv.y == 0.0
    assert vertex.lightmap_uv.x == 1.0
    assert vertex.lightmap_uv.y == 0.0
    assert vertex.normal.x == 1.0
    assert vertex.normal.y == 1.0
    assert vertex.normal.z == 1.0
    assert vertex.bone_weight == None

    vertex.reset()

    assert vertex.position is None
    assert vertex.uv is None
    assert vertex.lightmap_uv is None
    assert vertex.normal is None
    assert vertex.bone_weight is None