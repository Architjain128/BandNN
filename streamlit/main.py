from faulthandler import disable
import streamlit as st
import json
import requests

BASE_URL="http://127.0.0.1:8000/"

input_reference = {
    "species": ["C", "H", "H", "H", "C", "H", "H", "H"],
    "coordinates": [
        [0.00000000,  0.00000000, 0.77129800],
        [-0.50676600,   0.87777700,  1.15591600],
        [1.01356000,  -0.00001600, 1.15591600],
        [-0.50679400,  -0.87776100,   1.15591600],
        [0.00000000,   0.00000000,  -0.77129800],
        [0.50676600,   0.87777700,  -1.15591600],
        [0.50679400, -0.87776100, -1.15591600],
        [-1.01356000, -0.00001600, -1.15591600]
    ],
    "bond_connectivity_list": [
        [1, 2, 3, 4],
        [0],
        [0],
        [0],
        [5, 6, 7, 1],
        [4],
        [4],
        [4]
    ]
}

def displayPDF():
    for i in range(1,24):
        val="0000"+i.__str__()
        val=val[-4:]
        st.image(f'./media/info_page-{val}.jpg', use_column_width=True)

def no_page():
    '''
        404 page
    '''
    st.error("### Oops! 404")

def explore_page():
    '''
        Explore page
    '''
    st.write("""## Model Overview """)
    displayPDF()

def show_predict_energy_page():
    '''
        Predict Energy page
    '''
    st.write("## Predict Energy Page")
    st.write("### User Inputs")
    inp_data= st.text_area("Enter Molecule desciption here: ",height=150)
    st.caption("> \* Refer to input format in the sidebar")
    run = st.button(label="Predict Energy")
    if run:
        st.markdown("""---""")
        placeHolder=st.empty()
        with st.spinner("Hold On, working on it ..."):
            if inp_data:
                try:
                    inp_data=json.loads(inp_data)
                    response = requests.post(BASE_URL+"predictEnergy", json=inp_data)
                    with placeHolder.container():
                        st.write('### Predicted Energy')
                        st.header(response.json()['energy'])
                except:
                    placeHolder.error("OOPS something went wrong")
            else:
                placeHolder.error("Empty input fields")

def show_geometric_optimization_page():
    '''
        Geometric Optimization page
    '''
    st.write("## Geometric Optimization Page")
    # with st.form(key='my_form2'):
    st.write("### User Inputs")
    inp_data= st.text_area("Enter Molecule desciption here: ",height=150)
    st.caption("> \* Refer to input format in the sidebar")
    run = st.button(label="Optimize Geometry")
    if run:
        st.markdown("""---""")
        placeHolder=st.empty()
        with st.spinner("Hold On, working on it ..."):
            if inp_data:
                try:
                    inp_data=json.loads(inp_data)
                    response = requests.post(BASE_URL+"geometricOptimization", json=inp_data)
                    with placeHolder.container():
                        c1,c2=st.columns(2)
                        c1.write('### Optimized Coordinates:')
                        c1.json(response.json()['optimized_coordinates'])
                        # c1.json(input_reference)
                        c2.write('### Optimized Species:')
                        c2.header(response.json()['optimized_species'])
                        # c2.header(13454655364.04)
                except:
                    placeHolder.error("OOPS something went wrong")
            else:
                placeHolder.error("Empty input fields")

st.set_page_config(
    page_title="BAND NN",
    initial_sidebar_state="expanded",
)

# sidebar start
st.sidebar.header('Navigation')
page = st.sidebar.selectbox("Select the page you want to see", ["Predict Energy","Geometric Optimazation","Explore"])
st.sidebar.markdown("---")
st.sidebar.markdown("""### Input Format Example""")
st.sidebar.json(input_reference)
# sidebar end

st.title("BAND NN")
if page == "Explore":
    explore_page()
elif page == "Predict Energy":
    show_predict_energy_page()
elif page == "Geometric Optimazation":
    show_geometric_optimization_page()
else:
    no_page()