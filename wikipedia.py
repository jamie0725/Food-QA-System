import subprocess
import pathlib
import re
import logging
import sys

class AnchorTexts:
    def __init__(self, filepath):
        self.path = pathlib.Path(filepath)
        
        if not self.path.is_file():
            raise FileNotFoundError

    def get_URLs(self, term):
        pipe = subprocess.Popen(['grep', '^' + term, 'anchor_texts'], stdout=subprocess.PIPE)
        wikipages = []
        for line in pipe.stdout:
            wikipages.append(re.split(r'\t+', line.strip().decode("utf-8")))
        wikipages.sort(key=lambda arr: int(arr[2]), reverse=True)
        logging.debug('Found wikipages for {}:\n'.format(term) +
                '\n'.join('- {}'.format(*p) for p in wikipages[:10]))
        return [el[1] for el in wikipages[:10]]
