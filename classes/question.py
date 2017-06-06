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
		
		self.nlp = spacy.load('en_default')		
		self.debug_modus = debug_modus

	def select_question_type(self):
		#check regex!

		#TODO @Vincent's part! work with self.question (the input question)
		question_type = 'value' #just to continue
		return question_type

	'''
	The first argument of functions that are in a class use self as input. 
	However, this is only with defining a function, not with calling a function.
	'''

	def analyze_value_question(self): #input = question on a line
		processed_question = self.nlp(self.asked_question)

		possible_subjects = []
		possible_objects = []
		for w in processed_question:
			print(w.lemma_, w.tag_, w.dep_)
			if w.dep_ == 'nsubj':
				for d in w.subtree:
					possible_subjects.append(d.lemma_)
			if w.dep_ in ['pobj', 'dobj']:
				for d in w.subtree:
					possible_objects.append(d.lemma_)

		print(possible_subjects)
		print(possible_objects)
		#subject = get_subject()

		#object = get_object()
		
		#format the subject and object if necessary
		#subject = format_string(subject)
		#object = format_string(object)
		
	
		#if self.debug_modus == True:
		#	print('Subject = {}, Object = {}'.format(subject, object))

		#try:
		#	return object, subject #list, list
		#except: #if the script couldn't find a subject or object
		return 'unknown', 'unknown' #or something else

	
	def analyze_boolean_question(self):
		pass

	def analyze_count_question(self):
		pass