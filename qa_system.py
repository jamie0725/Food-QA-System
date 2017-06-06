#!/usr/bin/env python3
import sys
import spacy

from classes.question import question
from classes.answer import answer

from functions.print import example_questions
from functions.print import ask_new_question

example_questions()
ask_new_question()

nlp = spacy.load('en_default')

#make class variables

try:
	for asked_question in sys.stdin: #every question on a new line
		question = question(nlp, asked_question, debug_modus = True)
		answer = answer(asked_question, debug_modus = True)
		question_type = question.select_question_type()
		if question_type == 'value': #list or simple questions
			entity, property = question.analyze_value_question() 
			#answer.formulate_answer(entity, property)
		elif question_type == 'count': #how much questions
			pass
		elif question_type == 'boolean': #yes no questions
			pass
		elif question_type == 'others??': #add other options
			pass
except KeyboardInterrupt: #ctrl+c won't return an error
	pass