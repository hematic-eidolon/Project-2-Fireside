import json, authenticatorHandler


class Player:

  def __init__(self):
    self.__matchesWon = 0
    self.__matchesPlayed = 0
    self.__moneySpent = 0  # default currency in sterling pounds (converter needed)
    self.__moneyWon = 0
    self.__position = 0  # 1 is top
    self.__fixtures = []
    self.__username = ""
    self.__password = ""
    self.__location = ""

  #===========Setters===========

  def setUsername(self, username):
    self.__username = username

  def setPassword(self, password):
    self.__password = password

  def setLocation(self, location):
    self.__location = location

  #===========Getters===========

  def getUsername(self):
    return self.__username

  def getPassword(self):
    return self.__password

  def getLocation(self):
    return self.__location

  #===========Methods===========

  #-----------JSON-----------

  # def getUserData(self, username):
  #   try:
  #     with open("players.json", mode="r") as file:
  #       userData = json.load(file)[username]
  #       return userData
  #   except json.JSONDecodeError:
  #     return -1  # Error parsing from json
  #   except FileNotFoundError:
  #     return -2  # File not found

  def getFileData(self, fileName):
    try:
      with open(fileName, mode="r") as file:
        allData = json.load(file)
        return allData
    except json.JSONDecodeError:
      return -1  # Error parsing from json
    except FileNotFoundError:
      return -2  # File not found

  def getAllPlayerData(self):
    return self.getFileData("players.json")

  def savePlayerData(self, freshUserData):  # essentially updates a player
    try:
      allData = self.getAllPlayerData()
      username = freshUserData["username"]
      if type(allData) is dict:
        if username in allData:
          freshUserData.pop("username")
          allData[username] = freshUserData
          with open("players.json", mode="w") as file:
            json.dump(allData, file, indent=4)
        else:
          return -3  # User not recorded
    except json.JSONDecodeError:
      return -1  # Error parsing from json
    except FileNotFoundError:
      return -2  # File not found

  def addPlayer(self, username):
    try:
      allData = self.getAllPlayerData()
      playerList = self.getPlayerList()
      if type(allData) is dict:
        # only initialises a pair "username": None, use savePlayerData() as well
        if username not in allData and username not in playerList["usernames"]:
          allData[username] = None
          playerList["usernames"].append(username)
          with open("players.json", mode="w") as file:
            json.dump(allData, file, indent=4)
          with open("playerList.json", mode="w") as file:
            json.dump(playerList, file, indent=4)
          return 0
        else:
          return -3  # User is already recorded, no changes made
    except json.JSONDecodeError:
      return -1  # Error parsing from json
    except FileNotFoundError:
      return -2  # File not found

  def removePlayer(self, username):
    try:
      allData = self.getAllPlayerData()
      allData.pop(username)
      with open("players.json", mode="w") as file:
        json.dump(allData, file, indent=4)
      playerList = self.getPlayerList()
      playerList["usernames"].remove(username)
      with open("playerList.json", mode="w") as file:
        json.dump(playerList, file, indent=4)
    except json.JSONDecodeError:
      return -1  # Error parsing from json
    except FileNotFoundError:
      return -2  # File not found
    except KeyError:
      return -3  # User not recorded, this is fine
      
  def checkJsonError(self, error, isReg = False) -> bool:
    if error in {-1,-2,-3}:
      match error:
        case -3:
          if isReg:
            print("User already recorded, no changes made.")
          else:
            print("User not recorded.")
        case -1:
          print("Error parsing from JSON.")
        case -2:
          print("Player data storage file not found.")
      isFine = False
    else:
      isFine = True
    return isFine

  def getPlayerList(self):
    return self.getFileData("playerList.json")
    
  def updateUserName(self, username1, username2):
    try:
      playerList = self.getPlayerList()
      allData = self.getAllPlayerData()
      if username1 in playerList["usernames"] and username1 in allData:
        playerList["usernames"].remove(username1)
        playerList["usernames"].append(username2)
        allData[username2] = allData.pop(username1)
        with open("playerList.json", mode="w") as file:
          json.dump(playerList, file, indent=4)
        with open("players.json", mode="w") as file:
          json.dump(allData, file, indent=4)
        return 0
      else:
        return -3  # User not recorded
    except json.JSONDecodeError:
      return -1  # Error parsing from json
    except FileNotFoundError:
      return -2  # File not found

  #-----------Player Functions-----------

  def registerPlayer(self):
    cancel = False
    errorEncountered = False
    while cancel is False:
      username = self.createUsername()
      if username in {-1,-2}:
        errorEncountered = True
        self.checkJsonError(username)
        print("An error has occured. Cannot continue with registration.")
        input("Press enter to continue: ")
        break # error, cannot continue with registration
      password = self.createPassword()
      location = self.createLocation()
      print("Please review your details:")
      print(
          f"Username: {username}\nPassword: {'*'*len(password)}\nLocation: {location}"
      )
      breakLoop = False
      while breakLoop is False:
        option = input("Would you like to finish your registration (Y/n): ")
        if option in {"", "Y", "y"}:
          cancel = True
          breakLoop = True
        elif option in {"N", "n"}:
          breakLoop = True
        else:
          print("That's not an option.")
    if errorEncountered is False:
      freshUserData = {"username":username, 
                      "password":str(authenticatorHandler.returnHash(password)),
                       "location":location,
                       "leaderboardPosition":0,
                       "matchesWon":0,
                       "matchesPlayed":0,
                       "moneySpent":0,
                       "moneyWon":0,
                       "fixtures":[]
                      }
      return freshUserData

  def createUsername(self):  # check username is unique
    allData = self.getAllPlayerData()
    if type(allData) is dict:
      username = input("Enter a new username: ")
      while username in allData:
        if username in allData:
          print("Username taken.")
        username = input("Enter a new username: ")
      return username
    else:
      return allData # returns error code

  def createPassword(self):  # check password strength
    print("Note: Passwords must be at least 8 characters long.\n")
    # this line below uses the authenticatorhandler getPassword function
    # this hides the text entered and replaces it with * so makes it more secure.
    password = authenticatorHandler.authenticator.getPassword(None)  # NOQA
    while len(password) < 8:
      print("Your password does not match the criteria.")
      password = authenticatorHandler.authenticator.getPassword(None)
    print("success")
    return password

  def createLocation(self):
    allLocations = {"UK", "US", "AU"}
    print("Available locations: UK, US, AU")
    location = input("Enter your location: ").upper()
    while location not in allLocations:
      print("Invalid location.")
      location = input("Enter your location: ").upper()
    return location

  def showDetails(self, username):
    try:
      allData = self.getAllPlayerData()
      if type(allData) is dict:
        if username in allData:
          userData = allData[username]
          for item in userData:
            itemName = item[0].upper() + item[1:]
            if item == "password":
              print(f"{itemName}:**Hidden**")
            else:
              print(f"{itemName}: {userData[item]}")
        else:
          return -3  # User not recorded
    except json.JSONDecodeError:
      return -1  # Error parsing from json
    except FileNotFoundError:
      return -2  # File not found

  def modifyPlayer(self):
    cancel = False
    options = ["Change a username", "Change a password", "Change a location", "Remove a player", "Exit player modification"]
    while cancel is False:
      print("---------------------------------")
      print("Welcome to the player modifier.\nOptions are shown below:")
      for index, message in enumerate(options):
        print(index, message)
      option = int(input("Enter an option: "))
      while not 0<=option<(len(options)):
        print("\nInvalid option. Please try again.\n")
        for index, message in enumerate(options):
          print(index, message)
        option = int(input("Enter an option: "))
      if option == 0:
        username1 = input("Existing username to replace: ")
        while username1 not in self.getAllPlayerData():
          print("\nUsername not found.\n")
          username1 = input("Existing username to replace: ")
        username2 = input("Enter a new username: ")
        self.updateUserName(username1,username2)
      elif option == 1:
        username = input("Enter a username: ")
        while username not in self.getAllPlayerData():
          print("\nUsername not found.\n")
          username = input("Enter a username: ")
        password = self.createPassword()
        allData = self.getAllPlayerData()
        freshUserData = allData[username]
        freshUserData["password"] = str(authenticatorHandler.returnHash(password))
        freshUserData["username"] = username
        self.savePlayerData(freshUserData)
      elif option == 3:
        username = input("Enter a username: ")
        while username not in self.getAllPlayerData() and username not in self.getPlayerList()["usernames"]:
          print("\nUsername not found.\n")
          username = input("Enter a username: ")
        self.removePlayer(username)
      elif option == len(options)-1:
        cancel = True

#===========Testing===========

Fab = Player()

#print(Fab.registerPlayer())
#print(Fab.showDetails("fab"))

#authenticatorHandler.checkPass(correcthash, inputstring)

# print(authenticatorHandler.checkPass(hash, strIn))

#Fab.modifyPlayer()
#print(Fab.addPlayer("fabs"))

#print(Fab.removePlayer())
