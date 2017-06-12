import re
from collections import OrderedDict

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

def dedup(itemlist):
    """Removes duplicates from a list"""
    return list(OrderedDict((x, True) for x in itemlist).keys())


def flatten(l):
    """Make list of lists into list (i.e. [[1,2], [3]] -> [1,2,3])."""
    return sum(l, [])

def remove_elements(l, elements):
    """Takes two lists, returns the first list with the elements that are in the second list removed"""

    new_l = [x for x in l if x not in elements]
    return new_l
