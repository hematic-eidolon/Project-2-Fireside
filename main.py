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

PlayerInstance = playerClass.Player()

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

nextFixID = 0
with open("settings.json") as f:
  nextFixID = int(dict(json.load(f))["settings"]["nextFixtureID"])


# ====================== VALIDATION FUNCTION ================== #

def verifyOptionInput(minimumInteger: int, maximumInteger: int,
                      userInput: str, __id:bool) -> int:
  if __id and userInput.lower() == "q":
    return 9
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
  global nextFixID
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
    9: Quit (or type q)
  """)
  choice = verifyOptionInput(0, 10, input(">"), True)
  match choice:
    case 1:
      # ================= FIXTURE GENERATOR =============== #
      os.system("clear")
      print(Fore.BLUE + asciiArt.fixture_title + Fore.WHITE)

      # GET FIXTURE DETAILS
      
      fName = input("Enter a fixture name: ")
      fDate = input("Enter a date (dd/mm/yyyy): ")
      fPlayers = input("Enter player usernames, spaced with a comma: ")
      fEntryFee = input("Enter an entry fee in GBP: £")
      fPrizeMoney = input("Enter prize money in GBP: £")

      # PROCESS DATE FROM STRING INTO DATETIME (WITH VALIDATION)

      date_list = fDate.split("/")
      try:
        date_list = [int(x) for x in date_list]
        fixtureDate = datetime.datetime(date_list[2],date_list[1],date_list[0])
      except (ValueError, TypeError):
        input(Fore.RED + "INVALID DATE FORMAT. Operation cancelled.")
        return

      # CONVERT PRICES INTO FLOATS WITH VALIADTION

      try:
        fEntryFee = float(fEntryFee)
        fPrizeMoney = float(fPrizeMoney)

      except (ValueError, TypeError):
        input(Fore.RED + "Invalid monetary format. Operation cancelled.")
        return

      # ADD FINISHED FIXTURE TO FIXTURE LIST

      activeFixtures.append(fixtureClass.Fixture(
        ID=nextFixID,
        currencyHandlerRef=currencyHandlerMaster,
        date=fixtureDate,
        name=fName,
        players=fPlayers,
        entryFee=fEntryFee,
        prizeMoney=fPrizeMoney
      ))

      # INCREMENT NEXTFIXID
      # need to reload settings afterwards to make sure it's saved
      # now need to refresh json storage to actually save the thing
      nextFixID += 1
      try:
        # load json to make sure nothing overwritten
        with open("settings.json") as f:
          data = dict(json.load(f))
        # turn the active fixture list into a ser'able list  
        data["fixtures"] = [x.serMe() for x in activeFixtures] 
        # increment the next id to reflect the new one
        data["settings"]["nextFixtureID"] += 1
        # now dump json to file
        with open("settings.json","w") as f:
          json.dump(data, f, indent=2)

        # output sucess message
          
        input(Fore.GREEN + "Fixture saved successfully. Press Enter" + Fore.WHITE)
      except Exception: # don't use bare except block will kill ctrl+c usage
        input(Fore.RED + "Fixture couldn't be saved! Press Enter" + Fore.WHITE)
        # oh dear! tell the user its all gone badly wrong
  
    case 2:
      print(Fore.RED + "WARNING! DELETING A FIXTURE IS PERMANENT")
      print(Fore.WHITE + "Active Fixtures:")
      # this is a very cursed way of printing the list but it saves time
      print(str(activeFixtures)[1:-1])
      fName = input("Enter fixture name to delete:")

      # CHECK FOR MATCH 
      
      for fixture in activeFixtures:
        if fixture.getName() == fName and authenticatorMaster.getPasswordAndAuthenticate(): # NOQA
            print(Fore.RED + f"Confirm delete fixture {fName}? (Y/n)")
            # CHECK TO DELETE AND AUTHENTICATE TO DO SO
            cfm = input()
            if cfm.lower() == "y":
              del activeFixtures[activeFixtures.index(fName)]
          
        print(Fore.WHITE)
        break # NO NEED TO CONTINUE CHECKING
  
    case 3:
      print("Viewing a fixture")
      print("Fixtures listed: ")
      print(str(activeFixtures)[1:-1])
      print("Enter a fixture name to view:")  
      fixName = input()
      # iterate over the active fixrure list
      for fixture in activeFixtures:
        # check for a match
        if fixture.getName() == fixName:
          # pretty-print the fixture details to the user
          os.system("clear")
          print(f"""
            {Fore.BLUE} Fixture: {fixName}
            ------------------{Fore.WHITE}
            {Fore.RED} ID: {Fore.WHITE}           {fixture.getID()}
            {Fore.RED} Date: {Fore.WHITE}         {fixture.getDatePretty()}
            {Fore.RED} Entry Fee: {Fore.WHITE}    £{fixture.getFee()}
            {Fore.RED} Prize Money: {Fore.WHITE}  £{fixture.getPrizeMoney()}
          """)
          input()
          # stop checking for more fixtures since one has been found
          break
  
    case 4:
      # --------- ADD RESULT --------- #
      print(Fore.BLUE + "Add a fixture's results!" + Fore.WHITE)
      p1 = p2 = "" # 2 players for each result
      found = False
      for p_searched in [p1, p2]:
        # Looping for each player
        p_searched = input('Name of the first player: ')
        with open('players.json', 'r') as f:
          # Taking information for players.json
          player_info = json.load(f)
          for player in player_info:
            if player.lower() == p_searched.lower():
              print(player.lower())
              print(p_searched.lower())
              # Checking if player exists
              p_searched = player
              found = True
              break
          if not found:
              print('Player not in database!')
              # Player does not exist
              return
 
      winner = input(f'Who was the winner of the match, (1) {p1} or (2) {p2}')
      # Checks the winner
      with open('players.json', 'r') as f:
        player_info = json.load(f)
        player_info[player]['wins'] += 1
        # Increases the players wins by 1
      with open('players.json', 'w') as f:
        json.dump(player_info, f, indent=2)
      input()

    case 5:
      os.system("clear")
      # Title
      print(Fore.BLUE+asciiArt.leaderboard_title+Fore.WHITE)
      # Gets information from players.json
      with open('players.json', 'r') as f:
        player_info = json.load(f)
        # Sorts the information by the number of wi ns
        sorted_players = dict(sorted(player_info.items(), key=lambda item: item[1]['wins'], reverse=True))
        
        for player, info in sorted_players.items():
          for inf, value in info.items():
            # Unpacks nested dictionary to get player wins for each player
            if inf == 'wins':
              wins = value
              break
          print(f'{player}, wins: {wins}')
        input()
        # Sorts list by item[x] (change x depending on where position is)
    case 6:
      PlayerInstance.registerPlayer()
    case 7:
      queriedUsername = input("Username to search for: ")
      error = PlayerInstance.showDetails(queriedUsername)
      match error:
        case -3:
          print("User not recorded.")
        case -1:
          print("Error parsing from JSON.")
        case -2:
          print("Player data storage file not found.")
      input()
    case 9:
     sys.exit()
    # any other clearup needs to go here, don't think this applies to anything rn


# ===============================================#


## END OF MAIN ADMIN LOOP, LOADING MAIN FUNCTIONS HERE ##


#============= OPENING GRAPHICS =================#
print(Fore.BLUE + asciiArt.fireside_title + Fore.RED)
print(f"{'ENTER PASSWORD:' : ^50}")

success = multipleAttemptsFunction(
  authenticatorMaster.getPasswordAndAuthenticate,
  3,
  Fore.RED + "Incorrect password. *t tries remaining."
)


# activeFixtures = fixtureClass.loadFixturesFromJSON(currencyHandlerMaster)  

if 1: # switch this around to disable admin authentication when testing
# if success:
  print(Fore.GREEN + "LOGIN SUCCESSFULL. ADMIN ACCESS GRANTED" + Fore.WHITE)
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
  except Exception:
    print("Invalid choice.")

  if choice == 1:
    pass
  elif choice == 2:
    quit()