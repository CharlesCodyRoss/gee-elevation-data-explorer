from commands_database import load_commands_df
from dataset_search import dataset_search
import pandas as pd

def elevation_database_load():
    """
    Compiles and returns a Pandas dataframe that contains all dataset info needed to load and visualize
    the GEE datasets.
    """
    
    #Load The Local Commands Database and Create a List of Available Datasets
    commands_df = load_commands_df()
    dataset_list = commands_df['Dataset'].tolist()  
    
    
    #Perform a Dataset Search for Elevation Tagged GEE Datasets and Filter List from Available in the Commands Database
    elevation_info = dataset_search("elevation")
    delete_list = []
    
    for key in elevation_info.keys():
        if key not in dataset_list:
            if key not in delete_list:
                delete_list.append(key)
                
    for dataset in delete_list:
        del elevation_info[dataset]
    
    
    #Create a Pandas Dataframe from the Results and Add Commands        
    elevation_info_pd = pd.DataFrame.from_dict(elevation_info, orient = 'index').reset_index()
    elevation_info_pd['commands'] = commands_df['Commands']
    
    return elevation_info_pd