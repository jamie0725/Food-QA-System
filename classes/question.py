#!/usr/bin/env python3
import spacy
from collections import OrderedDict

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
		
		words = []
		tags = []
		deps = []
		head_deps = []
		object_counter = 0
		subject_counter = 0
		for w in processed_question:
			words.append(w.lemma_)
			tags.append(w.tag_)
			deps.append(w.dep_)
			head_deps.append(w.head.dep_)
			if w.dep_ in ['dobj', 'pobj||prep', 'pobj', 'pcomp']:
				object_counter += 1
			if w.dep_ in ['nsubj', 'nsubjpass']:
				subject_counter += 1
		
		x = 0
		occur_list = {	'words': 	words,
				'tags':		tags,
				'deps':		deps,
				'head_deps':	head_deps}
		
		print(occur_list)

		subject = []
		subject_status = False
		subject, subject_status = self.get_value(occur_list, subject, subject_status, ['nsubj'])
		subject, subject_status = self.get_value(occur_list, subject, subject_status, ['nsubjpass'])
		if subject_status == False:
			subject, subject_status = self.get_value(occur_list, subject, subject_status, ['attr'])

		object = []
		object_status = False
		object, object_status = self.get_value(occur_list, object, object_status, ['pobj'])
		object, object_status = self.get_value(occur_list, object, object_status, ['dobj'])
		
		if object_status == False:
			object, object_status = self.get_value(occur_list, object, object_status, ['pcomp'])

		if object_counter == 0:
			object, object_status = self.get_value(occur_list, object, object_status, ['nsubj'])
		
		if subject_counter == 0:
			subject, subject_status = self.get_value(occur_list, subject, subject_status, ['pobj'])
			subject, subject_status = self.get_value(occur_list, subject, subject_status, ['dobj'])

		subject = list(OrderedDict((x, True) for x in subject).keys()) #strange method for removing duplicates (but order remains the same)
		object = list(OrderedDict((x, True) for x in object).keys())
	
		if self.debug_modus == True:
			print('Subject = {}, Object = {}'.format(subject, object))

		try:
			return object, subject #list, list
		except: #if the script couldn't find a subject or object
			return 'unknown', 'unknown' #or something else

	def get_value(self, occur_list, value, status, sent_deps):
		words = occur_list['words']
		tags = occur_list['tags']
		deps = occur_list['deps']
		head_deps = occur_list['head_deps']
		for length in range(-3, 0):

			x = 0
			y = 0

			length = abs(length) #length is for trigram and bigram (length 3 = trigram, length 2 = bigram, 1 = uni)
			match_x_before = [sent_deps]
			match_x_after = [sent_deps]
			for i in range(0, length):
				if i > 0:
					match_x_before = [self.preparation_deps()] + match_x_before
				if i == 1:
					match_x_after = match_x_after + [self.conjunction_deps()] + [self.conjuncted_deps()]
		
			for w in words:
				if y+length < len(words) and tags[x] not in self.ignore_tag_list():
					match_y = deps[x:y+length]
					checker_match_before = 0 #checks whether the whole n-gram corresponds
					checker_match_after = 0
					for i in range(0, len(match_y)):
						if match_y[i] in match_x_before[i]:
							checker_match_before += 1
							if checker_match_before == len(match_y):
								value.append(format_string(' '.join(words[x:y+length])))
								status = True
						if match_y[i] in match_x_after[i]:
							checker_match_after += 1
							if checker_match_after == len(match_y):
								value.append(format_string(' '.join(words[x:y+length])))
								status = True
				x += 1
				y += 1
		return value, status			
	
	def analyze_boolean_question(self):
		pass

	def analyze_count_question(self):
		pass

	def preparation_deps(self): #prep alleen tussen 2 obj en dobj
		return ['compound', 'amod', 'poss', 'case']
	def conjunction_deps(self): #prep alleen tussen 2 obj en dobj
		return ['prep', 'cc']
	def conjuncted_deps(self):
		return ['pobj', 'conj', 'attr']
	def ignore_tag_list(self):
		return ['DT', 'WP', 'WDT']