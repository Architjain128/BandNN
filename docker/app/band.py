"""wrapper functions file"""
from .predictor import get_default_prediction_model, predict_energy
from .optimizer import optimize

def predict_energy_wrapper(data):
    """wrapper for predict_energy function"""
    prediction_model = get_default_prediction_model()
    energy = predict_energy(prediction_model,
        data.coordinates,data.species,data.bond_connectivity_list)
    return {"energy":energy}

def geometric_optimization_wrapper(data):
    """wrapper for geometric optimization function"""
    optimized_coordinates, optimized_energy=\
        optimize(data.coordinates,data.species,
            data.bond_connectivity_list)
    val= {"optimized_coordinates":optimized_coordinates.tolist(),
        "optimized_energy":optimized_energy}
    return val
