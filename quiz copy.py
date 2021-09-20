import time
import requests
import random
import colorama
import bcrypt
from html import unescape
from cryptography.fernet import Fernet
from colorama import Fore,Back,Style

def get_key():
  ''' gets the key to use for encryption and decryption '''
  with open("key.key","rb") as file:
    key = file.read()
  return key

def encrypt_file(file_directory:str,key) :
  ''' encrypts a file and replaces the info in the file with the encryption'''
  f = Fernet(key)
  with open(file_directory,"rb") as file:
    fileinfo = file.read()
  encrypted = f.encrypt(fileinfo)
  with open(file_directory,"wb") as file:
    file.write(encrypted)

def decrypt_file(file_directory:str,key):
  ''' decrypts a file and replaces the info in the file with the decryption'''
  f = Fernet(key)
  with open(file_directory,"rb") as file:
    fileinfo = file.read()
  decrypt = f.decrypt(fileinfo)
  decoded = decrypt.decode()
  with open(file_directory,"w") as file:
    file.write(decoded)

def sign_in_choice() ->bool :
  ''' gets user to choose a sign in method'''
  valid = False
  while valid == False:
    user_option = input(Back.BLACK + Style.BRIGHT + "please login or regesiter to continue\nenter L to login or R to register\n")
    user_option = user_option.upper()
    if user_option != "L" and user_option != "R":
      print(Fore.RED + Back.RESET + Style.BRIGHT + "sorry that was not an option")
    else:
      valid,user,pswd = sign_in(user_option.upper())
  return user,pswd

def sign_in(sign_in_method:str) ->bool:
  ''' signs user in based of what choice they made '''
  username = input (Back.BLACK + Style.BRIGHT + "enter your username\n")
  password = input (Back.BLACK + Style.BRIGHT + "enter your password\n")
  if (sign_in_method =="L"):
    return login(username,password),username,password
  else:    
    return register(username,password),username,password

def login(username:str,password:str) ->bool:
  ''' cheak to see if users account is in database and logges them in'''
  if check_file(username,password):
    print(Fore.YELLOW + Style.BRIGHT + "********************************************************************************\n********************************************************************************\n***************", Fore.RED + Style.BRIGHT + f" WELCOME {username.upper()} TO THE VEHCLE QUIZ ", Fore.YELLOW  + Style.BRIGHT + "***************** \n********************************************************************************\n*********************************************************************************")
    return True
  else:
    print(Fore.RED + Back.RESET + Style.BRIGHT + "your password or username is not recognised please try again or create a new account")
    return False 

def register(username:str,password:str) ->bool:
  ''' register user if they have entered new info '''
  if not check_file(username,password):
    write_hash(make_hash(username),make_hash(password))
    print(Fore.YELLOW + Style.BRIGHT + "********************************************************************************\n********************************************************************************\n***************", Fore.RED + Style.BRIGHT + f" WELCOME {username.upper()} TO THE VEHCLE QUIZ ", Fore.YELLOW  + Style.BRIGHT + "***************** \n********************************************************************************\n*********************************************************************************")
    return True
  else:
    print(Fore.RED + Back.RESET + Style.BRIGHT + "the info you entered is simular to another user please change your username and password")
    return False    

def make_hash(info:str) ->str:
  ''' takes a string a makes it into a hash'''
  return bcrypt.hashpw(info.encode("utf-8"),bcrypt.gensalt()).decode()
  
def write_hash(username:str,password:str):
  ''' writes the new hashes in the database '''
  with open("Josiahs-Quiz-YR11-Asses/user_info.txt","a") as file:
    file.write(f"\n{username},{password},easy:0.0:999999.0 medium:0.0:999999.9 hard:0.0:999999.9 any:0.0:999999.9,")

def check_file(username:str,password:str) ->bool:
  ''' cheak if the info entered matches any in the database '''
  with open("Josiahs-Quiz-YR11-Asses/user_info.txt","r") as file:
    for line in file:
      try:
        user,pswd,best_scores,end_of_line = line.split(",")
        if check_hash(username,user) and check_hash(password,pswd):
          return True
          break
      except:
        continue
  return False
        
def check_hash(info:str,hash:str) ->bool:
  ''' cheaks to see if the info entered matches the hash and returns the result '''
  return bcrypt.checkpw(info.encode("utf-8"),hash.encode('utf-8'))

def get_int_input(message:str, error:str, low:int, high:int) ->int:
  ''' gets an int input between two given values '''
  while True:
    try:
      # try to get an int input from user but returns error if not possible
      inpt = int(input(message))
      if low < inpt < high or low == inpt or high == inpt:
        return inpt
      else:
        print(error)
    except ValueError:
      print(error)

