import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import xgboost
import sklearn
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

def insect_classification(insect):
    if insect == 'Low':
        return 0
    elif insect == 'Average':
        return 1
    elif insect == 'High':
        return 2
    elif insect == 'Very High':
        return 3


# xgb_loaded = pickle.load(open("transformer_reg.pkl", "rb"))


def page_1():
    st.title("Predict Damage to Crops")
    insects = st.selectbox("Insects in field (Estimate)", ("Low", "Average", "High", "Very High"))
    crop_type = st.selectbox("Crop Type", ("Kharif", "Rabi"))
    soil_type = st.selectbox("Soil Type", ("Alluvial", "Black-Cotton"))
    season = st.selectbox("Season", ('Winter', 'Monsoon', 'Summer'))
    pesticide_use_category = st.selectbox("Pesticide Category", ('Herbicides', 'Bactericides', 'Insecticides'))
    number_of_doses_in_a_week = st.number_input("Number of Doses in a Week", min_value=0, max_value=100, value=0)
    number_of_weeks_used = st.number_input("Number of Weeks Used", min_value=0, max_value=52, value=0)

    
    insects_label = insect_classification(insects)
    inp = pd.DataFrame(
        {'Crop_Type': [crop_type], 'Soil_Type': [soil_type], 'Pesticide_Use_Category': [pesticide_use_category],
         'Number_Doses_Week': [number_of_doses_in_a_week], 'Number_Weeks_Used': [number_of_weeks_used],
         'Season': [season], 'Insects_Labeled': [insects_label]})
    
    transformer = pickle.load(open("transformer_reg.pkl", "rb"))
    inp_transformed = transformer.transform(inp)
    inp_transformed_encoded = pd.DataFrame(inp_transformed, columns=transformer.get_feature_names_out())
    xgb = pickle.load(open("xgb_reg.pkl", "rb"))
    
    print(inp)
    if st.button("Predict"):
        output = xgb.predict(inp_transformed_encoded) 
        # print(output)
        output = output[0]
        if output == 'Minimal Damage':
            st.success(output)
        elif output == 'Partial Damage':
            st.warning(output, icon="⚠️")
        elif output == 'Significant Damage':
            st.warning(output, icon='💀')
        
        
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
        
        
    