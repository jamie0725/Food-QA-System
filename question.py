import spacy
from enum import Enum
import logging
import base

QuestionType = Enum('QuestionType', 'VALUE COUNT BOOLEAN DESCRIPTION LIST')

class Question:
    def __init__(self, question, nlp):
        self.question = question
        self.nlp = nlp
        self.subjects = []
        self.objects = []
        self.types = [] # which question types this question should be interpreted as
                        # ordered by likelihood of being the correct interpretation

        self.determine_question_type()
        self.determine_components()

        logging.info("Made Question: {}".format(question))
        logging.info("subjects: {}".format(self.subjects))
        logging.info("objects: {}".format(self.objects))

    def determine_question_type(self):
        self.types = [QuestionType.VALUE, QuestionType.DESCRIPTION]

    def determine_components(self):
        occur_list, subject_counter, object_counter = self.basic_analysis()
        subjects = self.get_subject(occur_list, subject_counter)
        objects = self.get_object(occur_list, object_counter)

        self.objects = base.dedup(objects)
        self.subjects = base.dedup(subjects)

        logging.info('determine_components, subjects = {}\nobjects = {}'.format(subjects, objects))
        words_to_remove = ["be"]
        self.objects = base.remove_elements(self.objects, words_to_remove)
        self.subjects = base.remove_elements(self.objects, words_to_remove)

        logging.info("occur_list: {}".format(occur_list))
        logging.info('determine_components, subjects = {}\nobjects = {}'.format(subjects, objects))
        

    def basic_analysis(self):
        processed_question = self.nlp(self.question)
        words = []
        tags = []
        deps = []
        head_deps = []
        object_counter = 0
        subject_counter = 0
        for w in processed_question:
            words.append(w.lemma_)
            tags.append(w.tag_)
            deps.append(w.dep_)
            head_deps.append(w.head.dep_)
            if w.dep_ in ['dobj', 'pobj||prep', 'pobj', 'pcomp', 'acomp']:
                object_counter += 1
            if w.dep_ in ['nsubj', 'nsubjpass']:
                subject_counter += 1

        occur_list = {'words':      words,
                      'tags':       tags,
                      'deps':       deps,
                      'head_deps':  head_deps}

        return occur_list, subject_counter, object_counter

    def get_subject(self, occur_list, subject_counter):
        subjects = []
        subject_status = False
        subjects, subject_status = self.get_value(
            occur_list, subjects, subject_status, ['nsubj'])
        subjects, subject_status = self.get_value(
            occur_list, subjects, subject_status, ['nsubjpass'])
        subjects, subject_status = self.get_value(
            occur_list, subjects, subject_status, ['attr'])
        if subject_status == False:
            subjects, subject_status = self.get_value(
                occur_list, subjects, subject_status, ['aux'])
            subjects, subject_status = self.get_value(
                occur_list, subjects, subject_status, ['neg'])
            subjects, subject_status = self.get_value(
                occur_list, subjects, subject_status, ['advmod'])

        if subject_status == False:
            if subject_counter == 0:
                subjects, subject_status = self.get_value(
                    occur_list, subjects, subject_status, ['pobj'])
                subjects, subject_status = self.get_value(
                    occur_list, subjects, subject_status, ['dobj'])

        # if subject_status == False:
        subjects, subject_status = self.get_value(
            occur_list, subjects, subject_status, ['ROOT'])

        return subjects

    def get_object(self, occur_list, object_counter):
        objects = []
        object_status = False
        objects, object_status = self.get_value(
            occur_list, objects, object_status, ['pobj'])
        objects, object_status = self.get_value(
            occur_list, objects, object_status, ['dobj'])
        objects, object_status = self.get_value(
            occur_list, objects, object_status, ['pobj||prep'])
        objects, object_status = self.get_value(
            occur_list, objects, object_status, ['poss'])
        objects, object_status = self.get_value(
            occur_list, objects, object_status, ['aposs'])
        objects, object_status = self.get_value(
            occur_list, objects, object_status, ['oprd'])
        objects, object_status = self.get_value(
            occur_list, objects, object_status, ['advmod'])
        # if object_status == False:
        objects, object_status = self.get_value(
            occur_list, objects, object_status, ['pcomp'])
        objects, object_status = self.get_value(
            occur_list, objects, object_status, ['acomp'])
        objects, object_status = self.get_value(
            occur_list, objects, object_status, ['acl'])
        objects, object_status = self.get_value(
            occur_list, objects, object_status, ['amod'])
        objects, object_status = self.get_value(
            occur_list, objects, object_status, ['attr'])
        objects, object_status = self.get_value(
            occur_list, objects, object_status, ['compound'])

        if object_status == False:
            objects, object_status = self.get_value(
                occur_list, objects, object_status, ['nsubj'])

        return objects

    def get_value(self, occur_list, value, status, sent_deps):
        words = occur_list['words']
        tags = occur_list['tags']
        deps = occur_list['deps']
        head_deps = occur_list['head_deps']
        for length in range(-3, 0):

            x = 0
            y = 0

            # length is for trigram and bigram (length 3 = trigram, length 2 =
            # bigram, 1 = uni)
            length = abs(length)
            match_x_before = [sent_deps]
            match_x_after = [sent_deps]
            for i in range(0, length):
                if i > 0:
                    match_x_before = [self.preparation_deps()] + match_x_before
                if i == 1:
                    match_x_after = match_x_after + \
                        [self.conjunction_deps()] + [self.conjuncted_deps()]

            for w in words:
                if y+length < len(words) and tags[x] not in self.ignore_tag_list():
                    match_y = deps[x:y+length]
                    checker_match_before = 0  # checks whether the whole n-gram corresponds
                    checker_match_after = 0
                    for i in range(0, len(match_y)):
                        if match_y[i] in match_x_before[i]:
                            checker_match_before += 1
                            if checker_match_before == len(match_y):
                                value.append(base.format_string(
                                    ' '.join(words[x:y+length])))
                                status = True
                        if match_y[i] in match_x_after[i]:
                            checker_match_after += 1
                            if checker_match_after == len(match_y):
                                value.append(base.format_string(
                                    ' '.join(words[x:y+length])))
                                status = True
                x += 1
                y += 1
        return value, status

    def preparation_deps(self):  # prep alleen tussen 2 obj en dobj
        return ['compound', 'amod', 'poss', 'case', 'punct', 'nsubj', 'neg']

    def conjunction_deps(self):  # prep alleen tussen 2 obj en dobj
        return ['prep', 'cc', 'case']

    def conjuncted_deps(self):
        return ['pobj', 'conj', 'attr']

    def ignore_tag_list(self):
        return ['DT', 'WP', 'WDT']
