from question import QuestionType

def createAllQueries(questionTypes, entities, properties):
    queries[]
    for questionType in questionTypes:  # try out all the possible question types
        for entity_ID in entities:
            if (questionType == "BOOLEAN1"):
                for entity_ID2 in entities:
                    queries.append(createQuery(self, questionType, [
                                   entity_ID, null, entity_ID2]))
            else if (questionType == "DESCRIPTION" | |questionType == "LIST"):
                queries.append(createQuery(
                    self, questionType, [entity_ID]))
            else:
                for property_ID in properties:
                    if (questionType == "BOOLEAN2"):
                        for entity_ID2 in entities:
                            queries.append(createQuery(self, questionType, [
                                           entity_ID, property_ID, entity_ID2]))
                    else:  # questionType==VALUE||COUNT
                        queries.append(createQuery(
                            self, questionType, [entity_ID, property_ID]))

    # query=unioniseQueries(queries)
    # return query
    return queries

# removed createQuery!

def answer(entity_ID, property_ID):
    query = '''
    SELECT ?property ?propertyLabel WHERE {
       wd:'''+entity_ID+''' wdt:'''+property_ID+'''  ?property.
       SERVICE wikibase:label {
         bd:serviceParam wikibase:language "en" .
       }
    }'''
    return query

def entity_description(entity_ID):
    query = '''
    SELECT ?descriptionLabel WHERE {
        wd:'''+entity_ID+'''  schema:description ?descriptionLabel.
            FILTER(LANG(?descriptionLabel) = "en")
    }'''
    return query

def entity_label(entity_ID):
    query = '''
    SELECT ?entityLabel WHERE {
        wd:'''+entity_ID+''' rdfs:label ?entityLabel.
    FILTER(LANG(?entityLabel) = "en")
    }'''
    return query

def entity_ID(entity_URL):
    query = '''
    SELECT ?e WHERE {
        '''+page_URL+''' schema:about ?e .
    }    '''
    return query

def entity_alias(entity_URL):
    query = '''
    SELECT ?alias WHERE {
        '''+page_URL+''' skos:altLabel ?aliases .
    }    '''
    return query

def ask(entity_URL, entity_URL2)  # is ham a food
    query = """
    ASK {
        wd:"""entity_URL""" ?property wd:"""entity_URL2""" .
    }"""
    return query

# is ham a kind of food
def ask_specific(entity_URL, entity_URL2, property_URL)
    query = """
    ASK {
        wd:"""entity_URL""" wdt:"""property_URL""" wd:"""entity_URL2""" .
    }"""
    return query

# are there count questions in different ways?
def answer_count(entity_ID, property_ID):
    query = '''
    SELECT (count(distinct ?property) as ?count) WHERE {
       wd:'''+entity_ID+''' wdt:'''+property_ID+'''  ?property.
    }'''
    return query

def answer_list(entity_ID):
    query = '''
    SELECT ?entity WHERE {
       ?entity wdt:P279|wdt:P31 entity_ID.
    }'''
    return query

# possible improvement check subclass of subclass (example: is ham a kind of meat-> ham is subclass of pork-> pork is a subclass of meat)
# list of synonims for properties?
# search in different laguages?
# Is the icecream colored yellow?
# Is the retarded man instance of human race?
# Is the icecream yellow?