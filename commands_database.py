from dataset_search import dataset_search
import requests
from bs4 import BeautifulSoup
import pandas as pd



#Remove Comments from Strings When Building Commmand Lists
def comment_remover(entry):
    """
    Pull the comment from a line and remove it from the string
    """

    period_check = ""
    remove = ""
    index_count = 0

    while "." != period_check:
        period_check = entry[index_count]
        remove = remove + entry[index_count]
        index_count = index_count + 1
        
    edit_command = entry.replace(remove, '').lstrip()
    
    #Set Command to Control for Mosaic Remainer
    if "mosaic(). " in edit_command:
        edit_command = edit_command.replace("mosaic(). ", '')


    return edit_command





#Remove Backward Slash From Commands, Must be Used After The Inital Comment Remover
def blank_space_remover(entry):
    """
    Certain commands have large gaps in them and need to be removed for the command to work.  This
    function will remove those gaps.
    """

    twenty_nine_blank_space = "                             ."
    four_blank_space = "    ."
    two_blank_space = "  ."
    
    if twenty_nine_blank_space in entry:
        edit_command = entry.replace(twenty_nine_blank_space, '.')
        
    elif four_blank_space in entry:
        edit_command = entry.replace(four_blank_space, '.')
        
    elif two_blank_space in entry:
        edit_command = entry.replace(two_blank_space, '.')
    
    else:
        edit_command = entry
        
    
    return edit_command





#Add String Comments to Keywords
def string_comments_on_keywords(entry):
    """
    Certain keywords need to be contained in strings when transforming scrape commands to python commands.
    This function will analyze the entry to see if it matches one of the keywords and then will wrap 
    that keyword with string comments.
    """
    
    keyword_list = [
        'palette',
        'color',
        'bands',
        'min',
        'max',
        'gamma',
        'pointSize',
        'filter_index'
    ]
    
    edit_string = entry

    for keyword in keyword_list:
        
        if keyword in entry:
            edit_string = edit_string.replace(keyword, f"'{keyword}'")
        
        else:
            pass
            
    return edit_string





#If Two Commands in the Same Line, Split and Return Both
def split_commands(entry):
    #Find Place of Second Equal Sign
    second_equal_sign_index = 0
    equal_counter = 0

    while equal_counter != 2:
        place = entry[second_equal_sign_index]
        
        if place == "=":
            equal_counter += 1
            
        second_equal_sign_index += 1
        
        
    #Locate Split Between Commands
    middle_index = second_equal_sign_index - 1
    space_counter = 0

    while space_counter != 2:
        head_back = entry[middle_index]
        
        if head_back == " ":
            space_counter += 1
        
        middle_index += -1


    #Move Forward One to Find the Space    
    middle_index = middle_index + 1

    
    #Split Found, Separate the Two Commands
    first_command = entry[:middle_index]
    second_command = entry[middle_index + 1:]
    
        
    return first_command, second_command




