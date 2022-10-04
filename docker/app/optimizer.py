"""This file is used for geometry optimization of a molecule"""
import scipy.optimize as sop
from predictor import get_default_prediction_model, predict_energy
from xyz_to_zmat import get_zmat_from_coordinates, get_coordinates_from_zmat

def optimize(coordinates,species,bonds):
    """optimization algorithm"""
    prediction_model = get_default_prediction_model()
    zparams,zconnect =  get_zmat_from_coordinates(coordinates)
    optim_params = sop.minimize(optimizer_oracle,zparams,method='Nelder-Mead',\
        args=(zconnect,species,bonds,prediction_model))
    optimized_coordinates = coordinates = get_coordinates_from_zmat(optim_params['x'],zconnect)
    optimized_energy = optim_params['fun']
    return optimized_coordinates, optimized_energy


def optimizer_oracle(zparams,zconnect,species,bonds,prediction_model):
    """input function to minimize for scipy optimize"""
    coordinates=get_coordinates_from_zmat(zparams, zconnect)
    energy = predict_energy(prediction_model,coordinates,species,bonds)
    return energy
