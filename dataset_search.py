import geemap.foliumap as geemap
from geemap.datasets import DATA
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


def dataset_search(keyword):
    """
    Pull datasets from Google Earth Engine using a keyword search term.  The function will create a dictionary
    with the title as the keys and a list of dataset information as the values.
    """
    
    search = geemap.search_ee_data(keyword)
    
    datasets = {}
    
    for iter in range(0,len(search)):
        datasets[search[iter]['title']] = search[iter]
        
    return datasets



def display_thumbnail(image_url):
    """
    Takes a thumbnail image url for a GEE dataset and displays it in a cell
    """
    
    #Initiate Request for Image URL
    response = requests.get(image_url)
    
    #Open Content with Image
    img = Image.open(BytesIO(response.content))
    
    return img


def display_description(asset_url):
    """
    Takes the GEE asset url and displays the description of the GEE dataset, 
    place in a markdown cell for final output
    
    """
    
    #Initiate Request to GEE Asset Page and grab content
    response = requests.get(asset_url)
    content = response.content
    
    #Convert Item to BS Item
    asset_soup = BeautifulSoup(content, 'html.parser')
    
    #Grab the Description from the Soup
    description = asset_soup.find(itemprop="description")
    
    return description





