import pytest
from ds_import.model import Model
from ds_import.mesh import Mesh


def test_model():

    model = Model()
    assert len(model.meshes) == 0

    model.meshes = [Mesh()]
    assert len(model.meshes) == 1

    with pytest.raises(TypeError):
        model.meshes = Mesh()

    with pytest.raises(TypeError):
        model.meshes = [1, 2, 3]

