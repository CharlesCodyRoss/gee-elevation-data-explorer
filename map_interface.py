import geocoder
from geopy.geocoders import Nominatim
import streamlit as st
geolocator = Nominatim(user_agent="geoapiExercises")


#Grab Lat and Long Based on Entry
def location_search(location):
    """
    Find the latitude and longitude of a city that is entered into the input prompt.
    """
    
    try:
        city, latlng = geolocator.geocode(location)
        
        lat = latlng[0]
        lng = latlng[1]
        
        return [lat, lng]
        
        
    except:
        
        """
        Location Not Found!
        
        Please Try Entering Your Location Information Again
        
        """
        
        
        
        
def my_location():
    """ 
    Find the latitude and longitude of the user's current device location
    """
    
    try:
        g = geocoder.ip('me')

        lat, lng = g.latlng

        return [lat, lng]
    
    except:
        """
        Location Not Found!
        
        Please Try Entering Your Location Information Again
        
        """