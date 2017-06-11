from question import QuestionType 

class SparqlQuery:

    def __init__(self):
        self.query = ""
        self.result = []

    def _val(self):
        """Returns the value from the obtained result.wer"""
        return self.result

    def get(self):
        if (not result):
            self.result = wikidata.fire_query(self.query)
        return self._val()


class ValueQuery(SparqlQuery):

    def __init__(self, entity_ID, property_ID):
        self.query = '''
        SELECT ?property ?propertyLabel WHERE {{
           wd:{} wdt:{} ?property .
           SERVICE wikibase:label {{
             bd:serviceParam wikibase:language "en" .
           }}
        }}'''.format(entity_ID, property_ID)

    def _val(self):
        pass


class DescriptionQuery(SparqlQuery):

    def __init__(self, entity_ID):
        self.query = '''
        SELECT ?descriptionLabel WHERE {{
            wd:{}  schema:description ?descriptionLabel .
            FILTER(LANG(?descriptionLabel) = "en")
        }}'''.format(entity_ID)

    def _val(self):
        pass


class LabelQuery(SparqlQuery):

    def __init__(self, entity_ID):
        self.query = '''
        SELECT ?entityLabel WHERE {{
            wd:{} rdfs:label ?entityLabel.
        FILTER(LANG(?entityLabel) = "en")
        }}'''.format(entity_ID)

    def _val(self):
        pass


class IDFromURLQuery(SparqlQuery):

    def __init__(self, page_URL):
        self.query = '''
        SELECT ?e WHERE {{
            {} schema:about ?e .
        }}'''.format(page_URL)

    def _val(self):
        pass


class AliasQuery(SparqlQuery):

    def __init__(self, entity_URL):
        self.query = '''
        SELECT ?alias WHERE {{
            {} skos:altLabel ?aliases .
        }}'''.format(entity_URL)

    def _val(self):
        pass


class AskQuery(SparqlQuery):  # is ham a food

    def __init__(self, entity_ID, ):
        self.query = """
        ASK {{
            wd:{} ?property wd:{} .
        }}""".format(entity_ID, entity_ID2)

    def _val(self):
        pass


class AskSpecificQuery(SparqlQuery):  # is ham a kind of food

    def __init__(self, entity_ID, property_URL, entity_ID2):
        self.query = """
        ASK {{
            wd:{} wdt:{} wd:{} .
        }}""".format(entity_ID, property_URL, entity_ID2)

    def _val(self):
        pass


class CountQuery(SparqlQuery):  # are there count questions in different ways?

    def __init__(self, entity_ID, property_URL, entity_ID2):
        self.query = '''
        SELECT (count(distinct ?property) as ?count) WHERE {{
            wd:{} wdt:{}  ?property.
        }}'''.format(entity_ID, property_ID)

    def _val(self):
        pass


class ListQuery(SparqlQuery):

    def __init__(self, entity_ID, property_URL, entity_ID2):
        self.query = '''
        SELECT ?entity WHERE {{
            ?entity wdt:P279|wdt:P31 entity_ID. ### TODO BUG
        }}'''

    def _val(self):
        pass

# possible improvement check subclass of subclass (example: is ham a kind of meat-> ham is subclass of pork-> pork is a subclass of meat)
# list of synonims for properties?
# search in different laguages?
# Is the icecream colored yellow?
# Is the retarded man instance of human race?
# Is the icecream yellow?
