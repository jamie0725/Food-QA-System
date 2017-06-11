import sparql
import wikidata
import base
from question import QuestionType
import logging

class Answer:

    def __init__(self, question, count, nlp):
        self.question = question
        self.count = count

        self.obj_entity_IDs = []
        self.subj_property_IDs = []
        self.subj_entity_IDs = []
        self.obj_property_IDs = []

        self.answers = []

    def print_it(self):
        if not self.answers:
            self._find_answer()
        print(self.count.use(), "\t", end='')
        print("\t".join(self.answers))

    def _find_answer(self):
        if not self.entity_IDs or not self.property_IDs:
            self._prepare_IDs()

        for question_type in self.question.types:
            self.answer_as(question_type)
            if self.answers:
                return

    def _prepare_IDs(self):
        for obj in self.question.objects:
            self.obj_entity_IDs.extend(wikidata.get_entity_IDs(obj))
            self.obj_property_IDs.extend(wikidata.get_property_IDs(obj))
        for subj in self.question.subjects:
            self.subj_entity_IDs.extend(wikidata.get_entity_IDs(subj))
            self.subj_property_IDs.extend(wikidata.get_property_IDs(subj))

        self.obj_entity_IDs = base.dedup(self.obj_entity_IDs)
        self.subj_property_IDs = base.dedup(self.subj_property_IDs)
        self.subj_entity_IDs = base.dedup(self.subj_entity_IDs)
        self.obj_property_IDs = base.dedup(self.obj_property_IDs)

        logging.debug("self.obj_entity_IDs = {}".format(self.obj_entity_IDs))
        logging.debug("self.subj_property_IDs = {}".format(self.subj_property_IDs))
        logging.debug("self.subj_entity_IDs = {}".format(self.subj_entity_IDs))
        logging.debug("self.obj_property_IDs = {}".format(self.obj_property_IDs))


    def answer_as(self, question_type):
        if question_type == QuestionType.VALUE:
            for entity_id, property_id in zip(self.obj_entity_IDs, self.subj_property_IDs):
                query = sparql.ValueQuery(entity_id, property_id)
                answer = query.get()
                if answer:
                    self.answers.extend(answer)
                    return
        elif question_type == QuestionType.DESCRIPTION:
            for entity_id in self.subj_entity_IDs self.obj_entity_IDs:
                query = sparql.DescriptionQuery(entity_id)
                answer = query.get()
                if answer:
                    self.answers.extend(answer)
                    return
        else:
            raise NotImplementedError
