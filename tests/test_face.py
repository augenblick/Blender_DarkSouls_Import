import pytest
from ds_import.face import Face


def test_face():
    f = Face()

    assert isinstance(f.vertices, list)
    assert len(f.vertices) == 0

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


# test the __str__() method
@pytest.mark.parametrize('vertices', [
    [0, 0, 0],
    [1, 2, 3],
    pytest.param([1], marks=pytest.mark.xfail(raises=ValueError)),
    pytest.param([-1, 2, 3], marks=pytest.mark.xfail(raises=ValueError)),
    pytest.param([1.0, 1.0, 1.0], marks=pytest.mark.xfail(raises=TypeError)),
])
def test_str(vertices):
    face = Face()
    expected_string = f'vertices={vertices}'

    face.vertices = vertices

    print(face)
    assert str(face) == expected_string


def test_reset():
    face = Face([0, 1, 2])
    assert len(face.vertices) == 3

    face.reset()
    assert len(face.vertices) == 0
