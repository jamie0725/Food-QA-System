import re

def format_string(string):
    # to avoid misspelling of f.e. Tony's Chocolonely as Tony 's Chocolonely 
    pattern = re.compile(r" 's")
    string = re.sub(pattern, "'s", string)

    # misspelling Jell-O, Jell - O
    pattern = re.compile(r" - ")
    string = re.sub(pattern, "-", string)

    if string == 'where':
        string = 'country of origin'    
    if string == 'when':
        string = 'inception'
    if string == 'make':
        string = 'has part'
    if string == 'class':
        string = 'subclass of'

    return string

def dedup(list):
    """Removes duplicates from a list"""
    return list(dict.fromKeys(list))

def flatten(list):
    """Make list of lists into list (i.e. [[1,2], [3]] -> [1,2,3])."""
    return sum(list, [])