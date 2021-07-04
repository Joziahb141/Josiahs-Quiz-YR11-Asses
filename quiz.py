import requests
from html import unescape
import random

# gets 10 multichoice any difficulty vehicle questions and the possible answers plus more from open trivia DB using requests.get and stores it all using the variable data
response = requests.get("https://opentdb.com/api.php?amount=10&category=28&type=multiple")
data = response.json()['results']

# creating an empty array for questions, correct answers and incorrect answers
questions = []
right_answers = []
wrong_answers = []

# gets the info of data and sorts the questions, correct answer and incorrect answer from into into the empty arrays above
for i,question in enumerate(data):
  questions.append(unescape(question["question"]))
  right_answers.append(question["correct_answer"])
  for i,wrong in enumerate(question["incorrect_answers"]):
    wrong_answers.append(wrong)

# for loop that runs for the amount of questions and prints out the questions and answers to them
for i in range (len(questions)):
  # generates the number tkhat will be the correct awnser
  correct_ans_number = random.randint(1,4)
  print(questions[i])
  if correct_ans_number == 1:
    print(f"1. {right_answers[i]}\n2. {wrong_answers[(i+1)*3-3]}\n3. {wrong_answers[(i+1)*3-2]}\n4. {wrong_answers[(i+1)*3-1]}")
    # prints all the answers for the question with one being the correct one
  elif correct_ans_number == 2:
    print(f"1. {wrong_answers[(i+1)*3-3]}\n2. {right_answers[i]}\n3. {wrong_answers[(i+1)*3-2]}\n4. {wrong_answers[(i+1)*3-1]}")
    # prints all the answers for the question with two being the correct one
  elif correct_ans_number == 3:
    print(f"1. {wrong_answers[(i+1)*3-3]}\n2. {wrong_answers[(i+1)*3-2]}\n3. {right_answers[i]}\n4. {wrong_answers[(i+1)*3-1]}")
    # prints all the answers for the question with three being the correct one  
  else:
    print(f"1. {wrong_answers[(i+1)*3-3]}\n2. {wrong_answers[(i+1)*3-2]}\n3. {wrong_answers[(i+1)*3-1]}\n4. {right_answers[i]}")
    # prints all the anwsers for the question with four being the correct one
    
