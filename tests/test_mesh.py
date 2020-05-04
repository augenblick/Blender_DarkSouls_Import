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