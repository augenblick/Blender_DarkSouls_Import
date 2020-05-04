import pytest
from ds_import.vector2 import Vector2


def test_vector2_init():
    v = Vector2()
    assert v.x == 0
    assert v.y == 0
    assert isinstance(v.x, float)
    assert isinstance(v.y, float)

    v = Vector2(1.0, 2.0)
    assert v.x == 1
    assert v.y == 2
    assert isinstance(v.x, float)
    assert isinstance(v.y, float)


@pytest.mark.parametrize('x,y,expected', [
    (0, 0, TypeError),
    ('a', 'a', TypeError),
    ('a', 1, TypeError),
    (1, 'a', TypeError),
    (1, 1, TypeError),
    (None, None, TypeError)
])
def test_vector2_init_exceptions(x, y, expected):
    with pytest.raises(expected):
        Vector2(x, y)


def test_vector2_xy():
    v = Vector2()

    assert v.x == 0.0
    assert v.y == 0.0
    assert isinstance(v.x, float)
    assert isinstance(v.y, float)

    v.x = 1.0
    v.y = 2.0

    assert v.x == 1.0
    assert v.y == 2.0
    assert isinstance(v.x, float)
    assert isinstance(v.y, float)

    with pytest.raises(TypeError):
        v.x = 3
    with pytest.raises(TypeError):
        v.y = 4

    assert v.x == 1.0
    assert v.y == 2.0