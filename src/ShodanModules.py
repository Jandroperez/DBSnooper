"""
Description:
--------------------------
This Script will handle all the modules that will be used to interact Shodan

Author:
--------------------------
Alex Perez
"""

# *=======================
# Import Section
# *=======================

import requests
import yaml
import os
from colorama import Fore
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize


#*=======================
# Global Variables
# *=======================
# Setting up Base Path
currentPath = os.getcwd()

with open(currentPath + '/src/auth.yaml') as auth:
    authList = yaml.load(auth, Loader=yaml.FullLoader)
    shodanApiKey = authList['shodanApiKey']

# *=======================
# Functions Section
# *=======================

# The Shodan Search Function
def Shodan_Search(searchTerm, facets=''):
    """
    Description: 
    -----------------------
    The Function that to search Shodan for results. Results may vary depending
    on the User's Query

    Parameters:
    ------------------------
    @param searchTerm   : the search term that is provided by the User
    @param facets       : Any facets that are wanted by the User
    @return             : Will return a json of the Data
    """
    
    try:
        # The Shodan Search URL
        ShodanSearchURL = f'https://api.shodan.io/shodan/host/search?key={shodanApiKey}&query={searchTerm}&facets={facets}'
        # Sending out the Request
        ShodanRequest = requests.get(ShodanSearchURL)
        # Shodan Data Conversion into Json
        ShodanSearchJson = ShodanRequest.json()
        # Returns the Json of the response
        return ShodanSearchJson
        
    except requests.RequestException as error:
        print(error)

# This Function will parse out JSON of the query 
def ShodanParser(QueryData):
    """
    Description:
    -------------------
    This Function will parse the Data from the Json that is provided by Shodan and present in a neat format

    Parameters:
    --------------------
    @QueryData:
        The Json Data that is received from the query
    @Dataframe:
        Default Value is set to False. If True, then the data will be provided in a Dataframe

    Returns:
    --------------------
    Will return the Data in a readable format
    """
    # Will Convert the JSON into a Dataframe
    ShodanDataframe = json_normalize(QueryData['matches'])
    ShodanDataframe = ShodanDataframe[['ip_str', 'port', 'org', 'asn', 'product']]
    return ShodanDataframe
