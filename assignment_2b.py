import json
import codecs
from pymongo import MongoClient

'''
This function can be used to convert the json output of bio-vcf to 
a format that Mongo will accept as imported file in Windows. 
In the template add a comma after the last bracket as this is necessary for forming array
'''
def make_compatible(filename):
	# open original file as utf16 / ucs2 (source encoding)
	file = codecs.open(filename+".json", encoding="utf16")
	# create list for temporary storage of json file
	temp = []
	# iterate through lines in json file
	for line in file:
		# change encoding of line to utf-8
		convert = line.decode('utf-8', 'ignore')
		# add converted line to the temporary list
		temp.append(convert.rstrip())
	# insert opening square bracket to indicate jsonArray
	temp.insert(0, "[")
	# remove last comma (comma not needed for the last item in array)
	if "," in temp[-1]:
		temp[-1] = "}"
	# close jsonArray with square bracket
	temp.insert(len(temp), "]")
	# create new file (utf-8 encoding) to store the converted json
	new_filename = filename + "_conv.json"
	new_file = codecs.open(new_filename, encoding="utf-8", mode="w+")
	# iterate through the temporary storage
	for line in temp:
		# write line to the file
		new_file.write(line + "\n")
	new_file.close()

###################################################

client = MongoClient()
# i hosted the collection in the test db
db = client.test
# this code will use the collection assignment_2 where the converted vcf was loaded

cursor = db.assignment_2.find()

# create counter for later usuage
counter = 0 

# iterate through database collection
for document in cursor:
	# specifically reading the samples array with the dp listed
	target = document["rec"]["samples"] 
	# search for sample 3 and 4 (python starts counting at 0) with both dps higher than 7
	if target[2] > 7 and target[3] > 7:
		# optional print statement for matching chromosome, position and listed samples with required dp
		## print document["rec"]["chr"], document["rec"]["pos"], target[2:4]
		# count if they are larger than 7
		counter += 1

# display results
print counter, "hits found with depth of sample 3 & 4 larger than 7!" 



