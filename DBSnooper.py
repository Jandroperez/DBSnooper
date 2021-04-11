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

import argparse
from src.ShodanUtils import Shodan
import src.Constants as CS

# *=============================
# * Argument Parser
# *=============================


# *=================================
# * Handling the User Interactions
# *=================================


QueryRequest = Shodan.Shodan_Search(searchTerm="Elastic")
print(QueryRequest)


    