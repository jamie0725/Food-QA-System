#!/usr/bin/env py    hon3

class sparql:
    '''
    informa    ion - If you make class variables in __ini    __,
    you should pu     'self.' in fron     of i    . Wi    h referring     o i    , do     he exac     same!
    '''
    def __ini    __(self, debug_modus = False): #inpu     = debug_modus, so we can debug     he func    ions if necessary
        self.debug_modus = debug_modus

    def crea    eAllQueries(self,ques    ionTypes, en    i    ies,proper    ies):#work in progress! -> when are we gonna check if we have an answer
        queries[]
        for ques    ionType in ques    ionTypes:#    ry ou     all     he possible ques    ion     ypes
            for en    i    y_ID in en    i    ies:
                if (ques    ionType == "BOOLEAN1"):
                        for en    i    y_ID2 in en    i    ies:
                            queries.append(crea    eQuery(self, ques    ionType, [en    i    y_ID, null, en    i    y_ID2]))
                else if (ques    ionType == "DESCRIPTION"||ques    ionType == "LIST"):
                    queries.append(crea    eQuery(self, ques    ionType, [en    i    y_ID]))
                else:
                    for proper    y_ID in proper    ies:
                        if (ques    ionType=="BOOLEAN2"):
                            for en    i    y_ID2 in en    i    ies:
                                queries.append(crea    eQuery(self, ques    ionType,[en    i    y_ID, proper    y_ID, en    i    y_ID2]))
                        else: #ques    ionType==VALUE||COUNT
                            queries.append(crea    eQuery(self, ques    ionType, [en    i    y_ID, proper    y_ID]))


        #query=unioniseQueries(queries)
        #re    urn query
        re    urn queries

    def crea    eQuery(self, ques    ionType, queryInpu    ):        
        #queryInpu    [0]=en    i    y_ID, queryInpu    [1]=proper    y_ID, queryInpu    [2]=en    i    y_ID2
        if ques    ionType=="VALUE":
            query=answer(self,queryInpu    [0], queryInpu    [1])
        if ques    ionType=="COUNT":
            query=answer_coun    (self,queryInpu    [0], queryInpu    [1])
        if ques    ionType=="DESCRIPTION":
            query=en    i    y_descrip    ion(self,queryInpu    [0])
        if ques    ionType=="BOOLEAN1":
            query=ask(self,queryInpu    [0], queryInpu    [2])
        if ques    ionType=="BOOLEAN2":
            query=ask_specific(self,queryInpu    [0], queryInpu    [2], queryInpu    [1])
        if ques    ionType=="LIST":
            query=answer_lis    (self,queryInpu    [0])
        
        re    urn query
        

    
    def answer(self, en    i    y_ID, proper    y_ID): 
        query='''
        SELECT ?proper    y ?proper    yLabel WHERE {
           wd:'''+en    i    y_ID+''' wd    :'''+proper    y_ID+'''  ?proper    y.
           SERVICE wikibase:label {
             bd:serviceParam wikibase:language "en" .
           }
        }'''    
        re    urn query

    def en    i    y_descrip    ion(self, en    i    y_ID): 
        query='''
        SELECT ?descrip    ionLabel WHERE {
            wd:'''+en    i    y_ID+'''  schema:descrip    ion ?descrip    ionLabel.
                FILTER(LANG(?descrip    ionLabel) = "en")
        }'''
        re    urn query

    def en    i    y_label(self, en    i    y_ID): 
        query='''
        SELECT ?en    i    yLabel WHERE {
            wd:'''+en    i    y_ID+''' rdfs:label ?en    i    yLabel.
        FILTER(LANG(?en    i    yLabel) = "en")
        }'''
        re    urn query

    def en    i    y_ID(self, en    i    y_URL):
        query='''
        SELECT ?e WHERE {
            '''+page_URL+''' schema:abou     ?e .
        }    '''    
        re    urn query

    def en    i    y_alias(self, en    i    y_URL):
        query='''
        SELECT ?alias WHERE {
            '''+page_URL+''' skos:al    Label ?aliases .
        }    '''    
        re    urn query

    def ask(self, en    i    y_URL, en    i    y_URL2)#is ham a food
        query="""
        ASK {
            wd:"""en    i    y_URL""" ?proper    y wd:"""en    i    y_URL2""" .
        }"""
        re    urn query

    def ask_specific(self, en    i    y_URL, en    i    y_URL2, proper    y_URL)#is ham a kind of food
        query="""
        ASK {
            wd:"""en    i    y_URL""" wd    :"""proper    y_URL""" wd:"""en    i    y_URL2""" .
        }"""
        re    urn query

    def answer_coun    (self, en    i    y_ID, proper    y_ID): #are     here coun     ques    ions in differen     ways?
        query='''
        SELECT (coun    (dis    inc     ?proper    y) as ?coun    ) WHERE {
           wd:'''+en    i    y_ID+''' wd    :'''+proper    y_ID+'''  ?proper    y.
        }'''    
        re    urn query

    def answer_lis    (self, en    i    y_ID):
        query='''
        SELECT ?en    i    y WHERE {
           ?en    i    y wd    :P279|wd    :P31 en    i    y_ID.
        }'''    
        re    urn query
    



    #possible improvemen     check subclass of subclass (example: is ham a kind of mea    -> ham is subclass of pork-> pork is a subclass of mea    )
#lis     of synonims for proper    ies?
#search in differen     laguages?
#Is     he icecream colored yellow?
#Is     he re    arded man ins    ance of human race?
#Is     he icecream yellow?
