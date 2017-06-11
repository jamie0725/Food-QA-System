import sys
import spacy
from question import Question
from count import Count
from answer import Answer
import logging

try:
    # show all logging with level >= DEBUG
    logging.basicConfig(level=logging.DEBUG)

    nlp = spacy.load('en')
    print_count = Count()

<<<<<<< HEAD
		question_types = question.select_question_type()
		for question_type in question_types:
			if question_type in ['VALUE', 'LIST', 'COUNT', 'BOOLEAN']: #list or simple questions
				entity_strings, property_strings = question.analyze_value_question() 
				answer.formulate_answer(entity_strings, property_strings)
			elif question_type == 'DESCRIPTION': #add other options
				entity_strings = question.analyze_description_question() 
				answer.formulate_answer(entity_strings, property_strings)
		
		ask_new_question()
except KeyboardInterrupt: #ctrl+c won't return an error
	pass
=======
    for line in sys.stdin:
        question = Question(line, nlp)
        answer = Answer(question, print_count, nlp)
        answer.print_it()
except KeyboardInterrupt: # ctrl+c won't return an error
    pass
>>>>>>> e5a00d477fb36cd9518ce246360bb9a6020e6800
