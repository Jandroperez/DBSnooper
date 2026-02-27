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
import pandas as pd
from pandas import json_normalize


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

# This class will handle the Shodan Modules
class Shodan:
    """
    Wrapper for Shodan API
    """

    @classmethod
    # The Shodan Search Function
    def Shodan_Search(cls, searchTerm, facets=''):
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
            ShodanRequest = requests.get(
                'https://api.shodan.io/shodan/host/search',
                params={'key': shodanApiKey, 'query': searchTerm, 'facets': facets}
            )
            return cls.ShodanParser(ShodanRequest.json())
            
        except requests.RequestException as error:
            print(error)

    @classmethod
    # This Function will parse out JSON of the query 
    def ShodanParser(cls, QueryData):
        """
        Description:
        -------------------
        This Function will parse the Data from the Json that is provided by Shodan and present in a neat format

        Parameters:
        --------------------
        @QueryData:
            The JSON data received from the Shodan API

        Returns:
        --------------------
        Will return the Data in a readable format
        """
        # Will Convert the JSON into a Dataframe
        ShodanDataframe = json_normalize(QueryData['matches'])
        ShodanDataframe = ShodanDataframe[['ip_str', 'port', 'org', 'asn', 'isp', 'product', 'location.country_name', 'location.latitude', 'location.longitude']]
        return ShodanDataframe
