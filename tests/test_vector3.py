import pytest
from ds_import.vector3 import Vector3


def test_vector3_init():
    v = Vector3()
    assert v.x == 0
    assert v.y == 0
    assert v.z == 0
    assert isinstance(v.x, float)
    assert isinstance(v.y, float)
    assert isinstance(v.z, float)

    v = Vector3(1.0, 2.0, 3.0)
    assert v.x == 1
    assert v.y == 2
    assert v.z == 3
    assert isinstance(v.x, float)
    assert isinstance(v.y, float)
    assert isinstance(v.z, float)


@pytest.mark.parametrize('x,y,z,expected', [
    (0, 0, 0, TypeError),
    ('a', 'a', 'a', TypeError),
    ('a', 1, 1, TypeError),
    (1, 'a', 1, TypeError),
    ('a', 'a', 1, TypeError),
    (1, 1, 1, TypeError),
    (None, None, None, TypeError)
])
def test_vector3_init_exceptions(x, y, z, expected):
    with pytest.raises(expected):
        Vector3(x, y, z)


def test_vector3_xyz():
    v = Vector3()

    assert v.x == 0.0
    assert v.y == 0.0
    assert v.z == 0.0
    assert isinstance(v.x, float)
    assert isinstance(v.y, float)
    assert isinstance(v.z, float)

    v.x = 1.0
    v.y = 2.0
    v.z = 3.0

    assert v.x == 1.0
    assert v.y == 2.0
    assert v.z == 3.0
    assert isinstance(v.x, float)
    assert isinstance(v.y, float)
    assert isinstance(v.z, float)

    with pytest.raises(TypeError):
        v.x = 4
    with pytest.raises(TypeError):
        v.y = 5
    with pytest.raises(TypeError):
        v.z = 6

    assert v.x == 1.0
    assert v.y == 2.0
    assert v.z == 3.0
