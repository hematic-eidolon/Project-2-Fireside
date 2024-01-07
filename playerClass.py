class Player:

  def __init__(self, username, password, location):
    self.matchesWon = 0
    self.matchesPlayed = 0
    self.moneySpent = 0  # default currency in sterling pounds (converter needed)
    self.moneyWon = 0
    self.position = 0  # 1 is top
    self.fixtures = []
    self.username = username
    self.password = password
    self.location = location

  def showDetails(self):
    pass

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
