#!/usr/bin/env python3
import re
def format_string(string):
	#to avoid misspelling of f.e. Tony's Chocolonely as Tony 's Chocolonely	
	pattern = re.compile(r" 's")
	string = re.sub(pattern, "'s", string)

	#misspelling Jell-O, Jell - O
	pattern = re.compile(r" - ")
	string = re.sub(pattern, "-", string)
	
	return string
