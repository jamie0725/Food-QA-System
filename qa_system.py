#!/usr/bin/env python3
import sys

from classes.question import question
from classes.answer import answer

from functions.print import example_questions
from functions.print import ask_new_question

example_questions()
ask_new_question()

#make class variables
question = question(debug_modus = True)
answer = answer(debug_modus = True)

try:
	for read_question in sys.stdin: #every question on a new line
		entity, property = question.analyze_question(read_question) 
		answer.set_question(read_question)
		answer.formulate_answer(entity, property)	
except KeyboardInterrupt: #ctrl+c won't return an error
	pass