"""This file is used for genrating neural model architecture"""
from keras.models import Sequential
from keras.layers import Dense

def get_bonds_model():
    """generates neural model for bonds"""
    model = Sequential()
    model.add(Dense(128, activation='relu', input_dim=17))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(1, activation='linear'))
    return model

def get_angles_model():
    """generates neural model for angles"""
    model = Sequential()
    model.add(Dense(128, activation='relu', input_dim=27))
    model.add(Dense(350, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(1, activation='linear'))
    return model

def get_nonbonds_model():
    """generates neural model for non-bonds"""
    model = Sequential()
    model.add(Dense(128, activation='relu', input_dim=17))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(1, activation='linear'))
    return model

def get_dihedrals_model():
    """generates neural model for dihedrals"""
    model = Sequential()
    model.add(Dense(128, activation='relu', input_dim=38))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(1, activation='linear'))
    return model
