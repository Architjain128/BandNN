# BAND-NN
## How to run
### Local server FastAPI server
```
    > cd ./bash 
    > ./run.sh
```
### Pylint
```
    > cd ./bash 
    > ./pylint.sh
```
### Pytest
```
    > cd ./bash
    > ./pytest.sh
```
### Streamlit frontend
```
    > cd ./bash
    > ./streamlit.sh
```
### Docker for FastAPI server
```
    > cd ./bash
    > ./docker.sh
```

## File Structure
```
..
├── Dockerfile
├── Readme.md
├── app
│   ├── __init__.py
│   ├── band.py
│   ├── featurizer.py
│   ├── main.py
│   ├── models.py
│   ├── optimizer.py
│   ├── predictor.py
│   ├── testFiles
│   │   ├── test_api.py
│   │   └── test_files.py
│   ├── trained_models
│   │   ├── angle_model.h5
│   │   ├── bond_model.h5
│   │   ├── dihedrals_model.h5
│   │   └── nonbonds_model.h5
│   ├── weights
│   │   ├── angle_weights.h5
│   │   ├── bond_weights.h4
│   │   ├── bond_weights.h5
│   │   ├── dihedral_weights.h5
│   │   └── nonbonds_weights.h5
│   └── xyz_to_zmat.py
├── bash
│   ├── docker.sh
│   ├── pylint.sh
│   ├── pytest.sh
│   ├── run.sh
│   └── streamlit.sh
├── requirements.txt
└── streamlit
    ├── main.py
    └── media
        ├── info_page-0001.jpg
        ...
        └── info_page-0024.jpg
```

## Things to check
+ ### by default the url is set to hosted docker server `http://localhost/`
+ ### if you want to run the local server, change the url accordingly 
    + Change `BASE_URL` in `app/testFiles/test_api.py` for api testing 
    + Change `BACKEND_BASE_URL` in `streamlit/main.py` for backend url 