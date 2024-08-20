import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import re  
import seaborn as sns
import matplotlib.pyplot as plt 
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import json
from urllib.request import urlopen

class Crime: 

    #----------------- Initialize -------------------------
    def __init__(self):
        try:
            # Read the file with pandas
            self.df = pd.read_excel("Bab 1 - Jenayah indeks 2020 v1.xlsx")
            self.df_crime = pd.DataFrame(pd.read_excel("Bab 1 - Jenayah indeks 2020 v1.xlsx", sheet_name="1.2 Crime Index Ratio"))
            self.df_violentCrimes = pd.DataFrame(pd.read_excel("Bab 1 - Jenayah indeks 2020 v1.xlsx", sheet_name="1.4")) 
        except FileNotFoundError as e:
            print(f"Error: {e}")
            self.df = pd.DataFrame()
            self.df_crime = pd.DataFrame()
            self.df_violentCrimes = pd.DataFrame()  
        except Exception as e:
            print(f"An error occurred: {e}")
            self.df = pd.DataFrame()
            self.df_crime = pd.DataFrame()
            self.df_violentCrimes = pd.DataFrame() 
    
    #------------------ Sheet 1.1 -------------------------
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

    def compareCrimeAcrossStates(self, year1, year2):  
        # List of valid years for comparison  
        valid_years = [2017, 2018, 2019]  
        
        # Check if the provided years are within the valid range  
        if year1 not in valid_years or year2 not in valid_years:  
            return "Error: Please select years from 2017, 2018, or 2019."  
        
        # Check if the DataFrame is empty and cannot perform the comparison  
        if self.df.empty:  
            return "DataFrame is empty. Cannot perform the comparison."  
        
        try:  
            # Select data corresponding to the specified years  
            df_year1 = self.df[self.df.Year == year1].reset_index(drop=True)  
            df_year2 = self.df[self.df.Year == year2].reset_index(drop=True)  
    
            # Merge the data for both years into a single DataFrame  
            df_comparison = pd.merge(  
                df_year1[['State', 'Total']],   
                df_year2[['State', 'Total']],   
                on='State',   
                suffixes=(f'_{year1}', f'_{year2}')  
            )  
            
            # Calculate the percentage change in total crimes between the two years  
            df_comparison['Change (%)'] = (  
                (df_comparison[f'Total_{year2}'] - df_comparison[f'Total_{year1}']) / df_comparison[f'Total_{year1}']  
            ) * 100  
            
            # Display the comparison DataFrame in JupyterLab  
            from IPython.display import display  
            display(df_comparison)  # This will display the DataFrame in JupyterLab  
            
            # Visualize the comparison results using a line chart  
            fig = px.line(  
                df_comparison,  
                x='State',  
                y=[f'Total_{year1}', f'Total_{year2}'],  
                title=f"Comparison of Total Crimes between {year1} and {year2}",  
                labels={f'Total_{year1}': f'Total Crimes {year1}', f'Total_{year2}': f'Total Crimes {year2}'},  
                markers=True  
            )  
            fig.update_layout(  
                xaxis_title='State',  
                yaxis_title='Total Crimes',  
                legend_title='Year',  
                title=f'Comparison of Total Crimes and Percentage Change ({year1} vs {year2})'  
            )  
            
            # Visualize the percentage change using a bar chart  
            fig2 = px.bar(  
                df_comparison,  
                x='Change (%)',  
                y='State',  
                title=f'Percentage Change in Total Crimes from {year1} to {year2}',  
                labels={'Change (%)': 'Percentage Change', 'State': 'State'}  
            )  
            fig2.update_layout(  
                xaxis_title='Percentage Change',  
                yaxis_title='State',  
                title=f'Percentage Change in Total Crimes ({year1} vs {year2})'  
            )  
    
            # Display the charts  
            fig.show()  
            fig2.show()  
            
        except Exception as e:  
            return f"An error occurred while comparing crime data: {e}"
                

    def compareCrimeTypes(self, year1, year2=None, year3=None):  
        valid_years = [2017, 2018, 2019]  
    
        # If only one year is provided, default to using 2018 as the other year  
        if year2 is None:  
            year2 = 2018  
    
        if year3 is not None and year3 not in valid_years:  
            print(f"Error: Invalid year {year3} selected. Please choose from {valid_years}.")  
            return  
    
        # Check if the provided years are valid  
        if year1 not in valid_years or year2 not in valid_years:  
            print(f"Error: Invalid years selected. Please choose from {valid_years}.")  
            return  
    
        if self.df.empty:  
            print("DataFrame is empty. Cannot perform the comparison.")  
            return  
    
        try:  
            # Select data for the specified years  
            df_year1 = self.df[(self.df.Year == year1) & (self.df.State == 'Malaysia')].reset_index(drop=True)  
            df_year2 = self.df[(self.df.Year == year2) & (self.df.State == 'Malaysia')].reset_index(drop=True)  
    
            # Extract the total cases for each crime type  
            df_year1_totals = df_year1[['Violent crime', 'Property crime']].iloc[0]  
            df_year2_totals = df_year2[['Violent crime', 'Property crime']].iloc[0]  
    
            df_comparison = pd.DataFrame({  
                'Crime Type': ['Violent crime', 'Property crime'],  
                f'Total Cases {year1}': [df_year1_totals['Violent crime'], df_year1_totals['Property crime']],  
                f'Total Cases {year2}': [df_year2_totals['Violent crime'], df_year2_totals['Property crime']]  
            })  
    
            if year3:  
                df_year3 = self.df[(self.df.Year == year3) & (self.df.State == 'Malaysia')].reset_index(drop=True)  
                df_year3_totals = df_year3[['Violent crime', 'Property crime']].iloc[0]  
                df_comparison[f'Total Cases {year3}'] = [df_year3_totals['Violent crime'], df_year3_totals['Property crime']]  
    
            # Calculate the percentage change in crime types  
            df_comparison['Change (%)'] = ((df_comparison[f'Total Cases {year2}'] - df_comparison[f'Total Cases {year1}']) / df_comparison[f'Total Cases {year1}']) * 100  
    
            # Visualize the total cases of different crime types for the specified years  
            y_columns = [f'Total Cases {year1}', f'Total Cases {year2}']  
            if year3:  
                y_columns.append(f'Total Cases {year3}')  
    
            fig = px.bar(df_comparison, x='Crime Type', y=y_columns,  
                         title=f"Total Cases of Different Crime Types in {year1}, {year2}" + (f", and {year3}" if year3 else ""),  
                         labels={'value': 'Number of Cases'})  
            fig.update_layout(  
                xaxis_title='Crime Type',  
                yaxis_title='Number of Cases',  
                title=f'Total Cases of Different Crime Types ({year1}, {year2}' + (f', {year3}' if year3 else '') + ')'  
            )  
            fig.show()  
    
            print(f"Summary of crime types in {year1}, {year2}" + (f", and {year3}" if year3 else "") + ":")  
            print(df_comparison)  
    
        except Exception as e:  
            print(f"An error occurred while comparing crime types in {year1}, {year2}" + (f", and {year3}" if year3 else "") + f": {e}")   

    
    #------------------ Sheet 1.2 -------------------------
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

    def showCrimePopulationCorrelation(self, year):  
        try:  
            # Check if the crime DataFrame is empty  
            if self.df_crime.empty:  
                print("Crime index DataFrame is empty. Cannot perform correlation analysis.")  
                return  
            
            # Filter out the row for "Malaysia" and select the specified year  
            df_filtered = self.df_crime[(self.df_crime['State'] != 'Malaysia') & (self.df_crime['Year'] == year)]  
            
            # Print DataFrame columns for debugging  
            print("Filtered DataFrame columns:")  
            print(df_filtered.columns)  
            
            # Define the correlation columns  
            correlation_columns = ['Crime index ratio', 'Population']  

            # Verify these columns are in the DataFrame  
            for col in correlation_columns:  
                if col not in df_filtered.columns:  
                    print(f"Column '{col}' is not in the DataFrame. Available columns are: {df_filtered.columns}")  
                    return  
            
            # Calculate the correlation matrix  
            correlation_matrix = df_filtered[correlation_columns].corr()  
            print("Correlation Matrix:")  
            print(correlation_matrix)  
            
            # Plotting the correlation  
            plt.figure(figsize=(10, 6))  
            sns.scatterplot(data=df_filtered, x='Population', y='Crime index ratio', hue='State', palette='viridis')  
            plt.title(f'Correlation between Population and Crime Index Ratio in {year}')  
            plt.xlabel('Population')  
            plt.ylabel('Crime Index Ratio')  
            plt.legend(title='State')  
            plt.show()  
            
        except Exception as e:  
            print(f"An error occurred while performing correlation analysis: {e}") 


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


    #------------------- Sheet 1.4 -------------------------
    def analyzeViolentCrimes(self):  
        if self.df_violentCrimes.empty:  
            print("The violent crimes DataFrame is empty. Cannot perform analysis.")  
            return  
    
        try:  
            # Display the data types for clarity on the DataFrame  
            print(self.df_violentCrimes.dtypes)  
    
            # Convert relevant columns to numeric (if they are not already)  
            crime_types = ['Murder', 'Rape', 'Gang robbery with Firearms',  
                           'Gang robbery without Firearms', 'Robbery with Firearms',  
                           'Robbery without Firearms', 'Causing injury']  
    
            # Convert columns to numeric, forcing errors to NaN  
            self.df_violentCrimes[crime_types] = self.df_violentCrimes[crime_types].apply(pd.to_numeric, errors='coerce')  
    
            # 1. Visualize total violent crimes per year for Malaysia using a line chart  
            total_violence = self.df_violentCrimes[self.df_violentCrimes['Contingent/ PDRM District'] == 'Malaysia'][['Year'] + crime_types]  
            total_violence = total_violence.set_index('Year').sum(axis=1).reset_index(name='TotalViolence')  
    
            # Create a line chart for total violent crimes  
            fig1 = px.line(total_violence, x='Year', y='TotalViolence',  
                           title='Total Violent Crimes in Malaysia (2017-2019)',  
                           labels={'TotalViolence': 'Total Violent Crimes'})  
            
            # Set x-axis to show only integer years  
            fig1.update_xaxes(tickmode='linear', tickvals=[2017, 2018, 2019])  
            fig1.show()    
        
            # 2. Track changes in specific types of violent crimes over time, excluding Malaysia  
            types_over_time = self.df_violentCrimes[self.df_violentCrimes['Contingent/ PDRM District'] != 'Malaysia'].melt(  
                id_vars=['Year', 'Contingent/ PDRM District'],  
                value_vars=crime_types,  
                var_name='Type', value_name='CrimeTotal'  
            )  
    
            types_over_time = types_over_time[types_over_time['CrimeTotal'] > 0]  # Filter out zero counts  
    
            # Create line plot  
            fig2 = px.line(types_over_time, x='Year', y='CrimeTotal', color='Type',  
                           title='Changes in Violent Crime Types Over Time by State (2017-2019)',  
                           labels={'CrimeTotal': 'Total Violent Crimes'},  
                           facet_col='Contingent/ PDRM District', facet_col_wrap=4)  
    
            # Adjust layout to increase height and width   
            fig2.update_layout(height=800, width=1300)  # Increase height and width  
            fig2.update_xaxes(tickvals=[2017, 2018, 2019])  # Set x-axis ticks to whole years only  
            fig2.update_yaxes(title_text='Violent Crimes', title_font=dict(size=10), tickmode='linear', tick0=0, dtick=500)  # Adjust y-axis label and ticks  
    
            fig2.show()  
    
            # 3. Contribution of states to total violent crimes in a horizontal bar chart  
            state_contribution = self.df_violentCrimes[self.df_violentCrimes['Contingent/ PDRM District'] != 'Malaysia']  
            fig3 = px.bar(state_contribution, x='Total', y='Contingent/ PDRM District', color='Year',  
                          title='Contribution of States to Total Violent Crimes (2017-2019)',  
                          orientation='h',  # Horizontal bar chart  
                          labels={'Total': 'Total Violent Crimes'})  
    
            # Increase margin to add more space between bars  
            fig3.update_layout(yaxis=dict(tickmode='linear', dtick=1),  # Increase gaps between states  
                               yaxis_title=None,  # Remove y-axis title for a cleaner look  
                               margin=dict(l=50, r=30, t=50, b=50))  # Adjust margins as needed  
            fig3.show()  
    
        except Exception as e:  
            print(f"An error occurred while analyzing violent crimes: {e}")   
    

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
        
            
    def analyzeViolentCrimeByArea(self, state, year):  
        """  
        Analyze crime types for the given state and year,  
        visualizing the crime distribution by area, excluding the state total.  
        """  
        df_state_year = self.showCrimeActivity(state, year)  
    
        if df_state_year.empty:  
            return  # No data available for the specified state and year  
    
        # Extract the state name dynamically from the sheet name  
        state_name = re.sub(r'1\.5', '', state)  
    
        # Prepare results for display while excluding the total for the state  
        results_df = pd.DataFrame({  
            'Area': df_state_year['Contingent/ PDRM District'],  
            'Total Cases': df_state_year['Total']  
        })  
    
        # Get the total cases for the state  
        state_total_cases = results_df[results_df['Area'] == state_name]['Total Cases'].values[0]  
    
        # Filter out the total for the specific state  
        results_df = results_df[results_df['Area'] != state_name]  
        results_df.reset_index(drop=True, inplace=True)  
    
        # Create a heatmap to show the distribution of crimes by area  
        fig = px.density_heatmap(results_df, x='Area', y='Total Cases', z='Total Cases',  
                                  title=f"Violent Crime Distribution in {state_name} for {year} (Total Cases in {state_name} = {state_total_cases})",  
                                  labels={'Total Cases': 'Total Cases'},  
                                  color_continuous_scale='YlOrRd')  
    
        # Show the chart  
        fig.show()  

    def analyzeViolentCrimeByType(self, state, year):  
        """  
        Analyze total cases for each type of violent crime in the given state and year,  
        visualizing the distribution in a pie chart.  
        """  
        # Extract the relevant data for the specified state and year  
        df_state_year = self.showCrimeActivity(state, year)  
        
        if df_state_year.empty:  
            print("No data available for the specified state and year.")  
            return  
        
        # Extract the state name dynamically from the sheet name  
        state_name = re.sub(r'1\.5', '', state)  
        
        # Filter the data to get the row corresponding to the state total  
        state_total_row = df_state_year[df_state_year['Contingent/ PDRM District'] == state_name]  
        
        if state_total_row.empty:  
            print(f"No total data available for {state_name} in {year}.")  
            return  
        
        # Define the violent crime types  
        violent_crime_types = ['Murder', 'Rape', 'Gang robbery with Firearms',  
                               'Gang robbery without Firearms', 'Robbery with Firearms',  
                               'Robbery without Firearms', 'Causing injury']  
        
        # Extract the total cases for each type of violent crime from the specific row  
        total_cases = [state_total_row[crime_type].values[0] for crime_type in violent_crime_types]  
        
        # Create a DataFrame to capture total cases for each type of violent crime  
        results_df = pd.DataFrame({  
            'Crime Type': violent_crime_types,  
            'Total Cases': total_cases  
        })  
        
        # Filter out cases where total cases are zero  
        results_df = results_df[results_df['Total Cases'] > 0]  
        
        # Create a pie chart to show distribution of violent crime types  
        fig = px.pie(results_df, names='Crime Type', values='Total Cases',  
                     title=f"Distribution of Violent Crime Types in {state_name} for {year}",  
                     labels={'Total Cases': 'Total Cases'})  
        
        # Show the pie chart  
        fig.show()   

    def analyzeViolentCrimeStatistics(self, state, year):  
            """  
            Analyze crime statistics for the given state and year,  
            calculating the min, max, and mean total cases, excluding the state total.  
            """  
            df_state_year = self.showCrimeActivity(state, year)  
            
            if df_state_year.empty:  
                return None  # No data available for the specified state and year  
            
            # Extract the state name dynamically from the sheet name  
            state_name = re.sub(r'1\.5', '', state)  
            
            # Prepare results for statistical analysis while excluding the total for the state  
            results_df = pd.DataFrame({  
                'Area': df_state_year['Contingent/ PDRM District'],  
                'Total Cases': df_state_year['Total']  
            })  
            
            # Filter out the total for the specific state  
            results_df = results_df[results_df['Area'] != state_name]  
            results_df.reset_index(drop=True, inplace=True)  
            
            # Calculate statistics  
            min_cases = int(results_df['Total Cases'].min())  # Convert to integer  
            max_cases = int(results_df['Total Cases'].max())  # Convert to integer  
            mean_cases = int(results_df['Total Cases'].mean())  # Convert mean to int  
        
            # Get the area with the most crime  
            area_max_crime = results_df.loc[results_df['Total Cases'].idxmax(), 'Area']  
        
            # Create a DataFrame for statistics, ensuring 'Value' is treated as integers  
            stats_df = pd.DataFrame({  
                'Statistic': ['Minimum Cases', 'Maximum Cases', 'Mean Cases'],  
                'Value': [min_cases, max_cases, mean_cases],  # Assign integer values directly  
                'Area': [None, area_max_crime, None]  
            })  
        
            # Convert the 'Value' column to integers explicitly  
            stats_df['Value'] = stats_df['Value'].astype(int)  
            
            # Display the statistics DataFrame in Jupyter Notebook  
            display(stats_df)  
        
            # Plotting the statistics  
            plt.figure(figsize=(10, 5))  
            bars = plt.bar(stats_df['Statistic'], stats_df['Value'], color=['skyblue', 'salmon', 'lightgreen'])  
            plt.title(f'Crime Statistics for {state_name} in {year}')  
            plt.ylabel('Number of Cases')  
            plt.xticks(rotation=45)  
            plt.grid(axis='y', linestyle='--', alpha=0.7)  
        
            # Adding exact values on top of the bars  
            for bar in bars:  
                yval = bar.get_height()  
                plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')  # va='bottom' ensures text is above the bar  
            
            plt.show()  
  #------------------ Sheet 1.7 -------------------------    
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



    
