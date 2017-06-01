#!/usr/bin/env python3

class sparql:
	'''
	information - If you make class variables in __init__,
	you should put 'self.' in front of it. With referring to it, do the exact same!
	'''
	def __init__(self, debug_modus = False): #input = debug_modus, so we can debug the functions if necessary
		self.debug_modus = debug_modus

	def answer(self, entity_ID, property_ID): 
		query='''
		SELECT ?property ?propertyLabel WHERE {
		   wd:'''+entity_ID+''' wdt:'''+property_ID+'''  ?property.
		   SERVICE wikibase:label {
		     bd:serviceParam wikibase:language "en" .
		   }
		}'''	
		return query

	def entity_description(self, entity_ID): 
		query='''
		SELECT ?descriptionLabel WHERE {
			wd:'''+entity_ID+'''  schema:description ?descriptionLabel.
		    	FILTER(LANG(?descriptionLabel) = "en")
		}'''
		return query

	def entity_label(self, entity_ID): 
		query='''
		SELECT ?entityLabel WHERE {
			wd:'''+entity_ID+''' rdfs:label ?entityLabel.
		FILTER(LANG(?entityLabel) = "en")
		}'''
		return query

	def entity_ID(self, entity_URL):
		query='''
		SELECT ?e WHERE {
			'''+page_URL+''' schema:about ?e .
		}	'''	
		return query