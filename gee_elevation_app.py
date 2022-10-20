import streamlit as st
import ee
import geemap.foliumap as geemap
import pandas as pd
import json

from dataset_info import elevation_database_load
from dataset_search import display_description


#INTIALIZE GOOGLE EARTH ENGINE

#TITLE AND OPENING MESSAGE
st.title("Google Earth Engine Elevation Dataset Explorer")

opening_message = ("""
             <p style="font-size:22px">Welcome to the Google Earth Engine Elevation Data Explorer.  This application will allow you
             to easily browse the eleavation datasets provided by the Google Earth Engine Catalog and download elevation
             files from your desired locations.  Select a dataset from the drop down menu, select your desired area from
             the map, and download your file.</p>
             """)

st.markdown(opening_message, unsafe_allow_html=True)

st.write("")
st.write("")


#AUTHENTICATE THE GEE CREDENTIALS AND INITIALIZE
json_data = st.secrets["json_data"]
service_account = st.secrets["service_account"]

# Preparing values
json_object = json.loads(json_data, strict=False)
service_account = json_object['client_email']
json_object = json.dumps(json_object)


# Authorising the app
credentials = ee.ServiceAccountCredentials(service_account, key_data=json_object)
ee.Initialize(credentials)




#LOAD EXISITNG COMMAND DATASET
elevation_datasets = elevation_database_load()



#DISPLAY ELEVATION DATASETS IN DROP DOWN MENU
dataset_names = elevation_datasets['index'].tolist()

#Add Default Value to Top
dataset_list = ['Select Elevation Dataset']
for item in dataset_names:
    dataset_list.append(item)

#Display in Dropdown Box
dataset_selection = st.selectbox(
                        "",
                        dataset_list
                        )


#DISPLAY INFOMATION ON DATSET IF ITEM SELECTED
if dataset_selection != 'Select Elevation Dataset':
    
    #Filter Database on Selection
    dataset = elevation_datasets[elevation_datasets['index'] == dataset_selection]
    
    title = dataset.title.iloc[0]
    asset_url = dataset.asset_url.iloc[0]

    description = display_description(asset_url)
    
    #Display Description
    st.markdown(f"""<strong style="font-size:24px"> {title}</strong>""", unsafe_allow_html=True)
    
    st.markdown(description, unsafe_allow_html=True)
    
    st.write("")
    st.write("")

    
    
    #LOAD COMMANDS AND DISPLAY ON MAP
    st.write("")
    st.write("")

    Map = geemap.Map(Draw_export=True)
    
    
    #Load Commands from Selected Database
    commands = dataset.commands.iloc[0]
    
    for itr in range(len(commands)):
        exec(commands[itr])
     
    Map.to_streamlit(height = 500)
    
    
    
#DISPLAY EMPTY MAP IF NO SELECTION
elif dataset_selection == 'Select Elevation Dataset':
    #INITIALIZE MAP
    Map = geemap.Map(Draw_export=True)
    Map.to_streamlit(height = 500)
        
    