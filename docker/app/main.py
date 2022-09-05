from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from scripts.band import *

app = FastAPI()

class BANDInput(BaseModel):
    species: list[str]
    coordinates: list[list[float]]
    bond_connectivity_list: list[list[int]]

@app.get("/")
def read_root():
    return "Hello World"

@app.get("/creator") 
def read_item():
    return "Archit Jain & Pulkit Gupta"

@app.post("/predictEnergy")
def predictEnergy(data: BANDInput):
    return predict_energy_wrapper(data)

@app.post("/geometricOptimization")
def geometricOptimization(data: BANDInput):
    return geometricOptimization_wrapper(data)