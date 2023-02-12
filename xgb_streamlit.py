import pandas as pd
import numpy as np
import streamlit as st
import sklearn
import pickle


# df=pd.read_excel("crop_data_dict.xlsx")

def insect_classification(insect):
    if insect == 'Low':
        return 0
    elif insect == 'Average':
        return 1
    elif insect == 'High':
        return 2
    elif insect == 'Very High':
        return 3


xgb_loaded = pickle.load(open("transformer_reg.pkl", "rb"))


def page_1():
    st.title("Predict Damage to Crops")
    insects = st.selectbox("Insects in field (Estimate)", ("Low", "Average", "High", "Very High"))
    crop_type = st.selectbox("Crop Type", ("Kharif", "Rabi"))
    soil_type = st.selectbox("Soil Type", ("Alluvial", "Black-Cotton"))
    season = st.selectbox("Season", ('Winter', 'Monsoon', 'Summer'))
    pesticide_use_category = st.selectbox("Pesticide Category", ("Insecticide", 'Bactericides', 'Herbicides'))
    number_of_doses_in_a_week = st.number_input("Number of Doses in a Week", min_value=0, max_value=100, value=0)
    number_of_weeks_used = st.number_input("Number of Weeks Used", min_value=0, max_value=52, value=0)

    insects_label = insect_classification(insects)
    inp = pd.DataFrame(
        {'Crop_Type': crop_type, 'Soil_Type': soil_type, 'Pesticide_Use_Category': pesticide_use_category,
         'Number_Doses_Week': number_of_doses_in_a_week, 'Number_Weeks_Used': number_of_weeks_used,
         'Season': season, 'Insects_Labeled': insects_label})
    transformer = pickle.load(open("transformer_reg.pkl", "rb"))
    inp_transformed = transformer.transform(inp)
    inp_transformed_encoded = pd.DataFrame(inp_transformed, columns=transformer.get_feature_names_out())
    xgb = pickle.load(open("xgb_reg.pkl", "rb"))
    if st.button("Predict"):
        xgb.predict(inp_transformed_encoded)
        output = "Prediction Output"  #
        st.success(f"Output: {output}")


def page_2():
    st.title("Predict What Type of Crop is Best for your Soil")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select a Tool", ["Crop Damage", "Crop Production"])

    st.write("NAME OF OUR FARMER PROJECT")

    if page == "Crop Damage":
        page_1()


if __name__ == '__main__':
    main()