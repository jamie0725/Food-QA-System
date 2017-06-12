import sparql
import wikidata
import base
from question import QuestionType
import logging
import itertools

class Answer:

    def __init__(self, question, count, nlp):
        self.question = question
        self.count = count

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

    def print_it_explicit(self):
        if not self.answers:
            self._find_answer()
		
        print(self.count.use(), "\t", end='')
        print(self.question.question, "\t", end='')
        print("\t".join(self.answers))

    def _find_answer(self):
        if not self.prepared_IDs:
            self._prepare_IDs()

        for question_type in self.question.types:
            logging.debug("question_type = {}".format(question_type))
            self.answer_as(question_type)
            if self.answers:
                return

    def _prepare_IDs(self):
        for obj in self.question.objects:
            new_entity_IDs = wikidata.get_entity_IDs(obj)
            new_property_IDs = wikidata.get_property_IDs(obj)
            self.obj_entity_IDs.extend(new_entity_IDs)
            self.obj_property_IDs.extend(new_property_IDs)
            self.IDsWithWords.update({el: str(obj) for el in new_entity_IDs + new_property_IDs})
        for subj in self.question.subjects:
            new_entity_IDs = wikidata.get_entity_IDs(subj)
            new_property_IDs = wikidata.get_property_IDs(subj)
            self.subj_entity_IDs.extend(new_entity_IDs)
            self.subj_property_IDs.extend(new_property_IDs)
            self.IDsWithWords.update({el: str(subj) for el in new_entity_IDs + new_property_IDs})
            print(subj)

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


    def answer_as(self, question_type):
        if question_type == QuestionType.VALUE:
            for entity_id, property_id in itertools.product(self.obj_entity_IDs, self.subj_property_IDs):
                query = sparql.ValueQuery(entity_id, property_id)
                answer = query.get()
                if answer:
                    self.answers = answer
                    return
            for entity_id, property_id in itertools.product(self.subj_entity_IDs, self.obj_property_IDs):
                query = sparql.ValueQuery(entity_id, property_id)
                answer = query.get()
                if answer:
                    self.answers = answer
                    return
        elif question_type == QuestionType.DESCRIPTION:
            for entity_id in itertools.product(self.subj_entity_IDs):
                query = sparql.DescriptionQuery(entity_id)
                answer = query.get()
                if answer:
                    self.answers = answer
                    return
            for entity_id in itertools.product(self.obj_entity_IDs):
                query = sparql.DescriptionQuery(entity_id)
                answer = query.get()
                if answer:
                    self.answers = answer
                    return
        elif question_type == QuestionType.COUNT:
            for entity_id, property_id in itertools.product(self.obj_entity_IDs, self.subj_property_IDs):
                query = sparql.CountQuery(entity_id, property_id)
                answer = query.get()
                if answer: # if the answer is 0, it's probably also incorrect
                    self.answes = answer
                    return
            for entity_id, property_id in itertools.product(self.subj_entity_IDs, self.obj_property_IDs):
                query = sparql.CountQuery(entity_id, property_id)
                answer = query.get()
                if answer: # if the answer is 0, it's probably also incorrect
                    self.answes = answer
                    return
        else:
            raise NotImplementedError
