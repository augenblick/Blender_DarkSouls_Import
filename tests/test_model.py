import pytest
from ds_import.model import Model
from ds_import.mesh import Mesh
from ds_import.face import Face
from ds_import.face_set import FaceSet
from ds_import.vertex import Vertex


def test_model():
    model = Model()
    assert len(model.meshes) == 0

    model.meshes = [Mesh()]
    assert len(model.meshes) == 1

    with pytest.raises(TypeError):
        model.meshes = Mesh()

    with pytest.raises(TypeError):
        model.meshes = [1, 2, 3]


# test the __str__() method
def test_str():
    model = Model()

    mesh = Mesh()
    mesh.vertices = [Vertex(), Vertex(), Vertex()]

    face_set = FaceSet(faces=[Face(), Face(), Face()])
    mesh.face_sets = [face_set]

    model.meshes.append(mesh)

    print(model)


def test_reset():
    model = Model()
    assert len(model.meshes) == 0

    model.meshes.append(Mesh())
    assert len(model.meshes) == 1

    model.reset()
    assert len(model.meshes) == 0
