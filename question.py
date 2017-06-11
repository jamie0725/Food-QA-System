import spacy
from enum import Enum

QuestionType = Enum('QuestionType', 'VALUE', 'COUNT',
                   'BOOLEAN', 'DESCRIPTION', 'LIST')

# ALL OTHERS: analyze_value_question()  = self.subject, self.object
# DESCRIPTION: analyze_description_question() #self.subject


class Question:
    def __init__(self, question, nlp):
        self.question = question
        self.nlp = nlp
        self.subjects = []
        self.objects = []
        self.types = []

    def determine_question_type(self):
        self.types = [t for t in QuestionType]

    def determine_components(self):
        if QuestionType.VALUE in self.types:
            self.analyze_value_question()
        if QuestionType.BOOLEAN in self.types:
            self.analyze_boolean_question()
        if QuestionType.COUNT in self.types:
            self.analyze_count_question()
        if QuestionType.DESCRIPTION in self.types:
            self.analyze_description_question()

    def analyze_value_question(self):
        occur_list, subject_counter, object_counter = self.basic_analysis()
        subject = self.get_subject(occur_list, subject_counter)
        object = self.get_object(occur_list, object_counter)

        # strange method for removing duplicates (but order remains the same)
        subject = list(OrderedDict((x, True) for x in subject).keys())
        object = list(OrderedDict((x, True) for x in object).keys())

        if self.debug_modus == True:
            print(occur_list)
            print('Subject = {}, Object = {}'.format(subject, object))

        try:
            self.object = object
            self.subject = subject  # list, list
        except:  # if the script couldn't find a subject or object
            self.object = []
            self.subject = []

    def analyze_description_question(self):
        occur_list, subject_counter, object_counter = self.basic_analysis()

        subject = self.get_subject(occur_list, subject_counter)

        # strange method for removing duplicates (but order remains the same)
        subject = list(OrderedDict((x, True) for x in subject).keys())

        if self.debug_modus == True:
            print(occur_list)
            print('Subject = {}'.format(subject))

        try:
            self.subject = subject  # list, list
        except:  # if the script couldn't find a subject or object
            self.subject = []

    def basic_analysis(self):
        processed_question = self.nlp(self.asked_question)
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
        subject = []
        subject_status = False
        subject, subject_status = self.get_value(
            occur_list, subject, subject_status, ['nsubj'])
        subject, subject_status = self.get_value(
            occur_list, subject, subject_status, ['nsubjpass'])
        subject, subject_status = self.get_value(
            occur_list, subject, subject_status, ['attr'])
        if subject_status == False:
            subject, subject_status = self.get_value(
                occur_list, subject, subject_status, ['aux'])
            subject, subject_status = self.get_value(
                occur_list, subject, subject_status, ['neg'])
            subject, subject_status = self.get_value(
                occur_list, subject, subject_status, ['advmod'])

        if subject_status == False:
            if subject_counter == 0:
                subject, subject_status = self.get_value(
                    occur_list, subject, subject_status, ['pobj'])
                subject, subject_status = self.get_value(
                    occur_list, subject, subject_status, ['dobj'])

        # if subject_status == False:
        subject, subject_status = self.get_value(
            occur_list, subject, subject_status, ['ROOT'])

        return subject

    def get_object(self, occur_list, object_counter):
        object = []
        object_status = False
        object, object_status = self.get_value(
            occur_list, object, object_status, ['pobj'])
        object, object_status = self.get_value(
            occur_list, object, object_status, ['dobj'])
        object, object_status = self.get_value(
            occur_list, object, object_status, ['pobj||prep'])
        object, object_status = self.get_value(
            occur_list, object, object_status, ['poss'])
        object, object_status = self.get_value(
            occur_list, object, object_status, ['aposs'])
        object, object_status = self.get_value(
            occur_list, object, object_status, ['oprd'])
        object, object_status = self.get_value(
            occur_list, object, object_status, ['advmod'])
        # if object_status == False:
        object, object_status = self.get_value(
            occur_list, object, object_status, ['pcomp'])
        object, object_status = self.get_value(
            occur_list, object, object_status, ['acomp'])
        object, object_status = self.get_value(
            occur_list, object, object_status, ['acl'])
        object, object_status = self.get_value(
            occur_list, object, object_status, ['amod'])
        object, object_status = self.get_value(
            occur_list, object, object_status, ['attr'])
        object, object_status = self.get_value(
            occur_list, object, object_status, ['compound'])

        if object_status == False:
            object, object_status = self.get_value(
                occur_list, object, object_status, ['nsubj'])

        return object

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
                                value.append(format_string(
                                    ' '.join(words[x:y+length])))
                                status = True
                        if match_y[i] in match_x_after[i]:
                            checker_match_after += 1
                            if checker_match_after == len(match_y):
                                value.append(format_string(
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
