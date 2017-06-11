from question import QuestionType
import requests
import re

class SparqlQuery:

    def __init__(self):
        self.query = ""
        self.result = []

    def _val(self):
        """Returns the value from the obtained result.wer"""
        return self.result

    def firequery(query):
        return requests.get("https://query.wikidata.org/sparql", params={'query': query, 'format': 'json'}).json()

    def get(self):
        if (not result):
            self.result = wikidata.fire_query(self.query)
        return self._val()


class ValueQuery(SparqlQuery):

    def __init__(self, entity_ID, property_ID):
        self.query = '''
        SELECT ?answer ?answerLabel WHERE {
           wd:'''+entity_ID+''' wdt:'''+property_ID+'''  ?answer.
           SERVICE wikibase:label {
             bd:serviceParam wikibase:language "en" .
           }
        }'''

    def _val(self):
        answer = []
        for item in data["results"]["bindings"]:
            for key in item:
                if item[key]["type"] == "literal":
                    print(item[key]["value"])
                    answer.append(item[key]["value"])
        return answer


class DescriptionQuery(SparqlQuery):

    def __init__(self, entity_ID):
        self.query = '''
        SELECT ?descriptionLabel WHERE {
            wd:'''+entity_ID+'''  schema:description ?descriptionLabel.
                FILTER(LANG(?descriptionLabel) = "en")
        }'''

    def _val(self):
        pass


class LabelQuery(SparqlQuery):

    def __init__(self, entity_ID):
        self.query = '''
        SELECT ?answerLabel WHERE {
            wd:'''+entity_ID+''' rdfs:label ?answerLabel.
        FILTER(LANG(?answerLabel) = "en")
        }'''

    def _val(self):
        pass


class IDFromURLQuery(SparqlQuery):

    def __init__(self, entity_URL):
        self.query = '''
        SELECT ?e WHERE {
            '''+page_URL+''' schema:about ?e .
        }    '''

    def _val(self):
        pass


class AliasQuery(SparqlQuery):

    def __init__(self, entity_URL):
        self.query = '''
        SELECT ?alias WHERE {
            '''+page_URL+''' skos:altLabel ?aliases .
        }'''

    def _val(self):
        pass


class AskQuery(SparqlQuery):  # is ham a food

    def __init__(self, entity_ID, entity_ID2):
        self.query = """
        ASK {
            wd:"""entity_URL""" ?property wd:"""entity_URL2""" .
        }"""

    def _val(self):
        pass


class AskSpecificQuery(SparqlQuery):  # is ham a kind of food

    def __init__(self, entity_ID, property_URL, entity_ID2):
        self.query = """
        ASK {
            wd:"""entity_URL""" wdt:"""property_URL""" wd:"""entity_URL2""" .
        }"""

    def _val(self):
        pass


class CountQuery(SparqlQuery):  # are there count questions in different ways?

    def __init__(self, entity_ID, property_URL, entity_ID2):
        self.query = '''
        SELECT (count(distinct ?property) as ?count) WHERE {
           wd:'''+entity_ID+''' wdt:'''+property_ID+'''  ?property.
        }'''

    def _val(self):
        pass


class ListQuery(SparqlQuery):

    def __init__(self, entity_ID, property_URL, entity_ID2):
        self.query = '''
        SELECT ?entity WHERE {
           ?entity wdt:P279|wdt:P31 entity_ID. ### TODO BUG
        }'''

    def _val(self):
        pass

# possible improvement check subclass of subclass (example: is ham a kind of meat-> ham is subclass of pork-> pork is a subclass of meat)
# list of synonims for properties?
# search in different laguages?
# Is the icecream colored yellow?
# Is the retarded man instance of human race?
# Is the icecream yellow?

