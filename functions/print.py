#!/usr/bin/env python3

def example_questions():
	#QUESTIONS
	print('EXAMPLE QUESTIONS')
	questions = [	'What is the country of origin of cookies?' ,
			'What are the ingredients of a gin and tonic?',
			'When was the inception of Dr Pepper?',
			'Who is the founder of the KFC?',
			'In what industry is the KFC?',
			'In which year was Coca Cola created?',
			'What are the ingredients of Roquefort cheese?',
			'What product does McDonalds sell?' ,
			'Which colors does an apple have?',	
			"Where is the headquarters of Tony's Chocolonely?"
			]

	for question in questions:
		print(question)

def ask_new_question():
	print('-'*50)
	print('What is your question?')

def question(question):
	print("Question: {} ".format(question))

def answer(answers):
	#for disambiguity 
	if len(answers) > 1:
		i = 0
		for answer in answers:
			i += 1 #TODO for disambiguity we could use something like this
			print("({}) Answer: if entity is {}: {}. ".format(i, answer, ', '.join(answers[answer])))
	else:
		for answer in answers:
			print("Answer: {}. ".format(', '.join(answers[answer])))
