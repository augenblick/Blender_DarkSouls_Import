import pytest
from ds_import.face_set import FaceSet
from ds_import.face import Face


def test_face_set():
    fs = FaceSet()

    assert len(fs.faces) == 0

    fs.faces = [Face()]

    assert len(fs.faces) == 1

    with pytest.raises(TypeError):
        fs.faces = None

    with pytest.raises(TypeError):
        fs.faces = 321

    with pytest.raises(TypeError):
        fs.faces = [1]

    with pytest.raises(TypeError):
        fs.faces = Face()