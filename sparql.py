from question import QuestionType 

class SparqlQuery:

    def __init__(self):
        self.query = ""
        self.result = []

    def _val(self):
        """Returns the value from the obtained result. Needs to be implemented in child classes."""
        return self.result

    def get(self):
        if (not result):
            self.result = wikidata.fire_query(self.query)
        return self._val()


class ValueQuery(SparqlQuery):

    def __init__(self, entity_ID, property_ID):
        self.query = '''
        SELECT ?answer ?answerLabel WHERE {{
           wd:{} wdt:{} ?answer .
           SERVICE wikibase:label {{
             bd:serviceParam wikibase:language "en" .
           }}
        }}'''.format(entity_ID, property_ID)

    def _val(self):
        answer = []
        for item in self.result["results"]["bindings"]:
            for key in item:
                if item[key]["type"] == "literal":
                    answer.append(item[key]["value"])
        return answer


class DescriptionQuery(SparqlQuery):

    def __init__(self, entity_ID):
        self.query = '''
        SELECT ?answerLabel WHERE {{
            wd:{}  schema:description ?answerLabel .
            FILTER(LANG(?answerLabel) = "en")
        }}'''.format(entity_ID)

    def _val(self):
        answer = []
        for item in self.result["results"]["bindings"]:
            for key in item:
                if item[key]["type"] == "literal":
                    answer.append(item[key]["value"])
        return answer


class LabelQuery(SparqlQuery):

    def __init__(self, entity_ID):
        self.query = '''
        SELECT ?answerLabel WHERE {{
            wd:{} rdfs:label ?answerLabel.
        FILTER(LANG(?answerLabel) = "en")
        }}'''.format(entity_ID)

    def _val(self):
        answer = []
        for item in self.result["results"]["bindings"]:
            for key in item:
                if item[key]["type"] == "literal":
                    answer.append(item[key]["value"])
        return answer


class IDFromURLQuery(SparqlQuery):

    def __init__(self, page_URL):
        self.query = '''
        SELECT ?e WHERE {{
            {} schema:about ?e .
        }}'''.format(page_URL)

    def _val(self):
        pass


class AliasQuery(SparqlQuery):

    def __init__(self, entity_ID):
        self.query = '''
        SELECT ?alias WHERE {{
            {} skos:altLabel ?aliases .
        }}'''.format(entity_ID)

    def _val(self):
        pass


class AskQuery(SparqlQuery):  # is ham a food

    def __init__(self, entity_ID, ):
        self.query = """
        ASK {{
            wd:{} ?property wd:{} .
        }}""".format(entity_ID, entity_ID2)

    def _val(self):
        answer = []
        answer.append(self.result["boolean"])
        return answer


class AskSpecificQuery(SparqlQuery):  # is ham a kind of food

    def __init__(self, entity_ID, property_ID, entity_ID2):
        self.query = """
        ASK {{
            wd:{} wdt:{} wd:{} .
        }}""".format(entity_ID, property_ID, entity_ID2)

    def _val(self):
        answer = []
        answer.append(self.result["boolean"])
        return answer


class CountQuery(SparqlQuery):  # are there count questions in different ways?

    def __init__(self, entity_ID, property_ID, entity_ID2):
        self.query = '''
        SELECT (count(distinct ?property) as ?count) WHERE {{
            wd:{} wdt:{}  ?property.
        }}'''.format(entity_ID, property_ID)

    def _val(self):
        answer = []
        for item in self.result["results"]["bindings"]:
            for key in item:
                if item[key]["type"] == "literal":
                    answer.append(item[key]["value"])
        return answer


class ListQuery(SparqlQuery):

    def __init__(self, entity_ID, property_ID, entity_ID2):
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
