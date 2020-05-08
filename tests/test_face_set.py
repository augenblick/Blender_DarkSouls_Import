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


# test the __str__() method
def test_str():
    face_set = FaceSet()
    expected_string = ''

    test_faces = [Face(), Face(), Face()]

    face_set.faces = test_faces

    for i in range(0, len(face_set.faces)):
        expected_string += f'face[{i}]={test_faces[i]}\n'

    print(face_set)
    assert str(face_set) == expected_string
