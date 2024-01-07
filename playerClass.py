import json


class Player:

  def __init__(self, username, password, location):
    self.__matchesWon = 0
    self.__matchesPlayed = 0
    self.__moneySpent = 0  # default currency in sterling pounds (converter needed)
    self.__moneyWon = 0
    self.__position = 0  # 1 is top
    self.__fixtures = []
    self.__username = username
    self.__password = password
    self.__location = location

  def showDetails(self):
    pass

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
    while not cancel:
      username = self.createUsername(["uname1", "uname2"])
      password = self.createPassword()
      location = self.createLocation(["UK", "US", "AU"])
      print("Please review your details:")
      print(
          f"Username: {self.username}\nPassword: {'*'*len(self.password)}\nLocation: {self.location}"
      )
      breakLoop = False
      while not breakLoop:
        option = input("Would you like to finish your registration (Y/n): ")
        if option in {"", "Y", "y"}:
          cancel = True
          breakLoop = True
        elif option in {"N", "n"}:
          breakLoop = True
        else:
          print("That's not an option.")
    if cancel is False:
      self.__init__(username, password, location)
      # save player data

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

  #===========Methods===========

  def createUsername(self, usernames):  # check username is unique
    username = input("Enter a new username: ")
    while username not in usernames:
      username = input("Enter a new username: ")
      if username in usernames:
        print("Username taken.")
    return username

  def createPassword(self):  # check password strength
    print("Passwords must be at least 8 characters long.")
    password = input("Enter a new password: ")
    while len(password) < 8:
      print("Your password does not match the criteria.")
      password = input("Enter a new password: ")
    return password

  def createLocation(self, locations):
    print("Available locations:", locations)
    location = input("Enter your location: ")
    while location not in locations:
      location = input("Enter your location: ")
      if location not in locations:
        print("Invalid location.")
    return location


testdict = {"location": "UK"}

Fab = Player("fabi", "123", "UK")
#print(Fab.getAllData())
#print(Fab.removePlayer("misterman"))
print(Fab.addPlayer("fab"))
print(Fab.savePlayerData("fab", testdict))
