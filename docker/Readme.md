# BAND-NN
## How to run
### local server
```
    > pip3 install -r requirements.txt
    > cd ./app
    > uvicorn main:app --reload
```
### pylint
```
    > pylint ./file/path
```
### pytest
```
    > cd ./app
    > pytest
```
### docker
```
    > docker build . -t bandnn
    > docker run -d --name bandnnImage -p 80:80 bandnn
```
## File Structure
```
.
├── Dockerfile
├── app
│   ├── Readme.md
│   ├── __init__.py
│   ├── main.py
│   ├── scripts
│   │   ├── __init__.py
│   │   ├── band.py
│   │   ├── featurizer.py
│   │   ├── models.py
│   │   ├── optimizer.py
│   │   ├── predictor.py
│   │   └── xyz_to_zmat.py
│   ├── testFiles
│   │   ├── test_api.py
│   │   └── test_files.py
│   ├── trained_models
│   │   ├── angle_model.h5
│   │   ├── bond_model.h5
│   │   ├── dihedrals_model.h5
│   │   └── nonbonds_model.h5
│   └── weights
│       ├── angle_weights.h5
│       ├── bond_weights.h4
│       ├── bond_weights.h5
│       ├── dihedral_weights.h5
│       └── nonbonds_weights.h5
└── requirements.txt
```