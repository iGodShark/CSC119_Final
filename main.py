import random
import tic_tac_toe

# oepn some files
item_infos_file = open('items.txt')
item_infos = [line.strip() for line in item_infos_file.readlines()]
room_directions_file = open('room_directions.txt')
room_directions = [line.strip() for line in room_directions_file.readlines()]
enemies_file = open('enemies.txt')
enemies = [line.strip() for line in enemies_file.readlines()]
extra_descriptions_file = open('extra_room_descriptions.txt')
extra_descriptions = [line.strip() for line in extra_descriptions_file.readlines()]

class Room:
  # init a room class
  def __init__(self, x, y, directions, extra_description=None, items=[]):
    self.x = x
    self.y = y
    self.directions = directions
    self.extra_description = extra_description
    self.items = items

  # show the room descriptions
  def show_description(self):
    # check if night vision goggles are in player inventory
    if player.has_night_vision():
      print(color('aqua'),end='') # get color
      # print more detailed description
      short_long = {'n':'North','e':'East','s':'South','w':'West'}
      if len(self.directions) == 1:
        print("You've reached a dead end.")
      elif self.directions == ['n','s'] or self.directions == ['e','w']:
        print("You're in a hallway heading {} and {}.".format(short_long[self.directions[0]],short_long[self.directions[1]]))
      elif len(self.directions) == 2:
        print("You've reached a corner which goes {} and {}.".format(short_long[self.directions[0]],short_long[self.directions[1]]))
      elif len(self.directions) == 3:
        print("You've reached a fork in your path, you can go {}, {}, and {}.".format(short_long[self.directions[0]],short_long[self.directions[1]],short_long[self.directions[2]]))
      else:
        print("You're in a room that can go every direction.")
      print(color('reset'),end='') # reset color
      # print any items that might be on the ground
      if self.items != []:
        print(color('blue'),end='')
        for item in self.items:
          print(item.ground_description)
        print(color('reset'),end='')
      # if room has extra description, also print it
      if self.extra_description != None:
        print(color('purple')+self.extra_description+color('reset'))
    # if player doesn't have night vision:
    else:
      print(color('aqua')+"You're in a dark room."+color('reset'))
      # exception: print night vision goggles are on the ground when played doesn't have them
      for item in self.items:
        if item.name == "Night Vision Goggles":
          print(color('blue')+item.ground_description+color('reset'))
          break

class Player:
  # init the player class
  def __init__(self, x, y, attack, health, defense, inventory=[]):
    self.x = x
    self.y = y
    self.attack = attack
    self.health = health
    self.defense = defense
    self.inventory = inventory
  
  # if player tries to eat something
  def eat(self, player_input):
    # first get item that player wants to eat
    for item in self.inventory:
      if item.name.lower() in player_input:
        if isinstance(item,Food):
          # if item is food, then eat it.
          item.eat()
        else:
          # if item isn't food:
          print(color('red')+"You can't eat that, silly!"+color('reset'))
        break
    # if player is trying to eat item that's not in his inventory
    else:
      print(color('red')+"You don't even have that in your inventory!"+color('reset'))
    
  # if player tries to read the diary
  def read_diary(self):
    for item in self.inventory:
      if item.name == "Diary":
        # read diary if player has it
        item.read_diary()
        break
    else:
      # if player doesn't have diary:
      print(color('red')+"You don't have a diary."+color('reset'))
  
  # check if player has night vision (True/False)
  def has_night_vision(self):
    for item in self.inventory:
      if item.name == "Night Vision Goggles":
        return True
    return False
  
  # display player inventory
  def display_inventory(self):
    if self.inventory != []:
      print(color('orange'),"You're carrying:")
      for item in self.inventory:
        print("   -",item.name)
      print(color('reset'),end='')
    else:
      print(color('red')+"You aren't carrying anything."+color('reset'))
  
  # display player statistics
  def display_stats(self):
    print(color('orange'),end='')
    print("   - Attack:",self.attack)
    print("   - Health:",round(self.health*100)/100)
    print("   - Defense:",self.defense)
    print(color('reset'),end='')
 
  # see if player already has certain type of armor
  def has_armor_type(self, armor_type):
    for item in self.inventory:
      if isinstance(item,Armor):
        if item.armor_type == armor_type:
          return True
    return False
  
  # count how many weapons player is holding
  def weapon_count(self):
    weapons = 0
    for item in self.inventory:
      if isinstance(item,Weapon):
        weapons += 1
    return weapons
  
  # count how many food items the player is holding
  def food_count(self):
    foods = 0
    for item in self.inventory:
      if isinstance(item,Food):
        foods += 1
    return foods
  
  # check if player has key for the locked door at the end
  def has_key(self):
    for item in self.inventory:
      if item.name == "Key":
        return True
    return False

