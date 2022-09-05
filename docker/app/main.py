from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/check")
def read_root():
    return "All Ok"

@app.get("/creator")
def read_item():
    return "Archit Jain & Pulkit Gupta"

@app.post("/predictEnergy")
def predictEnergy():
    return "Predicted Energy"

@app.post("/geometricOptimization")
def geometricOptimization():
    return "Optimized Geometry"