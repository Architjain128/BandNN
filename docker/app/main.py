"""FastAPI server"""
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from scripts.band import predict_energy_wrapper, geometric_optimization_wrapper

app = FastAPI()
class BANDInput(BaseModel):
    """Input format for BAND"""
    species: List[str]
    coordinates: List[list[float]]
    bond_connectivity_list: List[List[int]]

    def __init__(self, species, coordinates, bond_connectivity_list):
        super().__init__(species=species, coordinates=coordinates,
            bond_connectivity_list=bond_connectivity_list)
        self.species = species
        self.coordinates = coordinates
        self.bond_connectivity_list = bond_connectivity_list

    def print_species(self):
        """print band input species"""
        return f"species: {self.species}"

    def print_coordinates(self):
        """print band input coordinates"""
        return f"coordinates: {self.coordinates}"

    def print_bond_connectivity_list(self):
        """print band input bond connectivity list"""
        return f"bond_connectivity_list: {self.bond_connectivity_list}"


@app.get("/")
def read_root():
    """root"""
    return "Hello World"

@app.get("/creator")
def read_item():
    """This is a function to return the creator of the API"""
    return {"server":"Archit Jain & Pulkit Gupta"}

@app.post("/predictEnergy")
def predict_energy(data: BANDInput):
    """predict_energy function"""
    return predict_energy_wrapper(data)

@app.post("/geometricOptimization")
def geometric_optimization(data: BANDInput):
    """geometric_optimization function"""
    return geometric_optimization_wrapper(data)
