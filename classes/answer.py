#!/usr/bin/env python3
#this is how you import a class from a file
from classes.wikidataAPI import wikidataAPI
from classes.anchorText import anchorText

from functions.print import question as print_question
from functions.print import answer as print_answer

class answer:
	'''
	information - If you make class variables in __init__,
	you should put 'self.' in front of it. With referring to it, do the exact same!
	'''
	def __init__(self, question, debug_modus = False): #input = debug_modus, so we can debug the functions if necessary
		self.question = question
		self.debug_modus = debug_modus
		#this is how another class can be used
		self.wikidataAPI = wikidataAPI()
		self.anchorText = anchorText()
	
	'''
	The first argument of functions that are in a class use self as input. 
	However, this is only with defining a function, not with calling a function.
	'''
	def formulate_answer(self, entity, property): #input = entity, property
		#base case, calling to get_answer of this class should be done with self.get_answer()
		answer, status = self.get_answer(entity, property) #return is something like answer (string) and status (boolean).

		if status == False: #f.e. swap entity and property, try something with synonyms (with WordNet or so), etcetera
			answer, status = self.get_answer(property, entity) 
	
		#if status == False: #and go on if there is no answer found...

		
		#if no answer is found at all
		if status == False:
			print("no answer found for Question: {}. ".format(self.question))
		else:
			print_question(self.question)
			print_answer(answer)
			
	#TODO expand the function to get the right answer(s)
	def get_answer(self, entity, property):
		status = False
		'''
		To make this function efficient, we should first try to find the property.
		If no property is found, we can skip this whole process and return to formulate_answer()
		'''
		property_IDs = self.wikidataAPI.get_property_IDs(property) #return is a list of properties
		if self.debug_modus == True:
			print('property_IDs = {}'.format(property_IDs))

		if len(property_IDs) == 0: #if no property is found: just stop!
			return '', status #answer empty string, status is False

		#continue with finding the entity
		#I think wikidataAPI is more accurate, but if you think it should be the other way around, just swap them
		
		entity_IDs =  self.wikidataAPI.get_entity_IDs(entity)
		if self.debug_modus == True:
			print('wikidataAPI - entity_IDs = {}'.format(entity_IDs))
		if len(entity_IDs) > 0: #try to find an answer with wikidataAPI IDs
			answer, status = self.wikidataAPI.get_answer(entity_IDs, property_IDs)
			if self.debug_modus == True:
				print('wikidataAPI - answer = {}'.format(answer))

		#TODO anchor text!
		'''
		if status == False: #try anchorText if no answer is found
			entity_IDs = self.anchorText.get_entity_IDs(entity)
			if self.debug_modus == True:
				print('anchorText - entity_IDs = {}'.format(entity_IDs))
			if len(entity_IDs) > 0: #try to find an answer in wikidataAPI
				answer, status = self.wikidataAPI.get_answer(entity_IDs, property_IDs)
				if self.debug_modus == True:
					print('anchorText - answer = {}'.format(answer))
		'''

		return answer, status


