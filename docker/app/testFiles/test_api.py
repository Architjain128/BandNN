import imp
import json
import requests
import numpy as np
from urllib import response

base_url="http://127.0.0.1:8000"

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

def test_root():
    response = requests.get(base_url)
    assert response.status_code == 200
    assert response.json() == "Hello World"

def test_creator():
    response = requests.get(base_url+"/creator")
    assert response.status_code == 200
    assert response.json() == "Archit Jain & Pulkit Gupta"

def test_energy_prediction():
    response = requests.post(base_url+"/predictEnergy",json=mock_input)
    assert response.status_code == 200
    assert response.json() == {"energy": -712.6749267578125}

def test_geometry_optimization():
    output_data = {
        'optimized_coordinates': [
            [ 0.        ,  0.        ,  0.        ],
            [ 1.19854484,  0.        ,  0.        ],
            [-0.52919798,  0.9044144 ,  0.        ],
            [-0.39557848, -0.58476912,  0.77707765],
            [ 0.48615821, -0.69624683, -1.15337964],
            [ 0.93500306, -0.070097  , -1.83234072],
            [-0.46147619, -1.16791665, -1.49347916],
            [ 1.0123795 , -1.63082576, -0.85133562]
        ],
        'optimized_energy': -789.4498901367188
    }
    response = requests.post(base_url+"/geometricOptimization",json=mock_input)
    assert response.status_code == 200
    assert response.json()["optimized_coordinates"].all() == np.array(output_data["optimized_coordinates"]).all()
    assert response.json()["optimized_energy"] == output_data["optimized_energy"]