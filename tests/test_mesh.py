import pytest
from ds_import.mesh import Mesh
from ds_import.face_set import FaceSet
from ds_import.vertex import Vertex
from ds_import.face import Face


def test_mesh():
    m = Mesh()
    assert len(m.vertices) == 0
    assert len(m.face_sets) == 0

    m.vertices = [Vertex(), Vertex(), Vertex()]
    assert len(m.vertices) == 3

    m.face_sets = [FaceSet()]
    assert len(m.face_sets) == 1

    with pytest.raises(ValueError):
        m.vertices = [Vertex(), Vertex()]

    with pytest.raises(TypeError):
        m.vertices = [Vertex(), Vertex(), 'fish']

    with pytest.raises(TypeError):
        m.face_sets = [Face(), Face()]


# test the __str__() method
def test_str():
    mesh = Mesh()
    expected_string = ''
    mesh.vertices = [Vertex(), Vertex(), Vertex()]

    face_set = FaceSet()
    face_set.faces = [Face(), Face()]

    mesh.face_sets = [face_set, face_set]

    for i in range(0, len(mesh.vertices)):
        expected_string += f'vertex[{i}]={mesh.vertices[i]}\n'

    for i in range(0, len(mesh.face_sets)):
        expected_string += f'face_set[{i}]={mesh.face_sets[i]}\n'

    print(mesh)
    assert str(mesh) == expected_string


def test_reset():
    mesh = Mesh()
    assert len(mesh.face_sets) == 0
    assert len(mesh.vertices) == 0

    mesh.face_sets.append(FaceSet())
    mesh.face_sets.append(FaceSet())
    mesh.vertices.append(Vertex())
    assert len(mesh.face_sets) == 2
    assert len(mesh.vertices) == 1

    mesh.reset()
    assert len(mesh.face_sets) == 0
    assert len(mesh.vertices) == 0
