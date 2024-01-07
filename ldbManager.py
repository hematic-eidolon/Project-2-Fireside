import json

class Leaderboard:
  def __init__(self):
    self.players = self.read_players()

  def read_players(self):
    with open('players.json', 'r') as f:
      player_info = json.load(f)
      sorted_players = dict(sorted(player_info.items(), key=lambda item: item[1]['position']))
      # Sorts list by item[x] (change x depending on where position is)
      return sorted_players

  def add_players(self):
    with open('leaderboard.json', 'w') as f:
      json.dump(self.players, f, indent=2)
      # Writes list to json file