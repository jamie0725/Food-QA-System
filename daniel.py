import sys
import requests
import re


    

def firequery(query):
    return requests.get("https://query.wikidata.org/sparql", params={'query': query, 'format': 'json'}).json()

def subtractAnswer(data):
	for item in data['results']['bindings']:
		for var in item:
			if "Label" in var: 
				item[var]['value']



listOfQueries=['''
SELECT ?property ?propertyLabel WHERE {
   wd:Q170486 wdt:P31  ?property.
   SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
   }
}''']

print("in main")
data=firequery(listOfQueries[0])
print(data)
print(subtractAnswer(data))