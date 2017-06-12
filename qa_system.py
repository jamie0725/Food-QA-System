import sys
import spacy
from question import Question
from count import Count
from answer import Answer
import logging
import argparse
import wikipedia

parser = argparse.ArgumentParser(description='This is a demo.')
parser.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help="Set the logging level")

args = parser.parse_args()
if args.logLevel:
    logging.basicConfig(level=getattr(logging, args.logLevel))

try:
    # show all logging with level >= DEBUG
    nlp = spacy.load('en')
    anchor_texts = wikipedia.AnchorTexts('anchor_texts')
    print_count = Count()
    for line in sys.stdin:
        question = Question(line, nlp)
        answer = Answer(question, print_count, nlp, anchor_texts)
        answer.print_it() 
except KeyboardInterrupt: # ctrl+c won't return an error
    pass
