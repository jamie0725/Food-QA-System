import sparql

class Answer:
    def __init__(self, question, count, nlp):
        self.question = question
        self.count = count

        self.answers = []

    def formulate_answer(self, entity, property): 
        # base case, calling to get_answer of this class should be done with self.get_answer()
        answer, status = self.get_answer(entity, property) # return is something like answer (string) and status (boolean).

        if status == False: # f.e. swap entity and property, try something with synonyms (with WordNet or so), etcetera
            answer, status = self.get_answer(property, entity) 
    
        # if status == False: # and go on if there is no answer found...

        
        # if no answer is found at all
        if status == False:
            print("no answer found for Question: {}. ".format(self.asked_question))
        else:
            print_question(self.asked_question)
            print_answer(answer)
            
    # TODO expand the function to get the right answer(s)
    def get_answer(self, entity, property):
        status = False
        '''
        To make this function efficient, we should first try to find the property.
        If no property is found, we can skip this whole process and return to formulate_answer()
        '''
        property_IDs = self.wikidataAPI.get_property_IDs(property) # return is a list of properties
        if self.debug_modus == True:
            print('property_IDs = {}'.format(property_IDs))

        if len(property_IDs) == 0: # if no property is found: just stop!
            return '', status # answer empty string, status is False

        # continue with finding the entity
        # I think wikidataAPI is more accurate, but if you think it should be the other way around, just swap them
        
        entity_IDs =  self.wikidataAPI.get_entity_IDs(entity)
        if self.debug_modus == True:
            print('wikidataAPI - entity_IDs = {}'.format(entity_IDs))
        if len(entity_IDs) > 0: # try to find an answer with wikidataAPI IDs
            answer, status = self.wikidataAPI.get_answer(entity_IDs, property_IDs)
            if self.debug_modus == True:
                print('wikidataAPI - answer = {}'.format(answer))


    def print(self):
        if (not self.answer):
            self.formulate_answer()
        print(self.count, "\t", end='')
        print("\t".join(self.answers))
