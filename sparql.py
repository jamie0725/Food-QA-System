from question import QuestionType 
import wikidata
import logging

class SparqlQuery:

    def __init__(self):
        self.query = ""
        self.result = []

    def _val(self):
        """Returns the value from the obtained result. Needs to be implemented in child classes."""
        return self.result

    def get(self):
        try:
            if (not self.result):
                self.result = wikidata.fire_query(self.query)
                logging.debug("QUERY:\n{}\nRESULT:\n{}\n".format(self.query, self.result))
            return self._val()
        except:
            return None


class ValueQuery(SparqlQuery):

    def __init__(self, entity_ID, property_ID):
        super().__init__()
        self.query = '''
        SELECT ?answer ?answerLabel WHERE {{
           wd:{} wdt:{} ?answer .
           SERVICE wikibase:label {{
             bd:serviceParam wikibase:language "en" .
           }}
        }}'''.format(entity_ID, property_ID)
        
        

    def _val(self):
        val = []
        for item in self.result["results"]["bindings"]:
            for key in item:
                if item[key]["type"] == "literal":
                    val.append(item[key]["value"])
        return val


class DescriptionQuery(SparqlQuery):

    def __init__(self, entity_ID):
        super().__init__()
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
        super().__init__()
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
        super().__init__()
        self.query = '''
        SELECT ?e WHERE {{
            {} schema:about ?e .
        }}'''.format(page_URL)

    def _val(self):
        answer = []
        for item in self.result["results"]["bindings"]:
            for key in item:
                 answer.append(item["e"]["value"].replace("http://www.wikidata.org/entity/",""))
        return answer


class AliasQuery(SparqlQuery):

    def __init__(self, entity):
        super().__init__()
        self.query = """SELECT ?alias WHERE {{
            ?alias wdt:P279|wdt:P31 ?something.
            ?alias wdt:P646 ?whatever.
            ?alias skos:altLabel  ?y.
            FILTER regex(?y, {})
        }}""".format(entity_ID)

    def _val(self):
        answer = []
        for item in self.result["results"]["bindings"]:
            for key in item:
                if item[key]["type"] == "literal":
                    answer.append(item[key]["value"])
        return answer


class AskQuery(SparqlQuery):  # is ham a food

    def __init__(self, entity_ID, entity_ID2):
        super().__init__()
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
        super().__init__()
        self.query = """
        ASK {{
            wd:{} wdt:{} wd:{} .
        }}""".format(entity_ID, property_ID, entity_ID2)
        
        if property_ID == "P279" or property_ID == "P31":
            self.query = """ASK {{
               {{wd:{} wdt:P279|wdt:P31 wd:{}.
                }}UNION{{
                wd:{} wdt:P279|wdt:P31 ?whatever.
                ?whatever wdt:P279|wdt:P31 wd:{}.
                }}UNION{{
                wd:{} wdt:P279|wdt:P31 ?whatever.
                ?whatever wdt:P279|wdt:P31 ?whatever.
                ?whatever wdt:P279|wdt:P31 wd:{}.
                }} }}""".format(entity_ID, entity_ID2,entity_ID, entity_ID2,entity_ID, entity_ID2)

    def _val(self):
        answer = []
        answer.append(self.result["boolean"])
        return answer


class CountQuery(SparqlQuery):  # are there count questions in different ways?

    def __init__(self, entity_ID, property_ID, entity_ID2):
        super().__init__()
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

    def __init__(self, entity_ID):
        super().__init__()
        self.query = """SELECT ?answer ?answerLabel WHERE {{
                {{?answer wdt:P279|wdt:P31 wd:{}.
                SERVICE wikibase:label {{
                bd:serviceParam wikibase:language "en" .
                }}
                }}UNION{{
                ?answer wdt:P279|wdt:P31 ?whatever.
                ?whatever wdt:P279|wdt:P31 wd:{}.
                SERVICE wikibase:label {{
                bd:serviceParam wikibase:language "en" .
                }}
                }}UNION{{
                ?answer wdt:P279|wdt:P31 ?whatever.
                ?whatever wdt:P279|wdt:P31 ?whatever.
                ?whatever wdt:P279|wdt:P31 wd:{}.
                SERVICE wikibase:label {{
                bd:serviceParam wikibase:language "en" .
                }}
                }} }}""".format(entity_ID, entity_ID, entity_ID)

    def _val(self):
        answer = []
        for item in self.result["results"]["bindings"]:
            for key in item:
                if item[key]["type"] == "literal":
                    answer.append(item[key]["value"])
        return answer

# possible improvement check subclass of subclass (example: is ham a kind of meat-> ham is subclass of pork-> pork is a subclass of meat)
#remove duplicates from entity/answer/property lists
# list of synonims for properties?
# search in different laguages?
# Is the icecream colored yellow?
# Is the retarded man instance of human race?
# Is the icecream yellow?

