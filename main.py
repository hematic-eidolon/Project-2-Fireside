import authenticatorHandler  # NOQA
import currencyHandler
import asciiArt
import playerClass
from colorama import Fore, Back
import fixtureClass
import os
import time
import datetime
import json

# ==================== ATTEMPTS FUNCTION ================ #
# This function is used to call a function repreated times
# E.g. 3 password guesses
# 
def multipleAttemptsFunction(func, tries, prompt) -> bool:
  tries-=1
  if func():
    return True
  else:
    if tries == 0:
      return False
    _prompt=prompt.replace("*t",str(tries))
    print(_prompt)
    return multipleAttemptsFunction(func, tries, prompt)
    
currencyHandlerMaster = currencyHandler.currencyHandler()
authenticatorMaster = authenticatorHandler.authenticator()
activeFixtures = []


# ======================================================== #

def verifyOptionInput(minimumInteger: int, maximumInteger: int,
                      userInput: str) -> int:
  try:
    _userInput = int(userInput)
    if _userInput < minimumInteger or _userInput > maximumInteger:
      return -1
    else:
      return _userInput

  except ValueError:
    return -1
  except Exception:
    return -2

  # RETURN VALUES:
  # -1: the input the user entered didn't match the requirements.
  # -2: the function threw an error.

  # Otherwise, the integer value of the input is returned.

  # min and max: checks that min < input < max - EXCLUSIVE
  #--------------------------END-----------------------------#

def adminMenu():
  print(Fore.BLUE + asciiArt.admin_title)
  print(Fore.WHITE + """
    1: Host a new fixture
    2: Edit a fixture
    3: View a fixture
    4: Add results.
    5: View results
    6: Add a new user
    7: View a profile
    8: Edit a user
    9: Quit
  """)
  choice = verifyOptionInput(0, 8, input(">"))
  print(choice)

  match choice:
    case 1:
      # ================= FIXTURE GENERATOR =============== #
      os.system("clear")
      print(Fore.BLUE + asciiArt.fixture_title)
      print(Fore.WHITE)
      fName = input("Enter a fixture name: ")
      fDate = input("Enter a date (dd/mm/yyyy): ")
      fPlayers = input("Enter player usernames, spaced with a comma: ")
      fEntryFee = input("Enter an entry fee in GBP: £")
      fPrizeMoney = input("Enter prize money in GBP: £")

      date_list = fDate.split("/")
      try:
        date_list = [int(x) for x in date_list]
        fixtureDate = datetime.datetime(date_list[2],date_list[1],date_list[0])
      except (ValueError, TypeError):
        input(Fore.RED + "INVALID DATE FORMAT. Operation cancelled.")
        return

      try:
        fEntryFee = float(fEntryFee)
        fPrizeMoney = float(fPrizeMoney)

      except (ValueError, TypeError):
        input(Fore.RED + "Invalid monetary format. Operation cancelled.")
        return

      activeFixtures.append(fixtureClass.Fixture(
        ID=0,
        currencyHandlerRef=currencyHandlerMaster,
        date=fixtureDate,
        name=fName,
        players=fPlayers,
        entryFee=fEntryFee,
        prizeMoney=fPrizeMoney
      ))
      input(activeFixtures)
  
    case 2:
      print("Editing a fixture")
    case 3:
      print("Viewing a fixture")
      print("Fixtures listed: ")
      print([x for x in activeFixtures])
      print("Enter a fixture name to view:")  
      input()
      

    case 9:
      quit()

#============= OPENING GRAPHICS =================#
print(Fore.BLUE + asciiArt.fireside_title)
print(Fore.RED)

print(f"{'ENTER PASSWORD:' : ^50}")

success = multipleAttemptsFunction(
  authenticatorMaster.getPasswordAndAuthenticate,
  3,
  Fore.RED + "Incorrect password. *t tries remaining."
)

if success:
  print(Fore.GREEN)
  print("LOGIN SUCCESSFULL. ADMIN ACCESS GRANTED")
  print(Fore.WHITE)
  time.sleep(1)
  while 1:
    os.system("clear")
    adminMenu()
else:
  print("INCORRECT. ")
  print("""
    Enter 1 to login as a non-admin user.
    Enter 2 to quit.
  """)
  choice = 0
  try:
    choice = int(input(">"))
  except: # NOQA
    print("Invalid choice.")

  if choice == 1:
    pass
  elif choice == 2:
    quit()
