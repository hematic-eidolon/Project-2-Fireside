# === External Files === #
import authenticatorHandler  # NOQA
import currencyHandler
import asciiArt
import playerClass
import fixtureClass

# === External Libraries === #
from colorama import Fore

# === Builtin Libraries === #
import os
import sys
import time
import datetime
import json

# ==================== ATTEMPTS FUNCTION ================ #
# This function is used to call a function repreated times
# E.g. 3 password guesses

# PARAMETERS:
# func: reference to function to be called multiple times (must return a boolean)
# tries: integer, number of allowed attempts of the function
# prompt: a string to prompt the user between calls with, *t is replaced with the number of tries left. # NOQA

# RETURNS:
# bool, if function returned success, false if too many attempts.

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


# ====================== VALIDATION FUNCTION ================== #

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


# ======================================================#


def adminMenu():
  print(Fore.BLUE + asciiArt.admin_title)
  print(Fore.WHITE + """
    1: Host a new fixture
    2: Delete a fixture
    3: View a fixture
    4: Add results.
    5: View results
    6: Add a new user
    7: View a profile
    8: Edit a user
    9: Quit
  """)
  choice = verifyOptionInput(0, 8, input(">"))
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
      input(Fore.GREEN + "Fixture saved successfully." + Fore.WHITE)
  
    case 2:
      print("Deleting a fixture")
      print(Fore.RED + "WARNING! DELETING A FIXTURE IS PERMANENT")
      print(Fore.WHITE + "Active Fixtures:")
      print(str(activeFixtures)[1:-2])
      fName = input("Enter fixture name to delete:")
      
      for fixture in activeFixtures:
        if fixture.getName() == fName and authenticatorMaster.getPasswordAndAuthenticate(): # NOQA
            print(Fore.RED + f"Confirm delete fixture {fName}? (Y/n)")
            cfm = input()
            if cfm.lower() == "y":
              del activeFixtures[activeFixtures.index(fName)]
          
        print(Fore.WHITE)
        break
  
    case 3:
      print("Viewing a fixture")
      print("Fixtures listed: ")
      print(str(activeFixtures)[1:-2])
      print("Enter a fixture name to view:")  
      fixName = input()
      for fixture in activeFixtures:
        if fixture.getName() == fixName:
          print(f"""
            {Fore.BLUE} Fixture: {fixName + Fore.WHITE}
            ------------------
            {Fore.RED} ID: {Fore.WHITE}           {fixture.getID()}
            {Fore.RED} Date: {Fore.WHITE}         {fixture.getDatePretty()}
            {Fore.RED} Entry Fee: {Fore.WHITE}    £{fixture.getFee()}
            {Fore.RED} Prize Money: {Fore.WHITE}  £{fixture.getPrizeMoney()}
          """)
          input()
          break
  
    case 4:
      print("Add a fixture's results!")
      #  Loop for each player
      p1 = p2 = ""
      found = False
      for p_searched in [p1, p2]:
        p_searched = input('Name of the first player: ')
        with open('players.json', 'r') as f:
          player_info = json.load(f)
          for player in player_info:
            if player.lower() == p_searched.lower():
              p_searched = player
              found = True
              break
          if not found:
              print('Player not in database!')
              return
 
      winner = input(f'Who was the winner of the match, (1) {p1} or (2) {p2}')
      with open('players.json', 'r') as f:
        player_info = json.load(f)
        player_info[player]['wins'] += 1
      with open('players.json', 'w') as f:
        json.dump(player_info, f, indent=2)
        
    case 9:
      sys.exit()

# ===============================================#


## END OF MAIN ADMIN LOOP, LOADING MAIN FUNCTIONS HERE ##


#============= OPENING GRAPHICS =================#
print(Fore.BLUE + asciiArt.fireside_title)
print(Fore.RED)

print(f"{'ENTER PASSWORD:' : ^50}")

# success = multipleAttemptsFunction(
  # authenticatorMaster.getPasswordAndAuthenticate,
  # 3,
  # Fore.RED + "Incorrect password. *t tries remaining."
# )


fixtureClass.loadFixturesFromJSON()
input()


if 1: # switch this around to disable admin authentication when testing
# if success:
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