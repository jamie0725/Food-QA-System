#!/usr/bin/env python3
import spacy

from functions.base import format_string

#class to retrieve the object and subject from a sentence
class question:
	'''
	information - If you make class variables in __init__,
	you should put 'self.' in front of it. With referring to it, do the exact same!
	'''
	def __init__(self, debug_modus = False): #input = debug_modus, so we can debug the functions if necessary
		self.nlp = spacy.load('en_default') #load spacy for the whole class once
		self.debug_modus = debug_modus

	'''
	The first argument of functions that are in a class use self as input. 
	However, this is only with defining a function, not with calling a function.
	'''
	
	#TODO besides the entity and property, we can make a distinguish 
	#feature in this function like: simple answer, list, counts, yes/no
	def analyze_question(self, question): #input = question on a line
		processed_question = self.nlp(question)

		if self.debug_modus == True:
			subject = 'founded by'
			object = 'kfc'

		#TODO: implement all the functions to identify the subject and object

		##subject = get_subject()

		##object = get_object()
		
		#format the subject and object if necessary
		subject = format_string(subject)
		object = format_string(object)
		
	
		if self.debug_modus == True:
			print('Subject = {}, Object = {}'.format(subject, object))

		try:
			return object, subject #list, list
		except: #if the script couldn't find a subject or object
			return 'unknown', 'unknown' #or something else

	
	