def check_answer(user_choice:int,ans_num:int,correct_answer:str) ->int:
  ''' cheaks if users answer is the correct answer '''
  if user_choice == ans_num:
    # congradulates user if their answer matches and returns 1 to add to there score
    print(Fore.GREEN + Style.BRIGHT +"you guessed the correct answer\n")
    return 1
  else:
    # tells user they got the answer wrong and tells them what the correct one was 
    print(Fore.RED + Style.BRIGHT + "you guessed the wrong answer. The correct ans was ", Fore.RED + Style.BRIGHT +  correct_answer, "\n")
    return 0

def print_question(question:str,question_num:int):
  ''' prints out the question '''
  print(Fore.CYAN + Style.BRIGHT + f"{question_num}.", Fore.YELLOW + Style.BRIGHT + question)

def print_answers_in_random_order(correct_ans:str,incorrect_answers:list) ->list:
  ''' gets the answers and prints them out in a random order '''
  questions_answers =[]
  # added the correct answer to the possible answers
  questions_answers.append(correct_ans)
  for ans in incorrect_answers:
    # adds the incorrect answers to the possible answers then shuffles the possible answers to mix the order up
    questions_answers.append(ans)
    random.shuffle(questions_answers)
  for num, ans in enumerate(questions_answers):
    # prints the possible answers 
    print(Fore.CYAN+ Style.NORMAL + f"{num+1}.", Fore.YELLOW + Style.BRIGHT + unescape(ans))
  # gives the questions answers and the correct_answer back
  return questions_answers,int(questions_answers.index(correct_ans))+1

def get_api_info(difficulty:int) ->list:
  ''' gets the quiz info/data for the quiz the want to try'''
  if difficulty == 1:
    easy_response = requests.get('https://opentdb.com/api.php?amount=10&category=28&difficulty=easy')
    return easy_response.json()['results']
  elif difficulty == 2:
    medium_response = requests.get('https://opentdb.com/api.php?amount=10&category=28&difficulty=medium')
    return medium_response.json()['results']
  elif difficulty == 3:
    hard_response = requests.get('https://opentdb.com/api.php?amount=10&category=28&difficulty=hard')
    return hard_response.json()['results']
  else:
    any_response = requests.get("https://opentdb.com/api.php?amount=10&category=28")
    return any_response.json()['results']
  # returns the info recieved from the api in a list

def run_quiz():
  ''' runs the quiz '''
  # resets prints staments colours back to default after each statment
  colorama.init(autoreset=True)
  # decrypts the file with the users info will need to be ignored first time codes run
  #decrypt_file("Josiahs-Quiz-YR11-Asses/user_info.txt",get_key())
  # welcomes user to the quiz and tells them whats going to happen
  print(Back.BLACK + Fore.RED + Style.BRIGHT + "welcome. please sign in to continue to the quiz on vehicles")
  # gets the user to sign in and saves there user and pswd to find there account later
  user,pswd = sign_in_choice()
  # gets the info for the quiz based of a choice of difficulty
  quiz_difficulty = get_int_input(Fore.CYAN + Style.BRIGHT + "how difficult do you want the quiz to be\n1. easy\n2. medium\n3. hard\n4. any\n",Fore.RED + Style.BRIGHT + "that is not a valid option",1,4)
  data = get_api_info(quiz_difficulty)
  score = 0
  # statment that explains what will happen after they enter something
  start_quiz = input(Fore.MAGENTA + Style.BRIGHT + "you will be timed on how long it takes you to finish the quiz and will be told the time at the end.\n!!! prease enter to begin the quiz !!!")
  # gets the time when the quiz starts
  start_time = time.time()
  # creates a loop the runs through one question at a time untill there are no more
  for i,question in enumerate(data):
    # prints out the question
    print_question(unescape(question["question"]),i + 1)
    # prints out the questions answers in a random order
    question_answers,correct_ans = print_answers_in_random_order(unescape(question["correct_answer"]),unescape(question["incorrect_answers"]))
    # gets an int input from the user depending on the options they have
    users_choice = get_int_input(Fore.MAGENTA + Style.BRIGHT + 'type in 1,2,3 or 4 to select your answer\n', Fore.RED + Style.BRIGHT + 'PLEASE TYPE IN 1,2,3 OR 4 FOR YOUR ANSWER', 1, len(question_answers))
    # adds points to there score
    score += check_answer(users_choice, correct_ans, unescape(question["correct_answer"]))
  # records the time at the end to work out the time it took the user to finish the quiz
  end_time = time.time()
  # works out what percent the user got correct
  percent_correct = get_percent(i + 1, score)
  # works out the time it took the user to finish the quiz
  time_taken =  get_duration(start_time,end_time)
  # tells user how well they did
  give_results(time_taken, percent_correct)
  # cheaks if user beat there highscore and changes it if required
  change_file(user,pswd,percent_correct,time_taken,quiz_difficulty - 1)
  # encrypts the file
  encrypt_file("Josiahs-Quiz-YR11-Asses/user_info.txt",get_key())

