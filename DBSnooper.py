"""
Description:
-----------------------
This is the main script for the DBSnooper

Author:
-----------------------
Alex Perez
"""

# *============================
# * Import Section
# *============================

from src.ShodanUtils import Shodan

# *=================================
# * Handling the User Interactions
# *=================================

if __name__ == '__main__':
    QueryRequest = Shodan.Shodan_Search(searchTerm="Elastic")
    print(QueryRequest)
