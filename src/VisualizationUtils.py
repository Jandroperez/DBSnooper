"""
Description:
-----------------------
This Module will be used to handle all Visualization Tasks

Author: Alex Perez
"""

# ================== IMPORT SECTION =======================
from re import A
import pandas as pd
import altair as alt
import folium

# *================= CLASSES SECTION ======================

class ShodanMap:
    """
    Wrapper built around the Folium Library
    """

    @classmethod
    def BuildMap(cls, Dataframe, latitude_column, longitude_column):
        """
        Description:
        ----------------
            This Function will create the map and handle the Dataframe that is
            provided via the dataframe

        Parameters:
        -----------------
        Dataframe:
            The Target Dataframe that will be used as the backbone of the Data
        latitude_column:
            The Latitude Column
        longitude_column:
            The longitude column of the dataframe

        Returns:
        -------------------
        Will return an interactive map with tooltip information
        """

        try:
            Dataframe = Dataframe[Dataframe[latitude_column].notnull()]
            Dataframe = Dataframe[Dataframe[longitude_column].notnull()]

            # Instantiating the map from Folium
            Geo_Map = folium.Map(
                location=[Dataframe[latitude_column].mean(), Dataframe[longitude_column].mean()],
                zoom_start=2
            )

            # Begins iterating through the Dataframe
            for index, row in Dataframe.iterrows():
                Pop_up_HTML = f"""
                <b> Ip Address: </b> {row['ip_str']} <br>
                <b> Port: </b> {row['port']} <br>
                <b> ISP: </b> {row['isp']} <br>
                <b> Organization: </b> {row['org']} <br>
                """

                # Instantiating the Marker for the Map
                folium.Marker(
                    [row[latitude_column], row[longitude_column]],
                    popup=Pop_up_HTML,
                    tooltip=f"click for {row['ip_str']}"
                ).add_to(Geo_Map)

            #returns the Map
            return Geo_Map
        except:
            return "Error: Attempt to build map failed..."


class Graph:
    """
    This Class will handle all the metric visualizations and build Interactive Graphs
    """

    @classmethod
    def Bar_Graph(cls, Dataframe='', y_axis=''):
        """
        Description:
        ------------------
            This Module will create a Bar Graph with a tool tip

        Parameters:
        -------------------
            Dataframe:
                This will use a Dataframe to build out the Bar graph

            x_axis:
                Will gather the Target column to create a count of the wanted value
        
        Returns:
        ---------------------
        Will return a Bar Graph
        """
        try:
            Data = Dataframe[y_axis].value_counts()[:10].reset_index()
            Data.rename(columns={
                'index': y_axis,
                f'{y_axis}': 'Count'
            }, inplace=True)

            Data = Data.sort_values(by='Count', ascending=False)
            
            Altair_BarGraph = alt.Chart(Data).mark_bar().encode(
                alt.X('Count'),
                alt.Y(y_axis)
            )

            return Altair_BarGraph
        except:
            return "Error: Something Broke"