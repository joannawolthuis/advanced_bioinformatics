import urllib
import httplib2
import json
import networkx as nx
import matplotlib.pyplot as plt

# define prefixes and variables needed for sparql query
pf_friend = '<http://localhost:8080/openrdf-sesame/repositories/001#friend>'
pf_name = '<http://localhost:8080/openrdf-sesame/repositories/001#name>'
repository = '001'
endpoint = "http://localhost:8080/openrdf-sesame/repositories/%s" % (repository)

# define sparql query 1: retrieve all people in the db and their friend
query = 'SELECT ?name ?friend WHERE { ?person %s ?friend; %s ?name.}' %(pf_friend, pf_name)

# start posting sparql query 1
print "POSTing SPARQL query to %s" % (endpoint)
params = { 'query': query }
headers = { 
  'content-type': 'application/x-www-form-urlencoded', 
  'accept': 'application/sparql-results+json' 
}
(response, content) = httplib2.Http().request(endpoint, 'POST', urllib.urlencode(params), headers=headers)

# retrieve results in json format
print "Response %s" % response.status
match_results = json.loads(content)

# second query: retrieve popularity (who is listed as friend most often?)
query = 'SELECT ?friend(COUNT(?friend) as ?popularity){?person %s    ?friend.} GROUP BY ?friend' %pf_friend

# post query 2
print "POSTing SPARQL query to %s" % (endpoint)
params = { 'query': query }
(response, content) = httplib2.Http().request(endpoint, 'POST', urllib.urlencode(params), headers=headers)

# retrieve results
print "Response %s" % response.status
pop_results = json.loads(content)

# narrow down json branch where the actual results are stored
pop_list = pop_results['results']['bindings']

# create dictionary for storing popularity values
popularity_storage = {}

# match names to popularity values and add to dictionary
for line in pop_list:
	name = json.dumps(line['friend']['value']).strip("\"")
	popularity = json.dumps(line['popularity']['value']).strip("\"")
	popularity_storage[name] = popularity

# create a color gradient for use in graph based on popularity score
color_gradient = {0:"b", 1:"g", 2:"r", 3:"c", 4:"m", 5:"y"}

# narrow down json branch where the results are stored
match_list = match_results['results']['bindings']

# define graph

G=nx.Graph()

# go through the friend matches
for line in match_list:
	name = json.dumps(line['name']['value']).strip("\"")
	# check if they are a friend of someone or not
	if name in popularity_storage.keys():
		G.add_node(name)
	# if not, add them with value 0.5 for later node size
	elif name not in popularity_storage.keys():
		G.add_node(name)
		popularity_storage[name] = 0
	# define friend
	friend = json.dumps(line['friend']['value']).strip("\"")
	# create connections between names and friends 
	G.add_edge(*(name, friend))

'''
Draw graph.
node_size is defined by popularity storage * 100 (default size is 300). 
If the person has only one connection, their size becomes 50.
Node color is defined by mapping the popularity value to the color gradient dictionary. :-)
'''
nx.draw_circular(G, node_size = [100 * int(popularity_storage[str(node)]) if int(popularity_storage[str(node)]) > 0 else 50 for node in G],node_color=[popularity_storage[str(node)] for node in G])

plt.show()
