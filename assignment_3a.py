from faker import Factory
import random

def random_rdf(n, filename):
'''
This function generates n fake people using the 'faker' module.
Included is their SSN/BSN, city, phone number and name.
The results are written to an rdf file with name of choice. :-)
'''
	# use dutch locale for fun dutch names
	fake = Factory.create("nl_NL")
	# placeholder uri to use later on
	uri = "http://biobeat.org/rdf/ns#"
	# create rdf file based on user input
	rdf = open(str(filename+".rdf"), "w+")
	# generate 10 cities for the fake people to live in
	cities = []
	for i in range(10):
		# results of address are (each on new line) street, postal code, city
		city = fake.address().split("\n")[2]
		cities.append(city)

	# add first line to rdf file
	rdf.write("@prefix : <" + uri + "> .\n")

	# loop for generating people, encode in utf-8 for less conflict
	for i in range(1, n + 1):
		# choose city from the randomly generated list of 10 using random module
		city = random.choice(cities).encode('utf-8').strip()
		# generate fake name, bsn (part of profile generated dictionary), phone_nr
		name = fake.name().encode('utf-8').strip()
		bsn = fake.profile()["ssn"].encode('utf-8').strip()
		phone_nr = fake.phone_number().replace(" ", "").encode('utf-8').strip()
		# create a query id based on name w/o whitespace, bsn and loop iteration
		query_id = name.replace(" ", "") + "_" + bsn + "_id_" + str(i)
		# write this all to the rdf file using the turtle format
		rdf.write(":" + query_id + "\n")
		rdf.write("  :query_id \"" + query_id + "\" ;\n")
		rdf.write("  :name \"" + name + "\" ;\n")
		rdf.write("  :city \"" + city + "\" ;\n")
		rdf.write("  :phone_nr \"" + phone_nr + "\" ;\n")
		rdf.write("  :bsn "+ bsn + " .\n")

# apply function :-)
random_rdf(30, "random_db")