class Enemy:
  # init an enemy class
  def __init__(self, x, y, attack, health, defense, name):
    self.x = x
    self.y = y
    self.attack = attack
    self.health = health
    self.defense = defense
    self.name = name

class Item:
  # init an item class
  def __init__(self, name, ground_description):
    self.name = name
    self.ground_description = ground_description
  
  # read special diary, clue
  def read_diary(self):
    if self.name == 'Diary':
      print(color('purple'),"""
      Day 42:
      I've been stuck in this maze for 42 days.
      There's a locked door in the furthest south west room of this maze.
      I assume it's the way out, but I haven't found the key.
      I've been searching, but am on the brink of giving up...
      """,color('reset'))

class Weapon(Item):
  # init weapon, item subclass
  def __init__(self, name, ground_description, attack_increase):
    super().__init__(name, ground_description)
    self.attack_increase = int(attack_increase)

class Armor(Item):
  # init armor, item subclass
  def __init__(self, armor_type, armor_material, ground_description, defense_increase):
    self.name = "{} {}".format(armor_material, armor_type)
    super().__init__(self.name, ground_description)
    self.defense_increase = int(defense_increase)
    self.armor_type = armor_type

class Food(Item):
  # init food, item subclass
  def __init__(self, name, ground_description, health_increase):
    super().__init__(name, ground_description)
    self.health_increase = int(health_increase)
  
  # eat food item - increase player health, remove item from player inventory, and delete item instance
  def eat(self):
    if player.health + self.health_increase <= 20:
      player.health += self.health_increase
      player.inventory.remove(self)
      print("{}{} eaten. ({}+ {} health{}){}".format(color('aqua'),self.name,color('green'),self.health_increase,color('aqua'),color('reset')))
      del self
    # since player max health is 20, if eating item will go over 20, player isn't hungry
    else:
      print(color('red')+"You aren't hungry for",self.name+color('reset'))

def color(c):
  if c == 'reset':
    return '\033[0m'
  colors = {'red':31,'green':32,'orange':33,'blue':34,'purple':35,'aqua':36}
  return '\033[1;{}m'.format(colors[c])

def setup_rooms():
  # setup room matrix / tile map
  global rooms
  rooms = []
  room_index = 0
  for x in range(11):
    rooms.append([])
    for y in range(11):
      # get available directions in the room
      directions = room_directions[room_index].split(",")
      new_room = Room(x,y,directions)
      rooms[x].append(new_room)
      room_index += 1
  # setup the last room outside of map (exit!)
  last_room = Room(0,11,['n','e','s','w'],"You're outside in a bright beautiful garden!")
  rooms[0].append(last_room)

def setup_room_extra_descriptions():
  # get extra descriptions for certain rooms that are necessary to the game
  for description in extra_descriptions:
    x = int(description.split("-")[0])
    y = int(description.split("-")[1])
    description = description.split("-")[2]
    # add description to the certain room
    rooms[x][y].extra_description = description

def setup_items():
  # setup items
  # creates item class instance and sets it to the corresponding room's 'items' list
  for item in item_infos:
    item_info = item.split(",")
    # get item room coordinates
    x = int(item_info[0])
    y = int(item_info[1])
    # create certain item subclass and set it to the itemss list of the room
    if item_info[2] == "Food":
      rooms[x][y].items = [Food(item_info[3],item_info[4],item_info[5])]
    elif item_info[2] == "Weapon":
      rooms[x][y].items = [Weapon(item_info[3],item_info[4],item_info[5])]
    elif item_info[2] == "Armor":
      rooms[x][y].items = [Armor(item_info[3],item_info[4],item_info[5],item_info[6])]
    # other items that aren't certain subclasses but play a specific role in the storyline
    else:
      rooms[x][y].items = [Item(item_info[2],item_info[3])]