#Pull List of Elevation Datasets, Scrape Commands from GEE, and Convet to Python Commands
def build_dataset_commands_dict():
    """
    Locate a list of datasets with "elevation" tags from Google Earth Engine and scrape their javascript loading
    commands.  Javascript commands are converted into python code and then saved to a dictionary, the dictionary
    is then saved to a csv file for later use.
    """
    
    #Grab the List of Datasets with Elevation
    print("Grabbing List of Elevation Datasets")
    
    dataset_list = dataset_search('elevation')

    dataset_asset_dict = {}

    for key,values in dataset_list.items():
        dataset_asset_dict[key] = values['asset_url']

    
    
    #Scrape GEE for the JS Commands and Save to Dicitonary
    print("Scrapping GEE for Javascript Commands")
    
    js_commands_dict = {}

    for key, value in dataset_asset_dict.items():
        
        #Retrevie the Webpage
        response = requests.get(value)
        content = response.content
        
        #Convert Webapge to BS Item
        asset_soup = BeautifulSoup(content, 'html.parser')

        #Grab Commands from Page
        js = asset_soup.find("pre").text
        
        #Add JS Item to Dictionary
        js_commands_dict[key] = js
        
     
        
    #Conduct the initial cleaning of the javascript commands and place into new dictionary
    print("Perfoming Initial Command Clean")
    
    command_list_dict = {}

    for key, value in js_commands_dict.items():
        #Initial Edit of Strings, Remove Newlines, Var, and Split by ;
        string_command_list = value.replace("\n",'').replace("var",'').strip(" ").split(";")
        
        #Add Inital Command Edit to Dictionary
        command_list_dict[key] = (string_command_list)
        
        
        
    #Run through the previous dictionary and provide further edits of the individual commands.
    print("Perfoming Final Command Clean")
    
    instructions_list = [
        'Remove Comments',
        'Remove Leading and Trailing Spaces',
        'Remove Large Blank Spaces',
        'Place Strings on Keywords',
        "Separate Variables",
        "Remove Empty Entries"
    ]



    #Create Empty Storage Dictionary
    commands_dict = {}


    #Cycle Throug Instruction List and Perform Cleaning Steps
    for step in instructions_list:
        
        #Clean Comments from Lines
        if step == "Remove Comments":
            for key, values in command_list_dict.items():
                command_list = []
                for command in values:
                    if "//" in command and command != None:
                        comments_removed = comment_remover(command)
                        command_list.append(comments_removed)

                    else:
                        command_list.append(command)
                
                #Update Dictionary
                commands_dict[key] = command_list
        
                
        #Remove Empty Spaces at Beginning and Ending of Command        
        elif step == "Remove Leading and Trailing Spaces":
            for key, values in commands_dict.items():
                command_list = []
                for command in values:
                    strip_command = command.strip()
                    command_list.append(strip_command)
                    
                #Update Dictionary
                commands_dict[key] = command_list
        
                    
        #Remove Large Spaces in Commands            
        elif step == "Remove Large Blank Spaces":
            for key, values in commands_dict.items():
                command_list = []
                for command in values:
                    remove_blanks = blank_space_remover(command)
                    command_list.append(remove_blanks)
                    
                #Update Dictionary
                commands_dict[key] = command_list
                
        
        #Place Strings on Certain Keywords            
        elif step == "Place Strings on Keywords":
            for key, values in commands_dict.items():
                command_list = []
                for command in values:
                    edit_keywords = string_comments_on_keywords(command)
                    command_list.append(edit_keywords)
                
                #Update Dictionary
                commands_dict[key] = command_list
                
                
        #Place Strings on Certain Keywords            
        elif step == "Separate Variables":
            for key, values in commands_dict.items():
                command_list = []
                for command in values:
                    if command.count('=') >= 2:
                        first, second = split_commands(command)
                        command_list.append(first)
                        command_list.append(second)
                    else:
                        command_list.append(command)
                
                #Update Dictionary
                commands_dict[key] = command_list
        
                
        #Remove Empty Entries from Command List            
        elif step == "Remove Empty Entries":
            for key, values in commands_dict.items():
                command_list = []
                for command in values:
                    if command != "":
                        command_list.append(command)
                
                #Update Dictionary
                commands_dict[key] = command_list
                
        
        
            #Return Final Dictionary
            print("Commands Database Complete")
            return commands_dict
                
        



#Save Commands Dictionary to CSV File
def save_commands_dict(dictionary):
    "Takes the built command dictionary and saves it to a pickle file for later use"
    
    key_list = []
    values_list = []

    for key,values in dictionary.items():
        if key not in key_list:
            key_list.append(key)
        if values not in values_list:
            values_list.append(values)
     
    #Create Empty Dataframe       
    dict_pd = pd.DataFrame(columns = ['Dataset', "Commands"])
                
    #Save Data to Dataframe
    dict_pd["Dataset"] = key_list
    dict_pd["Commands"] = values_list
    
    #Save to Pickle File
    dict_pd.to_pickle("raw_elevation_dataset_commands.pkl")
    
    print("File Saved")
    
  
            
            
#Load the Commands Dictionary from the Pickle File
def load_commands_df():
    "Loads the Commands Dataframe from Pickle File to Pandas Dataframe"
    
    commands_df = pd.read_pickle('validated_elevation_dataset_commands.pkl')
    
    return commands_df







  
