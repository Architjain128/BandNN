from .predictor import *
from .optimizer import *

# Input format
mock_input = {
    "species": ["C", "H", "H", "H", "C", "H", "H", "H"],
    "coordinates": [
        [0.00000000,  0.00000000, 0.77129800],
        [-0.50676600,   0.87777700,  1.15591600],
        [1.01356000,  -0.00001600, 1.15591600],
        [-0.50679400,  -0.87776100,   1.15591600],
        [0.00000000,   0.00000000,  -0.77129800],
        [0.50676600,   0.87777700,  -1.15591600],
        [0.50679400, -0.87776100, -1.15591600],
        [-1.01356000, -0.00001600, -1.15591600],
    ],
    "bond_connectivity_list": [
        [1, 2, 3, 4],
        [0],
        [0],
        [0],
        [5, 6, 7, 1],
        [4],
        [4],
        [4],
    ],
}

def validate_input(data):
    for key in ["species", "coordinates", "bond_connectivity_list"]:
        if key not in data:
            raise ValueError("Missing required key: {}".format(key))

def predict_energy_wrapper(data):
    validate_input(data)
    prediction_model = get_default_prediction_model()
    energy = predict_energy(prediction_model,data.coordinates,data.species,data.bond_connectivity_list)
    return energy

def geometricOptimization_wrapper(data):
    # validate_input(data)
    return optimize(data.coordinates,data.species,data.bond_connectivity_list)

