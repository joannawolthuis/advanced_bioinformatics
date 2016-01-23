import urllib2
import csv
import StringIO
import numpy as np
import pandas as pd
from ggplot import *

'''customize query to send to CBIOportal'''

preconfig = raw_input("Use pre-configured parameters for assignment? y/n\n")

if preconfig == "y":
	case_set_id = "thca_tcga_pub_sequenced"
	genetic_profile_id = "thca_tcga_pub_mutations"
	gene_list = "BRAF"
elif preconfig == "n":
	case_set_id = raw_input("Please enter case set ID.\n")
	genetic_profile_id = raw_input("Please enter genetic profile ID.\n")
	gene_list = raw_input("Please enter gene list.\n")

'''build query from above parameters'''
url = 'http://www.cbioportal.org/webservice.do?cmd=getProfileData&case_set_id=' + case_set_id + '&genetic_profile_id=' + genetic_profile_id + '&gene_list=' + gene_list

'''request information from website and save as .txt'''
url_contents = urllib2.urlopen(url) 
with open( gene_list + '_data.txt', 'w') as f:
    f.write(url_contents.read())

'''save query page to txt and read into csv reader
The formatting is with tabs between rows so I use that as delimiter'''
in_txt = csv.reader(open('raw_data.txt', "rb"), delimiter = '\t')

'''we only need the 4th row as it has the mutation data per case
Call that row my_row for later usage'''
counter = 0 
my_row = []
for row in in_txt:
    counter+=1
    if counter == 4:
        my_row = row

'''delete first and second column as they have data we don't want to process. 
Delete the same row twice as the first index changes when we delete a row'''
del my_row[0]
del my_row[0]

'''load the mutation data into a big dictionary'''
wordcount = {}
for word in my_row:
    if word not in wordcount:
        wordcount[word] = 1
    else: 
        wordcount[word] += 1

'''set variable for calculating total cases'''
total = 0

'''set up a dictionary for loading the mutations and #s of cases'''
data = {'Mutation':[], 'Occurrence':[]}

'''count total cases - but only add the non-NaN keywords to the
list that will be processed next. NaN *is* included in total cases!'''
for key, value in wordcount.items():
    if 'NaN' not in key:
    	print key, value
    	data['Mutation'].append(key)
    	data['Occurrence'].append(value)
    total += value

'''load data into DataFrame for converting to csv
and loading into bar graph (necessary for ggplot and pandas'''
data_frame = pd.DataFrame(data)

'''plot data in bar graph with ggplot'''
graph = ggplot(aes(x='Mutation', y='Occurrence'), data=data_frame) + \
    geom_bar(position='dodge', stat='identity')

'''tell user where the data table is'''
print('Data tables for ' + gene_list + ' and mutation occurrence can be found in the folder with the .py file!')

print graph

'''append total to the table, we don't want it in the graph'''
data['Mutation'].append('Total:')
data['Occurrence'].append(total)

'''refresh dataframe'''
data_frame = pd.DataFrame(data)

'''save as csv'''
data_frame.to_csv( gene_list + '_results.csv', sep=',', index=False)


