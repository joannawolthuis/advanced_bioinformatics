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

make_compatible("pik3ca")

# exercise 1

client = MongoClient()
# i hosted the collection in the test db
db = client.test
# this code will use the collection assignment_2 where the converted vcf was loaded
cursor = db.assignment_2.find()

# create counter for later use
counter = 0 
# go through database collection
for document in cursor:
	# targeting the annotations "ann" specifically the Ensembl ID below
	target = document["rec"]["ann"] 
	keyword = "ENST00000263967" 
	# count the document if the Ensembl ID is in the annotations
	if keyword in target:
		counter += 1

# print results
print counter, "hits found with keyword", keyword + "!"



