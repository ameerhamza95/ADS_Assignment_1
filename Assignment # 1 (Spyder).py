# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 09:46:04 2023

@author: HAMZA
"""

# importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import ticker

""" Defining the functions to be used in a program """

def read_csv_file():
    """ This function ask the user for the csv file to be read and set the 
        index column to date and return it.
    """
    
    # Ask for user input of file name and path
    file_path = input("Enter file path and name: ")
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path, index_col=0)
    
    # convert the 'date' column to a datetime object
    df.index = pd.to_datetime(df.index)
    
    return df

def filter_countries(df):
    """ This function asks the user for the country names and makes a new subset
        dataframe with them.
    """
    
    # Ask for user input of countries to filter
    countries = input("Enter country names separated by commas: ")  \
        .strip().title().split(",")
    
    # Clean up country names by removing leading/trailing whitespace
    countries = ['US' if country.strip() == 'Us' else country.strip() \
                 for country in countries]
    
    # Filter DataFrame by countries
    filtered_df = df[df['Country/Region'].isin(countries)]
    
    return filtered_df

def plot_cases_by_country(df):
    """ This function create a lineplot of confirmed covid cases by date
        of different countries.
    """
        
    # Get unique country names
    countries = df['Country/Region'].unique()
    
    # Create a figure and axis object with desired figure size
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Loop through each country and plot their confirmed cases over time
    for country in countries:
        # Subset data for current country
        country_data = df[df['Country/Region'] == country]
        
        # Plot confirmed cases over time for current country
        ax.plot(country_data.index, country_data['Confirmed'], \
                label=country)
    
    # Add labels, legend, and title to plot
    ax.set_xlabel('Dates', fontsize=14)
    ax.set_ylabel('Confirmed Cases', fontsize=14)
    ax.set_title('Confirmed Cases by 10 most populated Countries \n', \
                 fontsize = 16, color = 'green')
    ax.legend()
    
    # save the figure
    plt.savefig("Lineplot.png")
    
    # Show the plot
    plt.show()
    
    return

def sum_by_country(df):
    """ Takes a DataFrame with a date index and a 'Country/Region' column, as 
        well as columns for 'Confirmed', 'Deaths','Recovered', and 'Active' cases,
        and returns a new DataFrame where each country appears only once and the
        row values are summed for that country for the whole period of time.
    """
    
    # Group by country and sum the other columns
    grouped_df = df.drop(columns = ['Confirmed', 'Deaths', 'Recovered', \
                                    'Active'])
    grouped_df = grouped_df.groupby('Country/Region').sum()
    grouped_df = grouped_df.rename(columns = {'New cases': 'Confirmed', \
                                              'New deaths': 'Deaths', \
                                              'New recovered': 'Recovered'})
    
    # Reset the index to include the country column
    grouped_df = grouped_df.reset_index()
    
    return grouped_df

def add_percentages(df):
    """ Takes the return of the function sum_by_country and adds two new 
        columns of recovery% and death%.
    """
    
    # Add recovery% column
    df['recovery%'] = round(df['Recovered'] / df['Confirmed'] * 100, 2)

    # Add deaths% column
    df['deaths%'] = round(df['Deaths'] / df['Confirmed'] * 100, 2)

    return df

def plot_top10_stacked(df):
    """ This function makes a stacked bar plot of top 10 countries in terms 
        of recovery and deaths in percentages. 
    """
    
    # Sort the DataFrame by confirmed cases and select the top 10 countries
    top10 = df.sort_values('Confirmed', ascending = False).head(10)

    # Select only the columns we want to plot
    plot_data = top10[['Country/Region', 'deaths%', 'recovery%']]

    # Set the country names as the index for plotting
    plot_data = plot_data.set_index('Country/Region')

    # Plot the stacked bar chart
    ax = plot_data.plot(kind = 'bar', stacked=True, figsize=(10, 6), \
                        color = ['red', 'green'])

    # Set the x and y axis labels
    ax.set_xlabel('Country', fontsize=14)
    ax.set_ylabel('Percentage(%)', fontsize=14)

    # Set the title
    ax.set_title('Top 10 most affected countries ordered using recovery% \
& death%\n', fontdict={'fontsize': 16, \
                     'fontweight': 5,  "color": "green"})

    # Show the legend
    ax.legend(loc = 'upper left')
    
    # save the figure
    plt.savefig("Stackedbarplot.png", bbox_inches='tight')
     
    # Show the plot
    plt.show()
    
    return

def clean_data(df):
    """ Takes the dataframe and sum the covid cases by country and months, 
        then pivot the new dataframe by making country names as row index, month 
        names as column index and cases as values of the columns in the 
        dataframe. 
    """
    
    # Group the data by country and sum the cases for each month
    df = df.groupby(['Country/Region', pd.Grouper(freq='M')])['New cases'] \
        .sum().reset_index()
    
    # Format the date column to display month name
    df['Date'] = pd.Categorical(df['Date'].dt.strftime('%B'), \
                                categories=['January', 'February','March',\
                                            'April', 'May', 'June', 'July',\
                                            'August'], ordered=True)

    # Pivot the data to create a matrix where rows are countries and columns 
    # are months
    df = df.pivot(index='Country/Region', columns='Date', \
                  values='New cases')
    
    # Sort the countries by total confirmed cases and select top 20 countries
    df = df.loc[df.sum(axis=1).sort_values(ascending=False).\
                head(20).index]
    
    return df
    
def millions_formatter(val, pos):
    """ Takes value and position and return the value to display in 
        millions. 
    """
    
    return f'{val/1000000:.1f}M'

def plot_heatmap(df):
    """ Plots a heatmap of the input DataFrame using the matplotlib library to 
        display the top 20 highest cases countries.
    """
    plt.figure(figsize=(10, 8))
    
    # Define a custom colormap
    colors = [(1, 1, 0), (1, 0.6, 0), (1, 0, 0)]  # yellow, orange, red
    cmap = LinearSegmentedColormap.from_list('my_colormap', colors, N=256)

    # Plot the heatmap
    im = plt.imshow(df, cmap=cmap, aspect="auto")
    
    # Set the colorbar with millions formatter
    cbar = plt.colorbar(im, label='Confirmed Cases', \
                        format=ticker.FuncFormatter(millions_formatter))
    cbar.ax.yaxis.set_ticks_position('right')
    cbar.ax.yaxis.set_label_position('right')
    
    plt.title('Top 20 countries with highest confirmed cases\n', \
              fontsize=16, color='green')
    plt.xlabel('Month', fontsize=14)
    plt.ylabel('Country', fontsize=14)

    # Set the x-axis ticks and labels
    plt.xticks(range(len(df.columns)), df.columns, rotation=45,\
               ha='right',fontsize=10)

    # Set the y-axis ticks and labels
    plt.yticks(range(len(df.index)), df.index, fontsize=10)

    # Loop over data dimensions and create text annotations for each cell
    for i in range(len(df.index)):
        for j in range(len(df.columns)):
            text = plt.text(j, i, df.iloc[i, j], ha='center', \
                            va='center', color='grey')
   
    # Adjust the plot
    plt.tight_layout()
    # save the figure
    plt.savefig("Heatmap.png")
    # Show the plot
    plt.show()
    
    return

def plot_top_20(df):
    """ Takes the dataframe and calls the functions to plot the heat map """
    
    # Clean the data to be used by heatmap plot
    df_clean = clean_data(df)
    
    # Plot the heatmap
    return plot_heatmap(df_clean)

""" Main Program. """

# Giving the name and path of the csv file to store as dataframe
# file name and path used: 'Data/full_grouped.csv'
df_cases = read_csv_file()

# print the first 5 rows of the dataframe
print(df_cases.head())

# Giving the names of the 10 most populated countries by calling the function
# country names entered: china, india, us, indonesia, pakistan, brazil, 
# nigeria, bangladesh, russia, mexico
df_countries = filter_countries(df_cases)

# Calling lineplot to plot the list of 10 most populated countries
plot_cases_by_country(df_countries)

# Calling function to display the sum of the cases by country
summed_df = sum_by_country(df_cases)

# Calling function to make new columns of recovery% and death% in dataframe
summed_df = add_percentages(summed_df)

# print the first 10 rows
print("\n", summed_df.head(10))

# Calling stacked bar plot to plot the data
plot_top10_stacked(summed_df)

# Calling the heatmap function to plot the monthly cases of countries
plot_top_20(df_cases)


    
    
    





    
    
    
    
    
    
    
    