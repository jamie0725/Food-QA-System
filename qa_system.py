import sys
import spacy
from question import Question
from count import Count
from answer import Answer
import logging

try:
    # show all logging with level >= DEBUG
    #logging.basicConfig(level=logging.DEBUG)
    nlp = spacy.load('en_default')
    print_count = Count()
    print('What are your questions?') #just so we know when NLP is ready (TEMPORARILY HERE)
    for line in sys.stdin:
        question = Question(line, nlp)
        answer = Answer(question, print_count, nlp)
        answer.print_it() 
       #answer.print_it_explicit() #(TEMPORARILY HERE)
except KeyboardInterrupt: # ctrl+c won't return an error
    pass
