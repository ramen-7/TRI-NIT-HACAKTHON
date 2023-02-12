import pandas as pd
import numpy as np
import streamlit as st

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
# for name in District_Names:
#     for name2 in seasons_unique:
#         filter=df[(df['District_Name']== name) & (df['Season']== name2)]
#         Crop=filter['Crop'].unique()
        
def page_1():
    st.write("This is page 1")
    st.write("This is a sample text in page 1")
# Saara python ka code yaha daal de
    
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




