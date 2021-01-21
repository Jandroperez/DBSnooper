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
from src.ShodanModules import Shodan_Search, ShodanParser
import src.Constants as CS

# *=============================
# * Argument Parser
# *=============================

# Builds the Argument Parser
parser = argparse.ArgumentParser(description=CS.description)

parser.add_argument('-q', '--query', help='The Shodan Search Term')

# Instantiates the Arguments
args = parser.parse_args()

# *=================================
# * Handling the User Interactions
# *=================================

if args.query:
    QueryRequest = Shodan_Search(searchTerm=args.query)
    Data = ShodanParser(QueryRequest)
    print(Data)
    print("")
    print()
    
    