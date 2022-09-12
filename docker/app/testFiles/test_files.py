"""file exists test"""
import os
import pytest

@pytest.mark.parametrize("file", ["./weights/bond_weights.h5",
                                "./weights/angle_weights.h5",
                                "./weights/nonbonds_weights.h5",
                                "./weights/dihedral_weights.h5"])
def test_weight_file(file):
    """test for weight file"""
    assert os.path.isfile(file)

@pytest.mark.parametrize("file", ["./trained_models/bond_model.h5",
                                "./trained_models/angle_model.h5",
                                "./trained_models/nonbonds_model.h5",
                                "./trained_models/dihedrals_model.h5"])
def test_model_file(file):
    """test for model file"""
    assert os.path.isfile(file)

@pytest.mark.parametrize("file", ["./scripts/predictor.py",
                                "./scripts/optimizer.py",
                                "./scripts/featurizer.py",
                                "./scripts/models.py",
                                "./scripts/band.py",
                                "./scripts/xyz_to_zmat.py",
                                "./main.py"])
def test_script_file(file):
    """test for script file"""
    assert os.path.isfile(file)
