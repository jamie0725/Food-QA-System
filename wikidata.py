import requests
import sparql
import logging

SPARL_ENDPOINT_URL = 'https://query.wikidata.org/sparql'
WIKIDATA_API_URL = 'https://www.wikidata.org/w/api.php'


# def get_values(entity_IDs, property_IDs):
#     answers = {}
#     # This is only for the basic method (what is X of Y)
#     for e_ID in entity_IDs:
#         for p_ID in property_IDs:
#             sparql = self.sparql.answer(e_ID, p_ID)
#             query = 
#             data = requests.get(SPARL_ENDPOINT_URL, params={
#                                 'query': sparql, 'format': 'json'}).json()
#             for item in data['results']['bindings']:
#                 for var in item:
#                     if "Label" in var:

#                         try:
#                             answers[e_ID].append(item[var]['value'])
#                         except KeyError:  # if the e_ID doesn't occur in the dict
#                             answers[e_ID] = [item[var]['value']]
#     return answers


def get_entity_IDs(entity_name):
    entity_IDs = []
    # if the entity_name couldn't be found in english, try other langugages
    for language in ['en', 'de', 'fr', 'nl', 'es', 'it']:
        params = {'action': 'wbsearchentities',
                  'language': language,
                  'format': 'json',
                  'search': entity_name}

        entity_IDs = get_IDs(params)
        if entity_IDs:
            return entity_IDs
    return entity_IDs


def get_property_IDs(property_name):
    logging.debug("get_property_IDs, for {}".format(property_name))
    property_IDs = []
    params = {'action': 'wbsearchentities',
              'type': 'property',
              'language': 'en',
              'format': 'json',
              'search': property_name}
    property_IDs = get_IDs(params)
    logging.debug("get_property_IDs, {}".format(property_IDs))
    return property_IDs


def get_IDs(params):
    json = requests.get(WIKIDATA_API_URL, params).json()
    IDs = []
    for result in json['search']:
        IDs.append(result['id'])
    return IDs


def get_entity_IDs_by_URL(entity_URLs):
    entity_IDs = []
    for url in entity_URLs:
        query = sparql.IDFromURLQuery(url)
        entity_ID = query.get()
        if entity_ID:
            logging.debug("Found ID {} from URL {}".format(entity_ID, url))
            entity_IDs.extend(entity_ID)
    return entity_IDs


def fire_query(query):
    try:
        return requests.get(SPARL_ENDPOINT_URL,
                        params={'query': query, 'format': 'json'
                                }).json()
    except:
        return []
