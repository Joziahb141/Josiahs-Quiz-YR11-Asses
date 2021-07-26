
import time
import requests
from html import unescape
import random



# a function to log user in if they have an account
def login(username, password):
  logged_in = False
  file = open("user.txt", "r")
  for i in file:
    Username,Password,Best = i.split(",") # splits the info in each lina and cheaks to see if the info matches
    if Username == username and Password == password:
      logged_in = True
      break
  file.close()
  if logged_in == True:
    return (username,password,logged_in)
  else:
    print("your password or username is not recognised please try again or create a new account")
    return (username,password,logged_in)



# a function to register a new user if the user is new
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
    file.write(f"\n{username},{password},0.0:999999.9")
    file.close()
    return (username,password,valid)

  else:
    print("someone else already has that username please try again")
    return (username,password,valid)



# function to get a the user to sign in
def sign_in_method():
  logged_in = False
  while logged_in == False:
    user_option = input("please login or regesiter to continue\nenter L to login or R to register\n")
    user_option = user_option.upper()
    if user_option != "L" and user_option != "R":
      print("sorry that was not an option")
      sign_in_method()
      return
    if (user_option =="L"):
      username = input ("enter your username\n")
      password = input ("enter your password\n")
      u,p,logged_in = login(username,password)
    else:
      print("Please create a username and password")
      username = input ("enter your username\n")
      password = input ("enter your password\n")
      u,p,logged_in = register(username,password)
    if logged_in == True:
      return(u,p,logged_in)
      
username, password, logged_in = sign_in_method()  

print(f"********************************************************************************\n********************************************************************************\n*************** WELCOME {username.upper()} TO THE VEHCLE QUIZ ***************** \n********************************************************************************\n*********************************************************************************")

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
if logged_in == True:
  correct_guesses = 0
  start_time = time.time()
  question_num = 0
  for i,question in enumerate(data):
    question_num += 1

    # prints the question out
    print("question_num",unescape(question["question"]))
    print("The correct answer is ", unescape(question["correct_answer"]))
    all_answers = []
    all_answers.append(question["correct_answer"])
    for ans in question["incorrect_answers"]:
      all_answers.append(ans)
    random.shuffle(all_answers)
    for num, ans in enumerate(all_answers):

      # prints out all the possible answers for question and the number for the answer they represent
      print(f"{num+1}. {unescape(ans)}")
    users_choice = get_int_input('type in 1,2,3 or 4 to select your answer\n', 'PLEASE TYPE IN 1,2,3 OR 4 FOR YOUR ANSWER', 1, 4) # gets users input
    correct_num = all_answers.index(question['correct_answer']) + 1 # finds correct answer number

    # cheaks if user geussed the correct number and tells them if they did or didn't
    if users_choice == correct_num:
      print("you guessed the correct answer\n")
      correct_guesses += 1
    elif users_choice != correct_num:
      print("you guessed the wrong answer. The correct ans was ", unescape(question["correct_answer"]), "\n")



  # works out how long user took to complete the quiz and tells them
  end_time = time.time()
  duration = end_time - start_time
  duration = round(duration,1)
  print(f"you finished in {duration} seconds")



  # works out what percent the user got correct
  correct_percent = correct_guesses * (100/question_num)
  # a print statment that tells the user how well they did
  if 10 >= correct_guesses > 7:
    print(f"well done you got {correct_percent}% correct. your amazing")
  elif 7 >= correct_guesses >= 4:
    print(f"congradulations you got {correct_percent}% correct. good job")
  else:
    print(f"nice try you got {correct_percent}% correct. better luck next time")



# cheaking to see if the user got a new highscore and saving it to their info in the file
file = open("user.txt","r")
new_file_info = ""
for line in file:
  Username,Password,best = line.split(",")
  if username == Username and password == Password:
    best_percent,best_time = best.split(":")

    # cheaks to see if the users score is better than there highscore
    if float(best_percent) < correct_percent:
      new_line_info = line.replace(best_percent,f"{correct_percent}").replace(best_time,f"{duration}\n")
      new_file_info = f"{new_file_info}{new_line_info}"
    elif float(best_percent) == correct_percent and float(best_time) > duration:
      new_line_info = line.replace(best_percent,f"{correct_percent}").replace(best_time,f"{duration}\n")
      new_file_info = f"{new_file_info}{new_line_info}"
    else:
      continue
  else:
    new_file_info = f"{new_file_info}{line}"

file = open("user.txt","w")
file.write(new_file_info)
file.close()
