#!/usr/bin/env python3

from classes.wikidataAPI import wikidataAPI

class anchorText:
	'''
	information - If you make class variables in __init__,
	you should put 'self.' in front of it. With referring to it, do the exact same!
	'''

	def __init__(self, debug_modus = False): #input = debug_modus, so we can debug the functions if necessary
		self.debug_modus = debug_modus

	def get_entity_IDs(self, entity):
		matches = []

		'''
		example
		#matching_rows = re.findall("\\n.*"+ entity_val + ".*\\t.+\\t.", self.anchor_texts, re.IGNORECASE)
		for line in matching_rows:
			text, link, amount = line.strip('\n').split('\t')
			matches.append([text, link, int(amount)])
				
		matches.sort(key=lambda x: x[2], reverse=True)
		entity_URLs = []
		for text, entity_URL, amount in matches[:10]:
			entity_URLs.append(page)
	
		entity_IDs = self.wikidataAPI.get_entity_IDs_by_URL(entity_URLs)	
		return entity_IDs	
		'''