#!/usr/bin/env python3


class sparql:
    '''
    information - If you make class variables in __init__,
    you should put 'self.' in front of it. With referring to it, do the exact same!
    '''

    # input = debug_modus, so we can debug the functions if necessary
    def __init__(self, debug_modus=False):
        self.debug_modus = debug_modus

    # work in progress! -> when are we gonna check if we have an answer
    def createAllQueries(self, questionTypes, entities, properties):
        queries[]
        for questionType in questionTypes:  # try out all the possible question types
            for entity_ID in entities:
                if questionType == "BOOLEAN1":
                    for entity_ID2 in entities:
                        queries.append(createQuery(self, questionType, [
                                       entity_ID, null, entity_ID2]))
                elif (questionType == "DESCRIPTION" | |questionType == "LIST"):
                    queries.append(createQuery(
                        self, questionType, [entity_ID]))
                else:
                    for property_ID in properties:
                        if questionType == "BOOLEAN2":
                            for entity_ID2 in entities:
                                queries.append(createQuery(self, questionType, [
                                               entity_ID, property_ID, entity_ID2]))
                        else:  # questionType==VALUE||COUNT
                            queries.append(createQuery(
                                self, questionType, [entity_ID, property_ID]))

        # query=unioniseQueries(queries)
        # return query
        return queries

    def createQuery(self, questionType, queryInput):
        #queryInput[0]=entity_ID, queryInput[1]=property_ID, queryInput[2]=entity_ID2
        if questionType == "VALUE":
            query = answer(self, queryInput[0], queryInput[1])
        if questionType == "COUNT":
            query = answer_count(self, queryInput[0], queryInput[1])
        if questionType == "DESCRIPTION":
            query = entity_description(self, queryInput[0])
        if questionType == "BOOLEAN1":
            query = ask(self, queryInput[0], queryInput[2])
        if questionType == "BOOLEAN2":
            query = ask_specific(
                self, queryInput[0], queryInput[2], queryInput[1])
        if questionType == "LIST":
            query = answer_list(self, queryInput[0])

        return query

    def answer(self, entity_ID, property_ID):
        query = '''
        SELECT ?property ?propertyLabel WHERE {
           wd:'''+entity_ID+''' wdt:'''+property_ID+'''  ?property.
           SERVICE wikibase:label {
             bd:serviceParam wikibase:language "en" .
           }
        }'''
        return query

    def entity_description(self, entity_ID):
        query = '''
        SELECT ?descriptionLabel WHERE {
            wd:'''+entity_ID+'''  schema:description ?descriptionLabel.
                FILTER(LANG(?descriptionLabel) = "en")
        }'''
        return query

    def entity_label(self, entity_ID):
        query = '''
        SELECT ?entityLabel WHERE {
            wd:'''+entity_ID+''' rdfs:label ?entityLabel.
        FILTER(LANG(?entityLabel) = "en")
        }'''
        return query

    def entity_ID(self, entity_URL):
        query = '''
        SELECT ?e WHERE {
            '''+page_URL+''' schema:about ?e .
        }    '''
        return query

    def entity_alias(self, entity_URL):
        query = '''
        SELECT ?alias WHERE {
            '''+page_URL+''' skos:altLabel ?aliases .
        }    '''
        return query

    def ask(self, entity_URL, entity_URL2)  # is ham a food
        query = """
        ASK {
            wd:"""entity_URL""" ?property wd:"""entity_URL2""" .
        }"""
        return query

    # is ham a kind of food
    def ask_specific(self, entity_URL, entity_URL2, property_URL)
        query = """
        ASK {
            wd:"""entity_URL""" wdt:"""property_URL""" wd:"""entity_URL2""" .
        }"""
        return query

    # are there count questions in different ways?
    def answer_count(self, entity_ID, property_ID):
        query = '''
        SELECT (count(distinct ?property) as ?count) WHERE {
           wd:'''+entity_ID+''' wdt:'''+property_ID+'''  ?property.
        }'''
        return query

    def ask_subclass(self,entity_ID,entity_ID2)#if the property is lookinf for a subclass, this one needs to be run somehow instead of the normal one
        query="""ASK {
       {wd:"""entity_ID""" wdt:P279|wdt:P31 wd:"""entity_ID2""".
        }UNION{
        wd:"""entity_ID"""wdt:P279|wdt:P31 ?whatever.
        ?whatever wdt:P279|wdt:P31 wd:"""entity_ID2""".
        }UNION{
        wd:"""entity_ID""" wdt:P279|wdt:P31 ?whatever.
        ?whatever wdt:P279|wdt:P31 ?whatever.
        ?whatever wdt:P279|wdt:P31 wd:"""entity_ID2""".
        }}"""
        return query

    def answer_list(self, entity_ID):
        query="""
        SELECT ?entity WHERE {
           ?entity wdt:P279|wdt:P31 wd:"""entity_ID""".
        }UNION{
        ?entity wdt:P279|wdt:P31 ?whatever.
        ?whatever wdt:P279|wdt:P31 wd:"""entity_ID""".
        }UNION{
        ?entity wdt:P279|wdt:P31 ?whatever.
        ?whatever wdt:P279|wdt:P31 ?whatever.
        ?whatever wdt:P279|wdt:P31 wd:"""entity_ID""".
        }.
        }"""   
        return query



    # possible improvement check subclass of subclass (example: is ham a kind of meat-> ham is subclass of pork-> pork is a subclass of meat)
# list of synonims for properties?
# search in different laguages?
# Is the icecream colored yellow?
# Is the retarded man instance of human race?
# Is the icecream yellow?