def setup_enemies():
  # setup enemies
  global enemy_list
  enemy_list = []
  for enemy in enemies:
    enemy_info = enemy.split(",")
    # get enemy coordinates
    x = int(enemy_info[0])
    y = int(enemy_info[1])
    name = enemy_info[2]
    # setup enemy stats
    if name == "Goblin":
      attack = random.randint(1,4)
      health = random.randint(2,5)
      defense = random.randint(2,4)
    elif name == "Troll":
      attack = random.randint(3,7)
      health = random.randint(4,8)
      defense = random.randint(4,7)
    elif name == "Cyclops":
      attack = random.randint(6,10)
      health = random.randint(7,11)
      defense = random.randint(7,10)
    else:
      attack = random.randint(9,13)
      health = random.randint(10,14)
      defense = random.randint(10,13)
    # add enemy to enemy list
    enemy_list.append(Enemy(x,y,attack,health,defense,name))

def setup():
  # setup game
  setup_rooms()
  setup_room_extra_descriptions()
  setup_items()
  setup_enemies()
  # also setup player with (x,y,attack,health,defense)
  global player
  player = Player(10,0,1,15,0)

def move_keyword(player_input):
  # returns if player entered a 'move keyword'
  return player_input in ('n','go n','north','go north','e','go e','east','go east','s','go s','south','go south','w','go w','west','go west')

def input_to_direction(player_input):
  # returns the player input into a direction the program can work with ('n','e','s','w')
  input_to_direction_dict = {'n':('n','go n','north','go north'),'e':('e','go e','east','go east'),'s':('s','go s','south','go south'),'w':('w','go w','west','go west')}
  for key, value in input_to_direction_dict.items():
    if player_input in value:
      return key

def move(direction, current_room):
  # move the player in the current direction if it's an available direction in the room.
  if direction in current_room.directions:
    # if direction is available, then move player
    if direction == 'n':
      player.y -= 1
    elif direction == 'e':
      player.x += 1
    elif direction == 's':
      player.y += 1
    else:
      player.x -= 1
    # show new room description
    rooms[player.x][player.y].show_description()
  # if the direction isn't available, player has ran into a wall.
  else:
    print(color('red')+"You ran into a wall."+color('reset'))
    if player.defense < 5:
      # if player has a low defense and runs into a wall, there's a 33% chance of stubbing the toe and losing .5 health
      if random.randint(1,3) == 1:
        print("{}You stubbed your toe. ({}- 0.5 health{}){}".format(color('aqua'),color('red'),color('aqua'),color('reset')))
        player.health -= 0.5

def take_item_keyword(player_input):
  # returns if player entered a 'take item' keyword
  take_item_keywords = ["take","pick it up","pick up","grab","get"]
  for keyword in take_item_keywords:
    if keyword in player_input:
      return True
  return False

def take_item(player_input, current_room):
  # attempt to take an item in the current room
  if current_room.items != []:
    # first check if the room isn't empty
    for item in current_room.items:
      if item.name.lower() in player_input or item.name == "Night Vision Goggles":
        # take item if item in room is what player asked to take
        if isinstance(item,Armor):
          # check if item is armor
          for type in ["Helmet","Chestplate","Leggings","Boots"]:
            # check if player has the armor type they're trying to take
            if item.armor_type == type:
              if player.has_armor_type(type):
                # if player already has armor type, they can't take
                print("{}You already have a {}, if you want to pick this one up you must drop your current one.{}".format(color('red'),type.lower(),color('reset')))
              else:
                # otherwise, take the item and increase player defense
                player.inventory.append(item)
                player.defense += item.defense_increase
                current_room.items.remove(item)
                print('{}{} taken. ({}+ {} defense{}){}'.format(color('aqua'),item.name,color('green'),item.defense_increase,color('aqua'),color('reset')))
              break
        elif isinstance(item,Weapon):
          # if item is a weapon, first make sure player doesn't already have 2 weapons (max they can hold)
          if player.weapon_count() >= 2:
            # if they already have 2 weapons:
            print("{}You have too many weapons, you must drop one to pick this one up.{}".format(color('red'),color('reset')))
          else:
            # if player doesn't have 2 weapons, take weapon and increase attack
            player.inventory.append(item)
            player.attack += item.attack_increase
            current_room.items.remove(item)
            print('{}{} taken. ({}+ {} attack{}){}'.format(color('aqua'),item.name,color('green'),item.attack_increase,color('aqua'),color('reset')))
        elif isinstance(item,Food):
          # if item is food, make sure player doesn't already have 3 foods (max they can carry)
          if player.food_count() >= 3:
            # if they already have 3 foods:
            print("{}You're carrying too much food, you must eat or drop some food to take this food.{}".format(color('red'),color('reset')))
          else:
            # if not, take food.
            player.inventory.append(item)
            current_room.items.remove(item)
            print(color('aqua')+item.name,'taken.'+color('reset'))
        else:
          # all other item types are essential to game, no max limit on how many they can hold (only other items are night vision goggles, diary, and key)
          player.inventory.append(item)
          current_room.items.remove(item)
          print(color('aqua')+item.name,'taken.'+color('reset'))
          # once player takes night vision goggles, show room and add a new direction
          if item.name == "Night Vision Goggles":
            current_room.directions.append('s')
            current_room.show_description()
        break
    else:
      # if player input doesn't contain any items in the room:
      print(color('red')+"I don't know what item you're trying to take."+color('reset'))
  else:
    # if room is empty:
    print(color('red')+"There isn't anything you can grab in this room."+color('reset'))

