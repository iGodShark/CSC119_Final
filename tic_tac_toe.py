import random

class Board:
  # init board class
  def __init__(self):
    self.board_list = ['1','2','3','4','5','6','7','8','9']
  
  # display the board - available spaces / spaces that are already taken
  def display_board(self):
    print(' {} {}|{} {} {}|{} {}{}'.format(self.board_list[0],color('blue'),color('reset'),self.board_list[1],color('blue'),color('reset'),self.board_list[2],color('reset')))
    print('{}---+---+---{}'.format(color('blue'),color('reset')))
    print(' {} {}|{} {} {}|{} {}{}'.format(self.board_list[3],color('blue'),color('reset'),self.board_list[4],color('blue'),color('reset'),self.board_list[5],color('reset')))
    print('{}---+---+---{}'.format(color('blue'),color('reset')))
    print(' {} {}|{} {} {}|{} {}{}'.format(self.board_list[6],color('blue'),color('reset'),self.board_list[7],color('blue'),color('reset'),self.board_list[8],color('reset')))

  # if it's a player's turn then get a valid space from the player - returns index
  def get_valid_player_space(self):
    choice = input(color('aqua')+"Choose a space: "+color('reset'))
    while choice not in self.board_list or choice in ['X','O',color('green')+'X'+color('reset'),color('red')+'O'+color('reset')]:
      choice = input(color('aqua')+"Invalid choice, try again: "+color('reset'))
    
    return int(choice) - 1
  
  # if it's a computer's turn then get a random available space - returns index
  def get_valid_computer_space(self):
    choice = str(random.randint(1,9))
    while choice not in self.board_list:
      choice = str(random.randint(1,9))
    
    # also print computer choice to player
    print(color('purple')+"I choose spot "+choice+color('reset'))
    return int(choice) - 1
  
  # check if the player passed in this function has won, returns boolean
  def check_for_winner(self, current_player):
    threes = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for three in threes:
      if self.board_list[three[0]] == self.board_list[three[1]] == self.board_list[three[2]] == current_player["marker"]:
        return True
    return False
  
  # check's if the game has ended in a tie
  def check_for_tie(self):
    for spot in self.board_list:
      if spot in '123456789':
        return False
    return True

# add color to game
def color(c):
  if c == 'reset':
    return '\033[0m'
  colors = {'red':31,'green':32,'orange':33,'blue':34,'purple':35,'aqua':36}
  return '\033[1;{}m'.format(colors[c])

# switch player turns
def switch_player(current_player):
  if current_player["type"] == "player":
    return {"type":"computer","marker":color('red')+"O"+color('reset')}
  else:
    return {"type":"player","marker":color('green')+"X"+color('reset')}

# play the game! will return winner as 'player', 'computer', or a 'tie'
def play_game():
  # initialize the board and current player
  board = Board()
  current_player = {"type":"player","marker":color('green')+"X"+color('reset')}
  while True:
    # while game hasn't ended, display board
    board.display_board()
    # get player/computer choice
    if current_player['type'] == 'player':
      choice_index = board.get_valid_player_space()
    else:
      choice_index = board.get_valid_computer_space()
    # mark the player/computer choice on the board
    board.board_list[choice_index] = current_player["marker"]
    # check for a winner
    if board.check_for_winner(current_player):
      board.display_board()
      return current_player['type']
      break
    # check for a tie
    if board.check_for_tie():
      board.display_board()
      return "tie"
      break
    #switch the player
    current_player = switch_player(current_player)