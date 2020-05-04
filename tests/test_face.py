import pytest
from ds_import.face import Face


def test_face():
    f = Face()

    assert isinstance(f.vertices, list)
    assert len(f.vertices) == 3
    for vertex_index in f.vertices:
        assert isinstance(vertex_index, int)
        assert vertex_index >= 0

    with pytest.raises(TypeError):
        f.vertices = None

    f.vertices = [8, 9, 10]

    with pytest.raises(TypeError):
        f.vertices = [8, 9, 'a']

    with pytest.raises(ValueError):
        f.vertices = [8, 9, 10, 11]

    f.vertices[0] = 20
    f.vertices[1] = 21
    f.vertices[2] = 23

    with pytest.raises(IndexError):
        f.vertices[3] = 24

    with pytest.raises(IndexError):
        assert f.vertices[3] == 0
