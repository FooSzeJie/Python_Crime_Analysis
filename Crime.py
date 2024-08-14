import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt 
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import json
from urllib.request import urlopen

class Crime: 

    def __init__(self):
        try:
            # Read the file with pandas
            self.df = pd.read_excel("Bab 1 - Jenayah indeks 2020 v1.xlsx")
            self.df_crime = pd.DataFrame(pd.read_excel("Bab 1 - Jenayah indeks 2020 v1.xlsx", sheet_name="1.2 Crime Index Ratio"))
        except FileNotFoundError as e:
            print(f"Error: {e}")
            self.df = pd.DataFrame()
            self.df_crime = pd.DataFrame()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.df = pd.DataFrame()
            self.df_crime = pd.DataFrame()
        
    def showTotalCrimeTable(self):
        # Show the total crime data with Pandas table
        if self.df.empty:
            print("DataFrame is empty. Cannot display the table.")
            return
        return self.df

    def ShowCrimeBarInYear(self, year):
        if self.df.empty:
            print("DataFrame is empty. Cannot display the chart.")
            return
        
        try:
            # Define the df
            df = self.df.copy()
            df.columns = df.columns.str.strip() # Delete the head of the table
            df17 = df.loc[(df.Year == year)] # We only want 2017 
            df17 = df17.reset_index(drop=True) # Resetting the Index 

            fig = px.bar(df17.iloc[1:], x='State', y='Total', hover_data=['Violent crime', 'Property crime'], width = 1000, color='Total',title=f"Table 1: Total Cases throughout each state in Malaysia in {year}")

            # Show the Chart
            fig.show()
            
        except Exception as e:
            print(f"An error occurred while creating the bar chart: {e}")

    def showCrimeRadioIndexTable(self):
        if self.df_crime.empty:
            print("DataFrame is empty. Cannot display the table.")
            return
        
        try:
            # Define the df_crime
            df_crime = self.df_crime.copy()

            df_crime.columns = df_crime.columns.str.strip() # Delete the Head of the table
            df_crime["Crime index ratio"]= df_crime["Crime index ratio"].round(decimals=1)
            return self.df_crime
        except Exception as e:
            print(f"An error occurred while processing the crime radio index table: {e}")

    def showCrimeRadioIndexBar(self):
        if self.df_crime.empty:
            print("DataFrame is empty. Cannot display the chart.")
            return
        
        try:
            # Define the df_crime
            df_crime = self.df_crime.copy()

            fig2 = px.bar(df_crime.iloc[3:] , x='State', y='Crime index ratio', hover_data=['Crime Index', 'Population',"Year"],width= 900, 
                color='Crime Index',title="Table 2 : Crime Index Ratio throughout 2017-2019")

            # Show the Chart
            fig2.show()
        except Exception as e:
            print(f"An error occurred while creating the bar chart: {e}")

    def showCrimeActivity(self, state, year):
        try:
            # Read the dataset based on the sheet name
            df_state = pd.DataFrame(pd.read_excel("Bab 1 - Jenayah indeks 2020 v1.xlsx", sheet_name=state))

            df_state.columns = df_state.columns.str.strip()
            df_state= df_state.replace("-",0)
            df_state_year = df_state[(df_state['Year'] == year) ].reset_index(drop=True)
            df_state_year = df_state_year.drop("Year", axis=1)

            return df_state_year
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"An error occurred: {e}")
            return pd.DataFrame()

    def showCrimeActivityBar(self, state, year, area):
        try:
            # Read the dataset based on the sheet name
            df_state = pd.DataFrame(pd.read_excel("Bab 1 - Jenayah indeks 2020 v1.xlsx", sheet_name=state))

            df_state.columns = df_state.columns.str.strip()
            df_state = df_state.replace("-", 0)
            df_state_year = df_state[df_state['Year'] == year].reset_index(drop=True)
            df_state_year = df_state_year.drop("Year", axis=1)

            # Retrieve the area name using the provided index
            area_name = df_state_year.iloc[area, 0]  # Assuming the area name is in the first column

            df_state_year_wm = df_state_year.iloc[area]
            df_state_year_wm = pd.DataFrame(df_state_year_wm)
            df_state_year_wm2 = df_state_year_wm.iloc[2:].reset_index()

            df_state_year_wm2.rename(columns={5: "Total", "index": "Cases"}, inplace=True)
            fig = px.treemap(df_state_year_wm2, values=df_state_year_wm2.columns[1], path=["Cases"], width=600, height=700, title=f"Table 3 : The Amount of cases in {area_name}", color_discrete_sequence=px.colors.sequential.RdBu)

            # Show the Chart
            fig.show()
        except Exception as e:
            print(f"An error occurred while creating the treemap chart: {e}")

    def showCrimeRadioIndexYearTable(self, year):     
        try:
            with urlopen('https://raw.githubusercontent.com/nullifye/malaysia.geojson/master/malaysia.state.geojson') as response: 
                my_map = json.load(response)
                
            state_id_map={}

            for feature in my_map['features']:
                state_id_map[feature['properties']['state']] = feature['id']

            # Rename the all the names from the JSON file 
            rename =["Kedah","Kelantan","Perak","Pulau Pinang","Kuala Lumpur","Negeri Sembilan","Melaka",
                     "Perlis","Pahang","Terengganu","Putrajaya","Labuan","Selangor","Sabah","Johor","Sarawak"]

            state_id_map = dict(zip(rename , list(state_id_map.values())))  

            # Define the df_crime
            df_crime = self.df_crime.copy()

            # Taking the data based on the year 
            df_state_crime =df_crime.loc[(df_crime.Year == year)]  
            df_state_crime= df_state_crime.reset_index(drop=True) 
            df_state_crime= df_state_crime.loc[1:].reset_index(drop=True) 

            return df_state_crime  # Show the table
        except Exception as e:
            print(f"An error occurred while processing the crime radio index year table: {e}")
            return pd.DataFrame()

    def showCrimeRadioIndexYearMap(self, year):
        try:
            with urlopen('https://raw.githubusercontent.com/nullifye/malaysia.geojson/master/malaysia.state.geojson') as response: 
                my_map = json.load(response)
                
            state_id_map={}

            for feature in my_map['features']:
                state_id_map[feature['properties']['state']] = feature['id']

            # Rename the all the names from the JSON file 
            rename =["Kedah","Kelantan","Perak","Pulau Pinang","Kuala Lumpur","Negeri Sembilan","Melaka",
                     "Perlis","Pahang","Terengganu","Putrajaya","Labuan","Selangor","Sabah","Johor","Sarawak"]

            state_id_map = dict(zip(rename , list(state_id_map.values())))  

            # Define the df_crime
            df_crime = self.df_crime.copy()

            # Taking the data based on the year 
            df_state_crime =df_crime.loc[(df_crime.Year == year)]  
            df_state_crime= df_state_crime.reset_index(drop=True) 
            df_state_crime= df_state_crime.loc[1:].reset_index(drop=True) 

            df_state_crime["id"]=df_state_crime["State"].apply(lambda x : state_id_map.get(x, None))
            fig = px.choropleth(
                df_state_crime,
                locations="id",width=700,
                geojson=my_map,
                color="Crime index ratio",
                hover_name="State",
                hover_data=["Crime Index","Population"],
                title=f"Table 4 :Crime Index Ratio throughout Malaysia in {year}")
            fig.update_geos(fitbounds="locations", visible=False)
            fig.show()
        except Exception as e:
            print(f"An error occurred while creating the choropleth map: {e}")
