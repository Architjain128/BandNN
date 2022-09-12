"""Main file"""
from fastapi import FastAPI
from pydantic import BaseModel
from scripts.band import predict_energy_wrapper, geometric_optimization_wrapper

app = FastAPI()

class BANDInput(BaseModel):
    species: list[str]
    coordinates: list[list[float]]
    bond_connectivity_list: list[list[int]]

@app.get("/")
def read_root():
    """root"""
    return "Hello World"

@app.get("/creator")
def read_item():
    """This is a function to return the creator of the API"""
    return "Archit Jain & Pulkit Gupta"

@app.post("/predictEnergy")
def predict_energy(data: BANDInput):
    """predict_energy function"""
    return predict_energy_wrapper(data)

@app.post("/geometricOptimization")
def geometric_optimization(data: BANDInput):
    """geometric_optimization function"""
    return geometric_optimization_wrapper(data)
