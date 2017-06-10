#!/usr/bin/env py    hon3
impor     spacy
impor     en_core_web_md
from collec    ions impor     OrderedDic    

from func    ions.base impor     forma    _s    ring


#class     o re    rieve     he objec     and subjec     from a sen    ence
class ques    ion:
    '''
    informa    ion - If you make class variables in __ini    __,
    you should pu     'self.' in fron     of i    . Wi    h referring     o i    , do     he exac     same!
    '''
    def __ini    __(self, debug_modus = False): #inpu     = debug_modus, so we can debug     he func    ions if necessary
        
        self.nlp = nlp = en_core_web_md.load()      
        self.debug_modus = debug_modus

        
        #check regex!
    
        #TODO @Vincen    's par    ! work wi    h self.ques    ion (    he inpu     ques    ion) append add a         he end of a lis    
    #regex (ques    ion) ->
    
    #VALUE (wha     is x of y - 1 en    i    y 1 proper    y)
    #  where
    #  who
    #  when 
    #  wha    
    #  which
    #    does no     con    ain are
    #DESCRIPTION (wan    s a desrip    ion as answer- 1 en    i    y)
      
    #COUNT (expec    s a number as answer - has en    i    y and proper    y)
    #  s    ar    s wi    h How many
      
    #BOOLEAN1 (2 en    i    ies)
    #BOOLEAN2(2     imes an en    i    y+ a proper    y) 
    
    #  S    ar    s wi    h is
    #LIST (special case of value (lis     american presiden    s) where only 1 en    i    y)
    #  s    ar    s wi    h Wha     are
      
    #  s    ill need descrip    ion
    #  difference boolean 1,2
        
    def selec    _ques    ion_    ype(self):
            re    urn ['VALUE', 'COUNT', 'BOOLEAN', 'LIST', 'DESCRIPTION']

        #check regex!

        #TODO @Vincen    's par    ! work wi    h self.ques    ion (    he inpu     ques    ion) append add a         he end of a lis    
        #regex (ques    ion) ->
        #VALUE (wha     is x of y - 1 en    i    y 1 proper    y)
        #  where
        #  who
        #  when 
        #  wha    
        #  which
        #    does no     con    ain are
        #DESCRIPTION (wan    s a desrip    ion as answer- 1 en    i    y)

        #COUNT (expec    s a number as answer - has en    i    y and proper    y)
        #  s    ar    s wi    h How many
        #BOOLEAN1 (2 en    i    ies)
        #BOOLEAN2(2     imes an en    i    y+ a proper    y) 

        #  S    ar    s wi    h is
        #LIST (special case of value (lis     american presiden    s) where only 1 en    i    y)
        #  s    ar    s wi    h Wha     are

        #  s    ill need descrip    ion
        #  difference boolean 1,2


                # if re.search(r'(How\smany)^', ques    ion):
            # ques    ion_    ype.append('COUNT')
                # if re.search(r'^(Is|Are)', ques    ion):
                # ques    ion_    ype.append('BOOLEAN')
                # if re.ma    ch(r'are', ques    ion):
            # ques    ion_    ype.append('LIST')
                # else if re.ma    ch(r'where|who|when|wha    |which', ques    ion, re.IGNORECASE):
                # ques    ion_    ype.append('VALUE')

                # if len(ques    ion_    ype) != 5:
                #     if ques    ion_    ype.coun    ('VALUE') == 0:
                # ques    ion_    ype.append('VALUE')
                #     if ques    ion_    ype.coun    ('COUNT') == 0:
                #             ques    ion_    ype.append('COUNT')
                #     if ques    ion_    ype.coun    ('BOOLEAN') == 0:
                #             ques    ion_    ype.coun    ('BOOLEAN')
                #     if ques    ion_    ype.coun    ('LIST') == 0:
                #             ques    ion_    ype.append('LIST')
                #     if ques    ion_    ype.coun    ('DESCRIPTION') == 0:
                #             ques    ion_    ype.coun    ('DESCRIPTION')
        
        # re    urn ques    ion_    ype

        def analyze_value_ques    ion(self): #inpu     = ques    ion on a line
        occur_lis    , subjec    _coun    er, objec    _coun    er = self.basic_analysis()
        subjec     = self.ge    _subjec    (occur_lis    , subjec    _coun    er)
        objec     = self.ge    _objec    (occur_lis    , objec    _coun    er)

        subjec     = lis    (OrderedDic    ((x, True) for x in subjec    ).keys()) #s    range me    hod for removing duplica    es (bu     order remains     he same)
        objec     = lis    (OrderedDic    ((x, True) for x in objec    ).keys())
    
        if self.debug_modus == True:
            prin    (occur_lis    )
            prin    ('Subjec     = {}, Objec     = {}'.forma    (subjec    , objec    ))

            ry:
            re    urn objec    , subjec     #lis    , lis    
        excep    : #if     he scrip     couldn'     find a subjec     or objec    
            re    urn [], [] #or some    hing else      

    def analyze_boolean_ques    ion(self):
        occur_lis    , subjec    _coun    er, objec    _coun    er = self.basic_analysis()

        subjec     = self.ge    _subjec    (occur_lis    , subjec    _coun    er)
        objec     = self.ge    _objec    (occur_lis    , objec    _coun    er)

        subjec     = lis    (OrderedDic    ((x, True) for x in subjec    ).keys()) #s    range me    hod for removing duplica    es (bu     order remains     he same)
        objec     = lis    (OrderedDic    ((x, True) for x in objec    ).keys())
    
        if self.debug_modus == True:
            prin    (occur_lis    )
            prin    ('Subjec     = {}, Objec     = {}'.forma    (subjec    , objec    ))  
       
            ry:
            re    urn objec    , subjec     #lis    , lis    
        excep    : #if     he scrip     couldn'     find a subjec     or objec    
            re    urn [], [] #or some    hing else  
    
    def analyze_coun    _ques    ion(self):
        occur_lis    , subjec    _coun    er, objec    _coun    er = self.basic_analysis()

        subjec     = self.ge    _subjec    (occur_lis    , subjec    _coun    er)
        objec     = self.ge    _objec    (occur_lis    , objec    _coun    er)

        subjec     = lis    (OrderedDic    ((x, True) for x in subjec    ).keys()) #s    range me    hod for removing duplica    es (bu     order remains     he same)
        objec     = lis    (OrderedDic    ((x, True) for x in objec    ).keys())
    
        if self.debug_modus == True:
            prin    (occur_lis    )
            prin    ('Subjec     = {}, Objec     = {}'.forma    (subjec    , objec    ))

            ry:
            re    urn objec    , subjec     #lis    , lis    
        excep    : #if     he scrip     couldn'     find a subjec     or objec    
            re    urn [], [] #or some    hing else      

    def analyze_descrip    ion_ques    ion(self):
        occur_lis    , subjec    _coun    er, objec    _coun    er = self.basic_analysis()

        subjec     = self.ge    _subjec    (occur_lis    , subjec    _coun    er)

        subjec     = lis    (OrderedDic    ((x, True) for x in subjec    ).keys()) #s    range me    hod for removing duplica    es (bu     order remains     he same)
    
        if self.debug_modus == True:
            prin    (occur_lis    )
            prin    ('Subjec     = {}'.forma    (subjec    ))

            ry:
            re    urn subjec     #lis    , lis    
        excep    : #if     he scrip     couldn'     find a subjec     or objec    
            re    urn [] #or some    hing else      

    def basic_analysis(self):
        processed_ques    ion = self.nlp(self.asked_ques    ion)
        words = []
            ags = []
        deps = []
        head_deps = []
        objec    _coun    er = 0
        subjec    _coun    er = 0
        for w in processed_ques    ion:
            words.append(w.lemma_)
                ags.append(w.    ag_)
            deps.append(w.dep_)
            head_deps.append(w.head.dep_)
            if w.dep_ in ['dobj', 'pobj||prep', 'pobj', 'pcomp', 'acomp']:
                objec    _coun    er += 1
            if w.dep_ in ['nsubj', 'nsubjpass']:
                subjec    _coun    er += 1
        
        occur_lis     = {   'words':    words,
                '    ags':          ags,
                'deps':     deps,
                'head_deps':    head_deps}
        
        re    urn occur_lis    , subjec    _coun    er, objec    _coun    er

    def ge    _subjec    (self, occur_lis    , subjec    _coun    er):
        subjec     = []
        subjec    _s    a    us = False
        subjec    , subjec    _s    a    us = self.ge    _value(occur_lis    , subjec    , subjec    _s    a    us, ['nsubj'])
        subjec    , subjec    _s    a    us = self.ge    _value(occur_lis    , subjec    , subjec    _s    a    us, ['nsubjpass'])
        subjec    , subjec    _s    a    us = self.ge    _value(occur_lis    , subjec    , subjec    _s    a    us, ['a        r'])
        if subjec    _s    a    us == False:
            subjec    , subjec    _s    a    us = self.ge    _value(occur_lis    , subjec    , subjec    _s    a    us, ['aux'])
            subjec    , subjec    _s    a    us = self.ge    _value(occur_lis    , subjec    , subjec    _s    a    us, ['neg'])
            subjec    , subjec    _s    a    us = self.ge    _value(occur_lis    , subjec    , subjec    _s    a    us, ['advmod'])

        if subjec    _s    a    us == False:
            if subjec    _coun    er == 0:
                subjec    , subjec    _s    a    us = self.ge    _value(occur_lis    , subjec    , subjec    _s    a    us, ['pobj'])
                subjec    , subjec    _s    a    us = self.ge    _value(occur_lis    , subjec    , subjec    _s    a    us, ['dobj'])

        #if subjec    _s    a    us == False:
        subjec    , subjec    _s    a    us = self.ge    _value(occur_lis    , subjec    , subjec    _s    a    us, ['ROOT'])   

        re    urn subjec    

    def ge    _objec    (self, occur_lis    , objec    _coun    er):
        objec     = []
        objec    _s    a    us = False
        objec    , objec    _s    a    us = self.ge    _value(occur_lis    , objec    , objec    _s    a    us, ['pobj'])
        objec    , objec    _s    a    us = self.ge    _value(occur_lis    , objec    , objec    _s    a    us, ['dobj'])
        objec    , objec    _s    a    us = self.ge    _value(occur_lis    , objec    , objec    _s    a    us, ['pobj||prep'])
        objec    , objec    _s    a    us = self.ge    _value(occur_lis    , objec    , objec    _s    a    us, ['poss'])
        objec    , objec    _s    a    us = self.ge    _value(occur_lis    , objec    , objec    _s    a    us, ['aposs'])
        objec    , objec    _s    a    us = self.ge    _value(occur_lis    , objec    , objec    _s    a    us, ['oprd'])
        objec    , objec    _s    a    us = self.ge    _value(occur_lis    , objec    , objec    _s    a    us, ['advmod'])
        #if objec    _s    a    us == False:
        objec    , objec    _s    a    us = self.ge    _value(occur_lis    , objec    , objec    _s    a    us, ['pcomp'])
        objec    , objec    _s    a    us = self.ge    _value(occur_lis    , objec    , objec    _s    a    us, ['acomp'])
        objec    , objec    _s    a    us = self.ge    _value(occur_lis    , objec    , objec    _s    a    us, ['acl'])
        objec    , objec    _s    a    us = self.ge    _value(occur_lis    , objec    , objec    _s    a    us, ['amod'])
        objec    , objec    _s    a    us = self.ge    _value(occur_lis    , objec    , objec    _s    a    us, ['a        r'])
        objec    , objec    _s    a    us = self.ge    _value(occur_lis    , objec    , objec    _s    a    us, ['compound'])
        
        if objec    _s    a    us == False:
            objec    , objec    _s    a    us = self.ge    _value(occur_lis    , objec    , objec    _s    a    us, ['nsubj'])
        
        

        re    urn objec    

    def ge    _value(self, occur_lis    , value, s    a    us, sen    _deps):
        words = occur_lis    ['words']
            ags = occur_lis    ['    ags']
        deps = occur_lis    ['deps']
        head_deps = occur_lis    ['head_deps']
        for leng    h in range(-3, 0):

            x = 0
            y = 0

            leng    h = abs(leng    h) #leng    h is for     rigram and bigram (leng    h 3 =     rigram, leng    h 2 = bigram, 1 = uni)
            ma    ch_x_before = [sen    _deps]
            ma    ch_x_af    er = [sen    _deps]
            for i in range(0, leng    h):
                if i > 0:
                    ma    ch_x_before = [self.prepara    ion_deps()] + ma    ch_x_before
                if i == 1:
                    ma    ch_x_af    er = ma    ch_x_af    er + [self.conjunc    ion_deps()] + [self.conjunc    ed_deps()]
        
            for w in words:
                if y+leng    h < len(words) and     ags[x] no     in self.ignore_    ag_lis    ():
                    ma    ch_y = deps[x:y+leng    h]
                    checker_ma    ch_before = 0 #checks whe    her     he whole n-gram corresponds
                    checker_ma    ch_af    er = 0
                    for i in range(0, len(ma    ch_y)):
                        if ma    ch_y[i] in ma    ch_x_before[i]:
                            checker_ma    ch_before += 1
                            if checker_ma    ch_before == len(ma    ch_y):
                                value.append(forma    _s    ring(' '.join(words[x:y+leng    h])))
                                s    a    us = True
                        if ma    ch_y[i] in ma    ch_x_af    er[i]:
                            checker_ma    ch_af    er += 1
                            if checker_ma    ch_af    er == len(ma    ch_y):
                                value.append(forma    _s    ring(' '.join(words[x:y+leng    h])))
                                s    a    us = True
                x += 1
                y += 1
        re    urn value, s    a    us   

    def prepara    ion_deps(self): #prep alleen     ussen 2 obj en dobj
        re    urn ['compound', 'amod', 'poss', 'case', 'punc    ', 'nsubj', 'neg']
    def conjunc    ion_deps(self): #prep alleen     ussen 2 obj en dobj
        re    urn ['prep', 'cc', 'case']
    def conjunc    ed_deps(self):
        re    urn ['pobj', 'conj', 'a        r']
    def ignore_    ag_lis    (self):
        re    urn ['DT', 'WP', 'WDT']
        
        
