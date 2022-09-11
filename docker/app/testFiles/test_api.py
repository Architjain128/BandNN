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
        "optimized_coordinates": [
            [
                0.0,
                0.0,
                0.0
            ],
            [
                1.1985448415367228,
                0.0,
                0.0
            ],
            [
                -0.5291979761742501,
                0.9044143976967525,
                0.0
            ],
            [
                -0.3955784848256375,
                -0.5847691241021874,
                0.7770776465543114
            ],
            [
                0.48615820969371526,
                -0.6962468293219094,
                -1.1533796418045001
            ],
            [
                0.935003057775518,
                -0.07009699855725882,
                -1.832340716326718
            ],
            [
                -0.4614761913366452,
                -1.1679166458199854,
                -1.4934791634343791
            ],
            [
                1.0123795020219943,
                -1.6308257565857425,
                -0.8513356176046953
            ]
        ],
        "optimized_energy": -789.4498901367188
    }
    response = requests.post(base_url+"/geometricOptimization",json=mock_input)
    assert response.status_code == 200
    assert response.json()["optimized_coordinates"] == output_data["optimized_coordinates"]
    assert response.json()["optimized_energy"] == output_data["optimized_energy"]