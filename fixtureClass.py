import currencyHandler as _c  # NOQA
import datetime
import json


class Fixture:

  def __init__(self, ID, currencyHandlerRef: _c.currencyHandler, **kwargs):
    self.__ID = ID
    self.__name = kwargs.get("name", "Unnamed Game")
    self.__date = kwargs.get("date", "Date TBC")
    self.__players = kwargs.get("players", "Players TBC")
    self.__entryFee = kwargs.get("entryFee", "£TBC")
    self.__prizeMoney = kwargs.get("prizeMoney", "£TBC")
    self.__currencyRef = currencyHandlerRef

  def __repr__(self) -> str:
    return f"Fixture ID: {self.__ID}, Name: {self.__name}"

  # =============== GETTERS =============== #
  def getID(self) -> int:
    return self.__ID

  def getName(self) -> str:
    return self.__name

  def getDate(self) -> datetime.datetime:
    return self.__date

  def getPlayers(self) -> list:
    return self.__players

  def getFee(self) -> float:
    return self.__entryFee

  def getPrizeMoney(self) -> float:
    return self.__prizeMoney

  # ============== SETTERS ============== #
  def setID(self, ID):
    self.__ID = ID

  def setName(self, name: str):
    self.__name = name

  def setDate(self, date: datetime.datetime):
    self.__date = date

  def setPlayers(self, players: list):
    self.__players = players

  def setFee(self, entryFee: float):
    self.__entryFee = entryFee

  def setPrizeMoney(self, prizeMoney: float):
    self.__prizeMoney = prizeMoney

  # ============== METHODS ================ #
  def getDatePretty(self) -> str:
    return self.__date.strftime("%d/%m/%y")


  # returns the cost for each country by using the reference to the currency handler

  def getCostForCountry(self, country: str):
    if country == "USA":
      return f"${self.__currencyRef.GBPtoUSD(self.__entryFee)}"
    elif country == "AUS":
      return f"${self.__currencyRef.GBPtoAUD(self.__entryFee)}"
    else:
      pass


  # for saving fixtures: serializeMe() returns the required json format.

  def serMe(self):
    return [
      self.__name, 
      self.getDatePretty(), 
      self.__players,
      self.__entryFee,
      self.__prizeMoney,
      self.__ID
    ]


# called to load the JSON file into a fixture list, takes the currency handler as a ref.

def loadFixturesFromJSON(c):
  jsonFixtures = dict(json.load(open("settings.json")))["fixtures"] # NOQA
  fList = []
  for fixture in jsonFixtures:
    # 'test', '01/01/2000', ['abc', 'def', 'ghi'], 1, 2
    entryFee = prizeMoney = 0
    try:
      entryFee = float(fixture[3])
      prizeMoney = float(fixture[4])
    except ValueError:
      pass

    fDate = fixture[1]
    date_list = fDate.split("/")
    try:
      date_list = [int(x) for x in date_list]
      fixtureDate = datetime.datetime(date_list[2], date_list[1],
                                      date_list[0])  # NOQA
      fList.append(
        Fixture(
          fixture[5],
          c,
          name=fixture[0],
          players=fixture[2],
          entryFee=entryFee,
          prizeMoney=prizeMoney,
          date = fixtureDate
        )
      )

    except (ValueError, TypeError):
      pass
  return fList
