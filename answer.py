import sparql
import wikidata
import base
from question import QuestionType

class Answer:
    def __init__(self, question, count, nlp):
        self.question = question
        self.count = count

        self.entity_IDs = []
        self.property_IDs = []

        self.answers = []

    def print(self):
        if (not self.answer):
            self._find_answer()
        print(self.count.use(), "\t", end='')
        print("\t".join(self.answers))

    def _find_answer(self):
        if (not self.entity_IDs or not self.property_IDs):
            self._prepare_IDs()

        for question_type in question.types:
            self.answer_as(question_type)
            if answer:
                return

    def _prepare_IDs(self):
        for entity_name in question.subjects:
            self.entity_IDs.extend(wikidata.get_entity_IDs(entity_name))
        for property_name in question.objects:
            self.property_IDs.extend(wikidata.get_property_IDs(property_name))

        base.dedup(self.entity_IDs)
        base.dedup(self.property_IDs)

    def answer_as(self, question_type):
        if question_type == QuestionType.VALUE:
            for entity_id, property_id in zip(self.entity_IDs, self.property_IDs):
                query = sparql.ValueQuery(entity_id, property_id)
                answer = query.get()

        else
            raise NotImplementedError 
            

