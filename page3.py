import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import xgboost
import sklearn
import pickle
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)


def page_1():
    df=pd.read_csv('Crop_recommendation.csv')
    st.title("Predict What Type of Crop is Best for your Soil")
    N = st.number_input("Nitrogen (Ratio in Soil)", min_value=0, max_value=100, value=0)
    P = st.number_input("Phosphorus (Ratio in Soil)", min_value=0, max_value=100, value=0)
    K = st.number_input("Potassium (Ratio in Soil)", min_value=0, max_value=100, value=0)
    T = st.number_input("Temperature in (Celsius)", min_value=0, max_value=45, value=0, format="%.2f")
    H = st.number_input("Humidity (%)", min_value=0, max_value=100, value=0, format="%.2f")
    ph = st.number_input("ph Level", min_value=0, max_value=10, value=0, format="%.2f")
    rainfall = st.number_input("Rainfall (in mm)", min_value=0, max_value=300, value=0, format="%.2f")
    model= pickle.load(open("soil_details_crop_classifier.pkl", "rb"))
    
    c=df.label.astype('category')
    targets = dict(enumerate(c.cat.categories))
    
    inp = pd.DataFrame({'N': [N], 'P': [P], 'K': [K], 'temperature': [T], 'humidity': [H], 'ph': [ph], 'rainfall': [rainfall]})
    if st.button("Predict"):
        model.predict(inp)
        output = model.predict(inp)  
        st.write(f"Output: {targets[output[0]]}")
        
        
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select a Tool", ["Page 1", "Crop Production"])
    
    st.write("NAME OF OUR FARMER PROJECT")
    
    if page == "Page 1":
        page_1()
    elif page == "Crop Production":
        page_2()
    

if __name__ == '__main__':
    main()
