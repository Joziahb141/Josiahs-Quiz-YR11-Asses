
import requests
from html import unescape
import random

def login(username, password):
  file = open("user.txt", "r")
  for i in file:
    Username,Password = i.split(",")
    Password = Password.strip()

    if Username == username and Password == password:
      print (f"********************************************************************************\n********************************************************************************\n*************** WELCOME {username.upper()} TO THE VEHCLE QUIZ ***************** \n********************************************************************************\n*********************************************************************************")
      break

    else:
      print("your password or username is not recognised please try again or create a new account")
      new_username = input ("enter your username\n")
      new_password = input ("enter your password\n")
      login(new_username,new_password)
  file.close()

def register(username, password):
  file = open("user.txt", "r")
  valid = True
  for i in file:
    Username = i.split(",")
    if Username[0] == username:
      valid = False  
      break
    
  if valid == True:
    file = open("user.txt", "a")
    file.write(f"\n{username},{password}")
    print(f"********************************************************************************\n********************************************************************************\n*************** WELCOME {username.upper()} TO THE VEHCLE QUIZ ***************** \n********************************************************************************\n*********************************************************************************")
    file.close()
  else:
    print("someone else already has that username please make another one")
    new_username = input ("enter your changed username\n")
    new_password = input ("enter your password\n")
    register(new_username,new_password)

def sign_in_method():
  user_option = input("please login or regesiter to continue\nenter L to login or R to register\n")
  user_option = user_option.upper()
  if (user_option != "L" and user_option != "R"):
    print("sorry that was not an option")
    sign_in_method()
  if (user_option =="L"):
    username = input ("enter your username\n")
    password = input ("enter your password\n")
    login(username,password,)
  else:
    print("Please create a username and password")
    username = input ("enter your username\n")
    password = input ("enter your password\n")
    register(username,password,)

sign_in_method()   

#quiz_apis = []
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
correct_guesses = 0
for i,question in enumerate(data):
  print(unescape(question["question"]))
  print("The correct answer is ", unescape(question["correct_answer"]))
  all_answers = []
  all_answers.append(question["correct_answer"])
  for ans in question["incorrect_answers"]:
    all_answers.append(ans)
  random.shuffle(all_answers)
  for num, ans in enumerate(all_answers):
    print(f"{num+1}. {unescape(ans)}")
  users_choice = get_int_input('type in 1,2,3 or 4 to select your answer\n', 'PLEASE TYPE IN 1,2,3 OR 4 FOR YOUR ANSWER', 1, 4)
  correct_num = all_answers.index(question['correct_answer']) + 1
  if users_choice == correct_num:
    print("you guessed the correct answer\n")
    correct_guesses += 1
  elif users_choice != correct_num:
    print("you guessed the wrong answer. The correct ans was ", unescape(question["correct_answer"]), "\n")

# a print statment that tells the user how well they did
if 10 >= correct_guesses > 7:
  print(f"well done you got {correct_guesses*10}% correct. your amazing")
elif 7 >= correct_guesses >= 4:
  print(f"congradulations you got {correct_guesses*10}% correct. good job")
else:
  print(f"nice try you got {correct_guesses*10}% correct. better luck next time")
