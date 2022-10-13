"""This file is used for predicting energy of a molecule"""
from .models import get_angles_model, get_bonds_model, get_nonbonds_model, get_dihedrals_model
from .featurizer import get_features, np

def get_default_prediction_model():
    """loading neural models for BAND"""
    bonds_model = get_bonds_model()
    bonds_model.load_weights('app/weights/bond_weights.h5')

    angles_model = get_angles_model()
    angles_model.load_weights('app/weights/angle_weights.h5')

    nonbonds_model = get_nonbonds_model()
    nonbonds_model.load_weights('app/weights/nonbonds_weights.h5')

    dihedralangles_model = get_dihedrals_model()
    dihedralangles_model.load_weights('app/weights/dihedral_weights.h5')

    model = {}
    model['bonds'] = bonds_model
    model['angles'] = angles_model
    model['nonbonds'] = nonbonds_model
    model['dihedrals'] = dihedralangles_model
    return model


def predict_energy(model,coordinates,species,bonds):
    """Predict energy for molecule"""
    features = get_features(coordinates, species, bonds)
    bond_energies = model['bonds'].predict(features['bonds'])
    angle_energies = model['angles'].predict(features['angles'])
    nonbond_energies = model['nonbonds'].predict(features['nonbonds'])
    dihedral_energies = model['dihedrals'].predict(features['dihedrals'])
    energy = -1*(np.sum(bond_energies) + np.sum(angle_energies) + np.sum(nonbond_energies)\
         + np.sum(dihedral_energies))
    return energy
