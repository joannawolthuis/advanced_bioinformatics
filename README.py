# advanced_bioinformatics
Entry tests for advanced bioinformatics course

import math
import csv
import matplotlib.pyplot as plt

'''create data table'''

data_table = {}
x_values = []
y_values = []

'''per row calculate y value and add to list for x and y values respectively'''

for x in range(-10, 10):
    y_value = 2 * math.cos(x)
    x_values.append(x)
    y_values.append(y_value)

data = [x_values, y_values]
'''print x and y values'''
print x_values
print y_values

'''write x to first row in csv, y to second'''
file = open('data_table.csv', 'wb')
csv = csv.writer(file, delimiter=',',quoting=csv.QUOTE_ALL)
csv.writerow('x,y')
csv.writerows(zip(*data))
file.close

'''make plot'''
plt.plot(x_values, y_values)
plt.ylabel('y')
plt.xlabel('x')
plt.show()
