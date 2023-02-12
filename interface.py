import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import xgboost
import sklearn
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

df=pd.read_excel("crop_data_dict.xlsx")

df.dropna(axis=0, how='any', inplace=True)
df['P/A']=df['Production']/df['Area']

df['Season'].str.strip()
df['District_Name'].str.strip()
df['Crop'].str.strip()

df['combined'] = df['District_Name'].astype(str) + df['Season'].astype(str) + df['Crop'].astype(str)

columns_remove=["Crop_Year","Area","Production"]
df.drop(columns_remove, axis=1, inplace=True)

df['combined']=df['combined'].apply(str)
df['combined'] = df['combined'].str.replace(' ', '')

hash_table = {}
for index, row in df.iterrows():
    # Insert the string-float mapping into the hash table
    hash_table[row['combined']] = row['P/A']

District_Names=list(df['District_Name'].unique())
seasons_unique=list(df['Season'].unique())
Crops=list(df['Crop'].unique())
Seasons={}
for name in District_Names:
    filter=df[df['District_Name']== name]
    Seasons[name]=filter['Season'].unique()

Crop= []
def insect_classification(insect):
    if insect == 'Low':
        return 0
    elif insect == 'Average':
        return 1
    elif insect == 'High':
        return 2
    elif insect == 'Very High':
        return 3

        
def Predict_Damage_to_Crops():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=UserWarning)
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
    
def page_2():
    st.title("Get Produce for you field")

    string1= st.selectbox("Choose a District", District_Names)
    string2 = st.selectbox("Choose a Season", Seasons[string1])
    filter=df[(df['District_Name']== string1) & (df['Season']== string2)]
    Crop=filter['Crop'].unique()
    string3 = st.selectbox("Choose a crop", Crop)
    Area= st.number_input("Enter your field area (in acres)")

    if string1 and string2 and string3:
        string4=string1+string2+string3
        string4=string4.replace(' ', '')
        rate=hash_table[string4]
        produce=rate*Area
        produce= round(produce, 3)
        rate=round(rate,3)
        left="Rate of Produce per acre {} ".format(rate)
        st.markdown(left)
        if(rate<1):
            st.markdown("**<span style='color:red; font-size:20px; ' >POOR</span>**", unsafe_allow_html=True)
        elif((rate>=1) & (rate<5)):
            st.markdown("<span style='color:blue; font-size:20px;'>GOOD</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color:green; font-size:20px;' >Amazing</span>", unsafe_allow_html=True)
        
        final="The amount of produce in your field is {} tonnes".format(produce)
        st.markdown("<h1 style='font-size:20px;'>{}</h1>".format(final), unsafe_allow_html=True)    
        
        
def Crop_recommendation():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=UserWarning)
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
    page = st.sidebar.selectbox("Select a Tool", ["Predict Damage to Crops", "Crop Production","Crop recommendation"])
    
    st.write("TEAM TIET")
    
    if page == "Predict Damage to Crops":
        Predict_Damage_to_Crops()
    elif page == "Crop Production":
        page_2()
    elif page == "Crop recommendation":
        Crop_recommendation()
    

if __name__ == '__main__':
    main()




