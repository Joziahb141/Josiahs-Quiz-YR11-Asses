import requests
from html import unescape

#gets 10 multichoice any difficulty vehicle questions and the possible answers plus more from open trivia DB using requests.get and stores it all using the variable data
response = requests.get("https://opentdb.com/api.php?amount=10&category=28&type=multiple")
data = response.json()['results']

#creating an empty array for questions, correct answers and incorrect answers
questions = []
right_answers = []
wrong_answers = []

#gets the info of data and sorts the questions, correct answer and incorrect answer from into into the empty arrays above
for i,question in enumerate(data):
  questions.append(unescape(question["question"]))
  right_answers.append(question["correct_answer"])
  for i,wrong in enumerate(question["incorrect_answers"]):
    wrong_answers.append(wrong)
