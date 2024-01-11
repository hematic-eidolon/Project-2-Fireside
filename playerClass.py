import json


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
    self.username = username

  def setPassword(self, password):
    self.password = password

  def setLocation(self, location):
    self.location = location

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

  def getAllData(self):
    try:
      with open("players.json", mode="r") as file:
        #allData = {"fabs": None}
        allData = json.load(file)
        return allData
    except json.JSONDecodeError:
      return -1  # Error parsing from json
    except FileNotFoundError:
      return -2  # File not found

  def savePlayerData(self, username, freshUserData):
    try:
      allData = self.getAllData()
      if type(allData) is dict:
        if username in allData:
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
      allData = self.getAllData()
      if type(allData) is dict:
        # only initialises a pair "username": None, use savePlayerData() as well
        if username not in allData:
          allData[username] = None
          with open("players.json", mode="w") as file:
            json.dump(allData, file, indent=4)
        else:
          return -3  # User is already recorded, no changes made
    except json.JSONDecodeError:
      return -1  # Error parsing from json
    except FileNotFoundError:
      return -2  # File not found

  def removePlayer(self, username):
    try:
      allData = self.getAllData()
      if type(allData) is dict:
        allData.pop(username)
        with open("players.json", mode="w") as file:
          json.dump(allData, file, indent=4)
    except json.JSONDecodeError:
      return -1  # Error parsing from json
    except FileNotFoundError:
      return -2  # File not found
    except KeyError:
      return -3  # User not recorded, this is fine

  #-----------Player Functions-----------

  def registerPlayer(self):
    cancel = False
    while cancel is False:
      username = self.createUsername()
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
    if cancel is False:
      for dataPiece in [self.getUsername(), self.getPassword()]:
        pass

  def createUsername(self):  # check username is unique
    try:
      allData = self.getAllData()
      if type(allData) is dict:
        username = input("Enter a new username: ")
        while username in allData:
          if username in allData:
            print("Username taken.")
          username = input("Enter a new username: ")
        return username
    except:
      print("Error.")
      return None

  def createPassword(self):  # check password strength
    print("Note: Passwords must be at least 8 characters long.\n")
    password = input("Enter a new password: ")
    while len(password) < 8:
      print("Your password does not match the criteria.")
      password = input("Enter a new password: ")
    print("success")
    return password

  def createLocation(self):
    allLocations = {"UK", "US", "AU"}
    print("Available locations: UK, US, AU")
    location = input("Enter your location: ").upper()
    while location not in allLocations:
      #if location not in allLocations:
      print("Invalid location.")
      location = input("Enter your location: ").upper()
    return location

  def showDetails(self):
    pass


#===========Testing===========

Fab = Player()
#print(Fab.getAllData())
#print(Fab.removePlayer("misterman"))
#print(Fab.addPlayer("fab"))
#print(Fab.savePlayerData("fab", testdict))

print(Fab.registerPlayer())

# authenticatorHandler.returnHash(password) -> str
# authenticatorHandler.checkpass(correcthash, inputstring)
