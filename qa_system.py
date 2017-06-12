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
    for line in sys.stdin:
        question = Question(line, nlp)
        answer = Answer(question, print_count, nlp)
        answer.print_it() 
except KeyboardInterrupt: # ctrl+c won't return an error
    pass