def drop_item_keyword(player_input):
  # return if player entered a 'drop item' keyword
  drop_item_keywords = ["drop","let go","get rid of"]
  for keyword in drop_item_keywords:
    if keyword in player_input:
      return True
  return False

def drop_item(player_input, current_room):
  # drop an item in the room
  if player.inventory != []:
    # first check if player has items to drop
    for item in player.inventory:
      if item.name.lower() in player_input and item.name != "Night Vision Goggles":
        # if player input is an item they have:
        if isinstance(item,Armor):
          # if item is armor type, then make sure to decrease defense
          player.defense -= item.defense_increase
          print('{}{} dropped. ({}- {} defense{}){}'.format(color('aqua'),item.name,color('red'),item.defense_increase,color('aqua'),color('reset')))
        elif isinstance(item,Weapon):
          # if item is weapon type, then make sure to decrease attack
          player.attack -= item.attack_increase
          print('{}{} dropped. ({}- {} attack{}){}'.format(color('aqua'),item.name,color('red'),item.attack_increase,color('aqua'),color('reset')))
        else:
          # if item is food or anything else, just drop it.
          print(color('aqua')+item.name,'dropped.'+color('reset'))
        current_room.items.append(item)
        player.inventory.remove(item)
        break
      elif item.name.lower() in player_input and item.name == "Night Vision Goggles":
        # if player tries to drop night vision goggles (undroppable, almost impossible to beat game without them)
        print(color('red')+"The night vision goggles are too tight around your head and you can't take them off. Perhaps it's a sign that you can't survive without them."+color('reset'))
        break
    else:
      # if none of players items in inventory were in the input:
      print(color('red')+"I don't know what item you're trying to drop."+color('reset'))
  else:
    # if player inventory is empty:
    print(color('red')+"There isn't anything you can drop."+color('reset'))

def fight(enemy, current_room):
  start_health = player.health
  # when player decides to fight enemy: attack until someone runs out of health
  while enemy.health > 0 and player.health > 0:
    enemy.health -= (player.attack * ((20 - enemy.defense)/20))
    player.health -= (enemy.attack * ((20 - player.defense)/20))
  if enemy.health <= 0:
    # if enemy is the one that died, print we killed enemy and remove enemy from enemy_list
    print("{}You killed the {} ({}- {} health{}){}".format(color('aqua'),enemy.name,color('red'),round((start_health - player.health)*100)/100,color('aqua'),color('reset')))
    enemy_list.remove(enemy)
    current_room.extra_description = "There's a dead {} on the ground.".format(enemy.name)

def run(enemy, previous_room):
  # if player decided to run from enemy
  hit = False
  if random.randint(1,2) == 1:
    hit = True
  # 50/50 chance of enemy hitting player when player tries to run back
  if hit:
    # if enemy got a hit, then display stats and decrease player health
    player.health -= (enemy.attack * ((20 - player.defense)/20))
    print("{}The {} got a hit on you. ({}- {} health{}){}".format(color('aqua'),enemy.name,color('red'),round(enemy.attack * ((20 - player.defense)/20)*100)/100,color('aqua'),color('reset')))
  # move player back to coords of previous room and show description.
  player.x = previous_room.x
  player.y = previous_room.y
  previous_room.show_description()

