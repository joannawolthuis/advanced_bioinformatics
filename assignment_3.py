from faker import Factory
import random

def random_rdf(n, filename):
	fake = Factory.create("nl_NL")

	uri = "http://biobeat.org/rdf/ns#"

	# initiate rdf file
	rdf = open(str(filename+".rdf"), "w+")

	cities = []
	for i in range(10):
		city = fake.address().split("\n")[2]
		cities.append(city)

	rdf.write("@prefix : <" + uri + "> .\n")

	for i in range(1, n + 1):
		name = fake.name().encode('utf-8').strip()
		city = random.choice(cities).encode('utf-8').strip()
		bsn = fake.profile()["ssn"].encode('utf-8').strip()
		phone_nr = fake.phone_number().replace(" ", "").encode('utf-8').strip()
		query_id = name.replace(" ", "") + "_" + bsn + "_id_" + str(i)
		rdf.write(":" + query_id + "\n")
		rdf.write("  :query_id \"" + query_id + "\" ;\n")
		rdf.write("  :name \"" + name + "\" ;\n")
		rdf.write("  :city \"" + city + "\" ;\n")
		rdf.write("  :phone_nr \"" + phone_nr + "\" ;\n")
		rdf.write("  :bsn "+ bsn + " .\n")

random_rdf(30, "random_db")
