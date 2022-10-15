from commands_database import build_dataset_commands_dict
from commands_database import load_commands_df
from commands_database import save_commands_dict
import ee
import geemap.foliumap as geemap


#Initialize GEE Credentials
try:
    ee.Initialize()

except ee.EEException as e:
    try:
        ee.Authenticate(auth_mode="appdefault")
        ee.Initialize()
        
    except ee.EEException as e:
        try:
            ee.Authenticate(auth_mode="gcloud")
            ee.Initialize()
    
        except:
            print("Google Earth Engine Credentials Not Verified")
            
             
             
#Build Most Recent Commands Dictionary
commands_dict = build_dataset_commands_dict()



#Save to Local Pickle File
save_commands_dict(commands_dict)


#Load Dictionary to Pandas DataFrame
commands_df = load_commands_df()
             
             
                      
#Validate Each Individual Dataset and Remove Any that Fail

fail_list = []
Map = geemap.Map()

#Test All Commands in Dataset for Validity
for index, rows in commands_df.iterrows():
    dataset_name = rows['Dataset']
    command_list = rows['Commands']

    for command in command_list:
        try:
            exec(command)
        
        except:
            if dataset_name not in fail_list:
                fail_list.append(dataset_name)
            pass
 
        
#Remove Failed Datasets
commands_df = commands_df[~commands_df.Dataset.isin(fail_list)]


#Replace Pickle File in Database
commands_df.to_pickle('validated_elevation_dataset_commands.pkl')
        

#Save Fail List to Another File
dataset_fails = pd.DataFrame(fail_list, columns = ["Datasets"])
dataset_fails.to_pickle("failed_datasets.pkl")