def get_duration(start_time:float,end_time:float) ->float:
  ''' a function to work out the duration of a task'''
  return round(end_time - start_time,1)

def get_percent(item_length:int,amount_of_item:int) ->float:
  ''' works out the percent of something out of somthing else '''
  return (amount_of_item * 100/item_length)

def give_results(duration:float,percent:float):
  ''' works out the users percent and provides apropiete feedback on there preformance '''
  # a print statment that tells the user how well they did
  if 100 >= percent > 66 and duration < 60.0:
    print(Fore.GREEN + Style.BRIGHT + f"well done you got {percent}% correct in {duration} seconds. your amazing")
  elif 66 >= percent > 33 and duration < 150.0:
    print(Fore.CYAN + Style.NORMAL + f"congradulations you got {percent}% correct in {duration} seconds. good job")
  else:
    print(Fore.RED + Style.BRIGHT + f"nice try you got {percent}% correct in {duration} seconds. better luck next time")

def check_highscore(best_percent:float,new_percent:float,best_time:float,new_time:float,old_score_info:str,line_info:str) ->str:
  ''' cheaks to see if the users new score is better than there highscore '''
  if float(best_percent) < new_percent:
    print(Fore.GREEN + Style.BRIGHT + " CONGRADULATIONS YOU GOT A NEW PERSONAL BEST")
    # replaces the old score with the new one if the new percent is best
    score_info = replace_info(old_score_info,best_percent,str(new_percent))
    score_info = replace_info(score_info,best_time,str(new_time))
    # changes the old score for the new score
    line_info = replace_info(line_info,old_score_info,score_info)
    return line_info
  elif float(best_percent) == new_percent and float(best_time) > new_time:
    print(Fore.GREEN + Style.BRIGHT + " CONGRADULATIONS YOU GOT A NEW PERSONAL BEST")
    # replaces the old score with the new one if the time is better and the percent is the same
    score_info = replace_info(old_score_info,best_percent,str(new_percent))
    score_info = replace_info(score_info,best_time,str(new_time))
    # changes the old score for the new score
    line_info = replace_info(line_info,old_score_info,score_info)
    return line_info
  else:
    print(Fore.CYAN + Style.BRIGHT + f"you didn't beat your highscore of {best_percent}% in {best_time} seconds")
    return line_info

def replace_info(old_info:str,thing_to_replace:str,replacement:str) ->str:
  ''' replaces something in a string with something else '''
  return old_info.replace(thing_to_replace,replacement)

def check_user_info_match(username:str,password:str,file_username:str,file_password:str) ->bool:
  ''' cheaks if the users info matches the info from the line '''
  if check_hash(username,file_username) and check_hash(password,file_password):
    return True
  else:
    return False  

def change_file(username:str,password:str,users_percent:float,users_time:float,quiz_difficulty:int):
  ''' rerites the file with changes to users highscore if required '''
  with open("Josiahs-Quiz-YR11-Asses/user_info.txt","r") as file:
    new_file_info = ""
    # cheaks each line looking for the user
    for line in file:
      try:
        # stores the value from the value in each variable with the bests being for the quiz with that difficulty
        user,pswd,best_scores,end_of_line = line.split(",")
        # if it finds the user then it splits up their best percent and time and cheak there highscore for the quiz they did
        if check_user_info_match(username,password,user,pswd):
          # splits the different best scores up into 4 one for each difficulty
          best_scores = best_scores.split(" ")
          # finds the users best score for the difficulty they choose
          quiz_type,best_percent,best_time = best_scores[quiz_difficulty].split(":")
          # adds the new line to the info to replace the line with
          new_file_info = f"{new_file_info}{check_highscore(best_percent,users_percent,best_time,users_time,best_scores[quiz_difficulty],line)}"
        else:
          # adds the new line to the info to replace the file with
          new_file_info = f"{new_file_info}{line}"
      except:
        continue
    # writes the new file info to the file
  with open("Josiahs-Quiz-YR11-Asses/user_info.txt","w") as file:
    file.write(new_file_info)

run_quiz()