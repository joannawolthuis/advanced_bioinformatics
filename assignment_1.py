import math
import csv
import pandas as pd
from ggplot import *

'''create list for x and y value'''
x_values = []
y_values = []

'''per row calculate y value and add to list for x and y values respectively.'''
for x in range(-10, 11):
    y_value = 2 * math.cos(x)
    x_values.append(x)
    y_values.append(y_value)

'''combine the x and y values into a dictionary'''
data = {'x':x_values, 'y':y_values}

'''make a DataFrame for the data - ggplot needs this as input and
it can also be used to make a nice .csv table.'''
data_frame = pd.DataFrame(data)

'''write our data to csv file. Use comma as seperator and
don't add indices in the first column'''
data_frame.to_csv('data_table.csv', sep=',', index=False)

'''tell user where the data table is'''
print('Data table with x and respective y values can be found in the folder with the .py file!')

'''plot data in line graph with ggplot. overlay with a more smoothed version of 2*cos function'''
graph = ggplot(aes(x='x', y='y'), data=data_frame) + \
	geom_line() + \
	stat_function(fun=lambda x:2*math.cos(x), color="red", size=1)
print graph
