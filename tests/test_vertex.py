import pytest
from contextlib import nullcontext as does_not_raise
from ds_import.vertex import Vertex


@pytest.mark.parametrize(('x', 'y', 'z', 'expected_exception'), [
    ('a', 'b', 'c', pytest.raises(TypeError)),
    (0, 0, 0, pytest.raises(TypeError)),
    (0, 0, 0, does_not_raise),
])
def test_init_type_errors(x, y, z, expectation):
    with expectation:
        v = Vertex(x, y, z)


if __name__ == '__main__':
    pytest.main()














