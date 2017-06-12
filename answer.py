import sparql
import wikidata
import base
from question import QuestionType
import logging
import itertools
import wikipedia

class Answer:

    def __init__(self, question, count, nlp, anchor_texts):
        self.question = question
        self.count = count
        self.anchor_texts = anchor_texts

        self.obj_entity_IDs = [] # IDs of objects in question interpreted as entities
        self.subj_property_IDs = [] # IDs of subjects in question interpreted as properties
        self.subj_entity_IDs = [] # etc.
        self.obj_property_IDs = [] # keeps track of which IDs have been found with which words
        self.IDsWithWords = {}
        self.prepared_IDs = False

        self.answers = []

    def print_it(self):
        if not self.answers:
            self._find_answer()
		
        print(self.count.use(), "\t", end='')
        print("\t".join(self.answers))

    def _find_answer(self):
        if not self.prepared_IDs:
            self._prepare_IDs()

        for question_type in self.question.types:
            logging.debug("question_type = {}".format(question_type))
            self.answer_as(question_type)
            if self.answers:
                return
    
    def getExtraEntityIDs(self,entities):
        entity_IDs = []
        for entity in entities:
            query(sparql.AliasQuery(entity))
            entity_IDs.extend(query.get())
        print(entity_IDs)


    def _prepare_IDs(self):
        for obj in self.question.objects:
            #getExtraEntityIDs(obj)
            wikipages = self.anchor_texts.get_URLs(obj)
            self.obj_entity_IDs.extend(wikidata.get_entity_IDs_by_URL(wikipages))
        for obj in self.question.objects:
            new_entity_IDs = wikidata.get_entity_IDs(obj)
            new_property_IDs = wikidata.get_property_IDs(obj)
            self.obj_entity_IDs.extend(new_entity_IDs)
            
            print(self.obj_entity_IDs)
            self.obj_property_IDs.extend(new_property_IDs)
            self.IDsWithWords.update({el: str(obj) for el in new_entity_IDs + new_property_IDs})
        for subj in self.question.subjects:
            new_entity_IDs = wikidata.get_entity_IDs(subj)
            new_property_IDs = wikidata.get_property_IDs(subj)
            self.subj_entity_IDs.extend(new_entity_IDs)
            self.subj_property_IDs.extend(new_property_IDs)
            self.IDsWithWords.update({el: str(subj) for el in new_entity_IDs + new_property_IDs})

        self.obj_entity_IDs = base.dedup(self.obj_entity_IDs)
        self.subj_property_IDs = base.dedup(self.subj_property_IDs)
        self.subj_entity_IDs = base.dedup(self.subj_entity_IDs)
        self.obj_property_IDs = base.dedup(self.obj_property_IDs)
        self.prepared_IDs = True

        logging.debug("self.obj_entity_IDs = {}".format(self.obj_entity_IDs))
        logging.debug("self.subj_property_IDs = {}".format(self.subj_property_IDs))
        logging.debug("self.subj_entity_IDs = {}".format(self.subj_entity_IDs))
        logging.debug("self.obj_property_IDs = {}".format(self.obj_property_IDs))
        logging.debug("self.IDsWithWords = {}".format(self.IDsWithWords))
   
    def id_got_with_same_word(self, first_id, second_id):
        return self.IDsWithWords[first_id] in self.IDsWithWords[second_id] or self.IDsWithWords[second_id] in self.IDsWithWords[first_id]

    def got_with_ignored_entity(self, entity_id):
        return self.IDsWithWords[entity_id] in ['origin']

    def get_answer(self, entities_and_properties, queryConstructor):
        for entity_id, property_id in entities_and_properties:
            # check if both ids are retrieved with the same word or with ignored entity, if so
            # we don't want to check this combination
            if self.id_got_with_same_word(entity_id, property_id) or self.got_with_ignored_entity(entity_id):
                continue
            query = queryConstructor(entity_id, property_id)
            answer = query.get()
            if answer:
                self.answers = answer
                return
                
    def get_answer_boolean(self, entities_and_properties_and_entities, queryConstructor):
        for entity_id, property_id, entity_id2 in entities_and_properties_and_entities:
            # check if both ids are retrieved with the same word or with ignored entity, if so
            # we don't want to check this combination
            if self.id_got_with_same_word(entity_id, property_id) or self.id_got_with_same_word(entity_id2, property_id) or self.id_got_with_same_word(entity_id2, entity_id) or self.got_with_ignored_entity(entity_id) or  self.got_with_ignored_entity(entity_id2):
                continue
            query = queryConstructor(entity_id, property_id, entity_id2)
            #print(entity_id) 
            #print(property_id) 
            #print(entity_id2)
            answer = query.get()
            #print(answer)
            if answer[0]:
                self.answers = ["Yes."]
                return
        self.answers=["No."]
        return
        
    def answer_as(self, question_type):
        all_combinations = base.dedup(itertools.chain(itertools.product(self.obj_entity_IDs, self.subj_property_IDs),
                itertools.product(self.obj_entity_IDs + self.subj_entity_IDs,
                        self.subj_property_IDs+ self.obj_property_IDs)))
        all_combinations_doubleEntity = base.dedup(itertools.chain(itertools.product(self.obj_entity_IDs, self.subj_property_IDs,self.obj_entity_IDs),itertools.product(self.obj_entity_IDs + self.subj_entity_IDs,
                        self.subj_property_IDs+ self.obj_property_IDs,self.obj_entity_IDs + self.subj_entity_IDs)))
        if question_type == QuestionType.VALUE:
            self.get_answer(all_combinations, sparql.ValueQuery)
        elif question_type == QuestionType.DESCRIPTION:
            for entity_id in self.subj_entity_IDs + self.obj_entity_IDs:
                query = sparql.DescriptionQuery(entity_id)
                answer = query.get()
                if answer:
                    self.answers = answer
                    return
        elif question_type == QuestionType.COUNT:
            self.get_answer(all_combinations, sparql.CountQuery)
        elif question_type == QuestionType.BOOLEAN:
            if (self.subj_property_IDs + self.subj_property_IDs+ self.obj_property_IDs):
                self.get_answer_boolean(all_combinations_doubleEntity, sparql.AskSpecificQuery)
            else:
                for entity_id in self.subj_entity_IDs + self.obj_entity_IDs:
                    for entity_id2 in self.subj_entity_IDs + self.obj_entity_IDs:
                        query = sparql.AskQuery(entity_id, entity_id2)
                        answer = query.get()
                        if answer[0]:
                            self.answers = ["Yes."]
                            return
                    self.answers=["No."]
                    return
        elif question_type == QuestionType.LIST:
            
            for entity_id in self.subj_entity_IDs + self.obj_entity_IDs:
                query = sparql.ListQuery(entity_id)
                answer = query.get()
                if answer:
                    self.answers = answer
                    return
        else:
            raise NotImplementedError
