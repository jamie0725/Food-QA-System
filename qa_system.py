#!/usr/bin/env python3
import sys

from classes.question import question
from classes.answer import answer

from functions.print import example_questions
from functions.print import ask_new_question

example_questions()
ask_new_question()


question = question(debug_modus = True)
answer = answer(debug_modus = True)
#make class variables

try:
	for asked_question in sys.stdin: #every question on a new line
		question.asked_question = asked_question
		answer.asked_question = asked_question

		question_type = question.select_question_type()
		if question_type == 'value': #list or simple questions
			entity_strings, property_strings = question.analyze_value_question() 
			#answer.formulate_answer(entity_strings, property_strings)
		elif question_type == 'boolean': #yes no questions
			entity_strings, property_strings = question.analyze_boolean_question() 
		elif question_type == 'count': #how much questions
			entity_strings, property_strings = question.analyze_count_question() 
		elif question_type == 'description': #add other options
			entity_strings = question.analyze_description_question() 
		
		ask_new_question()
except KeyboardInterrupt: #ctrl+c won't return an error
	pass