def fight_or_run(player_input,enemy,previous_room,current_room):
  # see if player wantsw to fight or run
  while player_input not in ("fight","run"):
    print(color('orange')+"Do you want to run, or do you want to fight?"+color('reset'))
    player_input = input(color('purple')+"> "+color('reset')).lower().strip()
  if player_input == "fight":
    # if fight, then fight
    fight(enemy,current_room)
  else:
    # otherwise, try to run
    run(enemy,previous_room)

def display_help():
  # help function - prints these commands
  print(color('orange'),"""
  Here are some acceptable commands:
    - go (north, east, south, west)
    - eat (food name)
    - pick up (item name)
    - drop (item name)
    - inventory
    - stats
    - look
  Here are some acceptable commands when you come across an enemy:
    - fight
    - run
  """,color('reset'))

def play_tic_tac_toe(current_room):
  # when player gets to puzzle master and plays tick tack toe.
  print(color('purple')+"You go first, you're X's and I'm O's"+color('reset'))
  winner = tic_tac_toe.play_game()
  # play first game and get winner.
  while winner == 'tie':
    # keep playing games until there's a winner
    print(color('purple')+"Aww a tie, lets try again. You go first, you're X's and I'm O's."+color('reset'))
    winner = tic_tac_toe.play_game()
  if winner == 'player':
    # if player won:
    print(color('purple')+"Nice, you won! Here, take the key."+color('reset'))
    # make player take key, and move to next room
    take_item('take key', current_room)
    move('s', current_room)
    return 'win'
  elif winner == 'computer':
    # if player lost, they die
    print(color('purple')+"Sorry, I must kill you now..."+color('reset'))
    return 'loss'

def get_points(number_of_moves):
  points = 0
  # get points based off of number of moves
  if number_of_moves < 1000:
    points += (1000 - number_of_moves)
  # get points based off of player stats:
  points += (int(player.health * 50))
  points += (player.attack * 63)
  points += (player.defense * 56)
  # get points based off items the player has:
  for item in player.inventory:
    if item.name == "Diary":
      points += 150
    elif item.name == "Night Vision Goggles":
      points += 100
    elif item.name == "Key":
      points += 200
    elif item.name == "Canned Peas":
      points += 25
    elif item.name == "Canned Tuna":
      points += 50
    elif item.name == "Canned Beans":
      points += 100
    elif item.name == "Canned Soup":
      points += 150
  # get points based off enemies left (unkilled):
  enemy_max_points = 1055
  for enemy in enemy_list:
    if enemy.name == "Goblin":
      enemy_max_points -= 35
    elif enemy.name == "Troll":
      enemy_max_points -= 45
    elif enemy.name == "Cyclops":
      enemy_max_points -= 55
    elif enemy.name == "Minotaur":
      enemy_max_points -= 65
  points += enemy_max_points
  # return player's points
  return points

