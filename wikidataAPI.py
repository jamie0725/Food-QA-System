import requests

from classes.sparql import sparql


class wikidataAPI:
    '''
    information - If you make class variables in __init__,
    you should put 'self.' in front of it. With referring to it, do the exact same!
    '''
    def __init__(self, debug_modus = False): # input = debug_modus, so we can debug the functions if necessary
        self.debug_modus = debug_modus
        self.sparql_URL = 'https://query.wikidata.org/sparql'
        self.wikidataAPI_URL = 'https://www.wikidata.org/w/api.php'
        self.sparql = sparql()

    def get_answer(self, entity_IDs, property_IDs):
        answers = {}
        # This is only for the basic method (what is X of Y)
        for e_ID in entity_IDs:
            for p_ID in property_IDs:
                sparql = self.sparql.answer(e_ID, p_ID)
                data = requests.get(self.sparql_URL, params={'query': sparql, 'format': 'json'}).json()
                for item in data['results']['bindings']:
                    for var in item:
                        if "Label" in var: 
                            
                            try: 
                                answers[e_ID].append(item[var]['value'])
                            except KeyError: # if the e_ID doesn't occur in the dict
                                answers[e_ID] = [item[var]['value']]

        if len(answers) > 0:
            return answers, True # status = True
        else:
            return answers, False
    
    def get_entity_IDs(self, entity):
        entity_IDs = []
        # if the entity couldn't be found in english, try other langugages
        for language in ['en', 'de', 'fr', 'nl', 'es', 'it']:
            params = {  'action'    : 'wbsearchentities',
                    'language'  : language,
                    'format'    : 'json',
                    'search'    : entity }

            entity_IDs = self.get_IDs(params)
            if len(entity_IDs) > 0:
                return entity_IDs
        return entity_IDs

    def get_property_IDs(self, property):
        property_IDs = []
        params = {  'action'    : 'wbsearchentities',
                'type'      : 'property',
                'language'  : 'en',
                'format'    : 'json',
                'search'    : property }
        property_IDs = self.get_IDs(params)
        return property_IDs

    def get_IDs(self, params):
        json = requests.get(self.wikidataAPI_URL, params).json()
        IDs = []
        for result in json['search']:
            IDs.append(result['id'])
        return IDs

    def get_entity_IDs_by_URL(self, entity_URLs):
        entity_IDs = []
        '''
        EXAMPLE
        entity_IDs = []
        for entity_URL in entity_URLs:
            query = self.sparql.entity_ID(entity_URL)
            data = requests.get(self.sparql_URL, params={'query': query, 'format': 'json'}).json()
            for item in data['results']['bindings']:
                    for var in item:
                        entity_IDs.append(item[var]['value'].split('entity/')[1])

        '''
        # TODO 
        return entity_IDs # list