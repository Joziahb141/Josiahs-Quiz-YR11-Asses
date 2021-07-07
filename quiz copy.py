import requests
from html import unescape
import random

# a function to get a int imput from user between 2 numbers - needs a message and error message lowest int value and highest int value
def get_int_input(message, error, low, high):
  while True:
    try:
      inpt = int(input(message))
      if low < inpt < high or low == inpt or high == inpt:
        return inpt
      else:
        print(error)
    except ValueError:
      print(error)
      
# gets 10 multichoice any difficulty vehicle questions and the possible answers plus more from open trivia DB using requests.get and stores it all using the variable data
response = requests.get("https://opentdb.com/api.php?amount=10&category=28&type=multiple")
data = response.json()['results']

# creating an empty array for questions, correct answers and incorrect answers
questions = []
right_answers = []
wrong_answers = []
all_answers = []

# gets the info of data and sorts the questions, correct answer and incorrect answer from into into the empty arrays above
for i,question in enumerate(data):
  questions.append(unescape(question["question"]))
  right_answers.append(question["correct_answer"])
  for j,wrong in enumerate(question["incorrect_answers"]):
    wrong_answers.append(wrong)

# for loop that runs for the amount of questions and prints out the questions and answers to them

for i,question in enumerate(question):
  print(unescape(question["question"]))
  all_answers = []
  all_answers.append(question["correct_answer"])
  for ans in enumerate(question["incorrect_answers"]):\
    all_answers.append(ans)
  random.shuffle(all_answers)
  for num, ans in enumerate(all_answers):
    print(f"{num+1}: {ans}")



  

    