def main():
  # print the intro:
  print(color('blue'),"""
  You wake up naked and cold.
  You can't remember much.
  All you remember is being knocked
  in the head with a baseball bat.
-------------------------------------
  Welcome to the mad maze!
  Good luck getting out!
  """,color('reset'))
  # setup the game
  setup()
  # at beginning, player has not won.
  winner = False
  # set a previous room (for when player tries to run from fight)
  previous_room = rooms[player.x][player.y]
  previous_room.show_description()
  # setup a number of moves to find out how many moves the player took to win.
  number_of_moves = 0
  # start the game loop
  while player.health > 0 and not winner:
    # get current room
    current_room = rooms[player.x][player.y]
    # currently, there is no enemy
    current_enemy = None
    # go through each enemy
    for enemy in enemy_list:
      if enemy.x == player.x and enemy.y == player.y:
        # if enemy coords same as players, then we do have a current enemy
        current_enemy = enemy
        # print the fight or run
        print(color('orange')+"You've came across a",enemy.name)
        print("Do you want to run, or do you want to fight?"+color('reset'))
    # special checks:
    # if player is in puzzle room, then start tic tac toe games
    if player.x == 5 and player.y == 5:
      if play_tic_tac_toe(current_room) == 'loss':
        # if player lost, then break out of loop with 0 health
        player.health = 0
        break
      else:
        # if player won, update current room
        current_room = rooms[player.x][player.y]
    # if player is in portal room, then teleport player to other end of portal.
    if player.x == 8 and player.y == 8:
      player.x = 2
      player.y = 2
      current_room = rooms[player.x][player.y]
      # update the 'extra description'
      current_room.extra_description = "I'm back at the recieving portal!"
      current_room.show_description()
    # if player has just passed the locked door for the first time, update the extra description
    if player.x == 0 and player.y == 10:
      current_room.extra_description = "There's a locked door heading south."
    # now, once we did special checks, get player input
    choice = input(color('purple')+"> "+color('reset')).lower().strip()
    if current_enemy != None:
      # if we're fighting an enemy, only let player fight or run
      fight_or_run(choice,current_enemy,previous_room,current_room)
    else:
      # if no enemy, try all other commands
      # if player is trying to move rooms
      if move_keyword(choice):
        # then try to move player
        move(input_to_direction(choice), current_room)
      # if player is trying to take item
      elif take_item_keyword(choice):
        # then try to take item
        take_item(choice, current_room)
      # if player is trying to drop item
      elif drop_item_keyword(choice):
        # then try to drop item
        drop_item(choice, current_room)
      # if player is trying to eat
      elif "eat" in choice:
        # then try to eat
        player.eat(choice)
      # if player needs help
      elif choice == "help":
        # display help
        display_help()
      # if player wants to check inventory
      elif choice == "inventory":
        # show inventory
        player.display_inventory()
      # if player wants to check stats (health, attack, defense)
      elif choice == "stats":
        # show stats
        player.display_stats()
      # if player is trying to read diary
      elif choice == "read diary":
        # then try to read diary
        player.read_diary()
      # if player wants to see the room
      elif choice == "look":
        # show the description again
        current_room.show_description()
      # if player tries to fight or run while not fighting an enemy:
      elif choice == "fight" or choice == "run":
        print(color('red')+"You can only fight or run when you've encountered an enemy!"+color('reset'))
      # if player tries to quit
      elif choice == "quit":
        player.health = 0
      # if player tries to unlock door at the end
      elif choice == "unlock door":
        # first check is player has key and is in room with locked door
        if player.has_key() and player.x == 0 and player.y == 10:
          # if so, then unlock and allow player to go new direction in room.
          current_room.directions.append('s')
          print(color('green')+"Door unlocked!"+color('reset'))
          current_room.extra_description = "There's an unlocked door heading South... You see light..."
          current_room.show_description()
        # if player doesn't have key but is in the room:
        elif player.x == 0 and player.y == 10:
          print(color('red')+"You don't have the key."+color('reset'))
        # any other case, there isnt even a door nearby
        else:
          print(color('red')+"There's no locked door nearby!"+color('reset'))
      else:
        # any other command, let them know they can try 'help'
        print(color('red')+"I don't understand! Try saying help for some acceptable commands."+color('reset'))
      # set previous room variable to current room incase player has moved and ran into a monster for running
      previous_room = current_room
    # check if player won, they win if their y is at 11, which is out of the map and can only happen if player has unlocked the door and moved south into the new room.
    number_of_moves += 1
    if player.y == 11:
      winner = True
  if player.health <= 0:
    # outside of loop, if loop ended due to player having 0 health:
    print(color("orange")+"Sadly, you lost :( Try playing again though! You might do better!")
    last_choice = input("Do you want a hint for next time?  "+color('reset')).lower().strip()
    while last_choice not in ["yes","no","y","n"]:
      last_choice = input(color('orange')+"Do you want a hint for next time? (Yes or No) "+color('reset')).lower().strip()
    if last_choice in ['yes','y']:
      print(color('aqua')+"When the game starts, you start in the most North East corner of the maze."+color('reset'))
  else:
    # if loop ended because player has won!:
    print(color('green')+"OMG YOU WIN!!! GOOD JOB!! THANKS FOR PLAYING MY GAME!!!!"+color('reset'))
  # get player points:
  points = get_points(number_of_moves)
  # print player's score
  print("{}You achieved a score of {} with a total number of {} moves.{}".format(color('blue'),points,number_of_moves,color('reset')))

# Start the game!
main()