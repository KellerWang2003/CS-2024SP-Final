import js as p5
import math

print('Assignment #7 (Final Project)')

start_font = p5.loadFont('font.ttf')
map = p5.loadImage('map.jpg')
character_img = p5.loadImage('character.PNG')
enemy_img = p5.loadImage('enemy.png')
sprint_icon = p5.loadImage('sprint_icon.png')
program_state = 'START'

global_wPressed = False
global_aPressed = False
global_sPressed = False
global_dPressed = False
global_mouse_pressed = False

class Hitbox():
  def __init__(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    
  def draw(self):
    p5.fill('rgba(255, 255, 255, 0.5)')
    p5.rect(self.x, self.y, self.width, self.height)

  def collision(self, other_hitbox):
    return (self.x < other_hitbox.x + other_hitbox.width/2) and (self.x > other_hitbox.x - other_hitbox.width/2) and (self.y < other_hitbox.y + other_hitbox.height/2) and (self.y > other_hitbox.y - other_hitbox.height/2)

class Map_hitbox(Hitbox):
  def __init__(self, x, y, width, height):
    self.x = x + map_movement.x
    self.y = y + map_movement.y
    self.width = width
    self.height = height
    
  def draw(self):
    p5.fill('rgba(255, 255, 255, 0.5)')
    p5.rect(self.x - map_movement.x, self.y - map_movement.y, self.width, self.height)

class EnemyBullet_hitbox(Hitbox):
  def __init__(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height

  def draw(self):
    p5.fill('rgba(255, 255, 255, 0.5)')
    # i = 0
    # while(i < len(enemy_bullet_list)):
    #   p5.push()
    #   p5.rotate(enemy_bullet_list[i].angle_list[i])
    #   self.x += 2.5
    #   p5.pop()
    #   i += 1
    p5.rect(self.x, self.y, self.width, self.height)

    



class Movement():
  speed_x = 0.5
  speed_y = 0.5
  wPressed = False
  aPressed = False
  sPressed = False
  dPressed = False
  shiftPressed = False
  sprinting = False
  sprint_timer = 0
  sprint_cd = False
  sprint_cd_timer = 0

  def __init__(self, x, y):
    self.x = x
    self.y = y

  def characterImg_reversed(self):
    p5.scale(-1, 1)
    p5.image(character_img, -self.x + 4, self.y, 20, 35)
    p5.rect(-(self.x + 4) + 4, self.y + 23, 15, 10)
    p5.rect(-(self.x - 4), self.y + 33, 15, 10)

  def characterImg(self):
    p5.image(character_img, self.x, self.y, 20, 35)
    p5.rect(self.x - 4, self.y + 23, 15, 10)
    p5.rect(self.x - 8, self.y + 33, 15, 10)

  def draw_character(self):
    p5.push()

    # p5.noStroke()
    # p5.fill(100, 50, 0)
    # p5.ellipse(self.x, self.y, 20, 20)
    # p5.fill(255, 50, 50)
    # p5.ellipse(self.x, self.y, 5, 5)
    p5.noStroke()
    p5.fill('rgba(100, 75, 25, 0.5)')
    
    if global_aPressed:
      if global_mouse_pressed and p5.mouseX > character_movement.x:
        self.characterImg()
      else:
        self.characterImg_reversed()
    elif global_dPressed:
      if global_mouse_pressed and p5.mouseX < character_movement.x:
        self.characterImg_reversed()
      else:
        self.characterImg()
    else:
      self.characterImg()

    


    # character_hitbox.draw()

    p5.pop()

  def position_x(self):
    if (self.aPressed == True):
      self.x -= self.speed_x
      character_hitbox.x -= self.speed_x

    if (self.dPressed == True):
      self.x += self.speed_x
      character_hitbox.x += self.speed_x

  def position_y(self):
    if (self.wPressed == True):
      self.y -= self.speed_y
      character_hitbox.y -= self.speed_y

    if (self.sPressed == True):
      self.y += self.speed_y
      character_hitbox.y += self.speed_y

  def sprint(self):
    p5.push()
    p5.fill(150)
    p5.noStroke()
    p5.rect(30, 30, 30, 30, 10)
    p5.image(sprint_icon, 30, 30, 30, 30)
    p5.pop()
    #sprinting starts
    if (self.shiftPressed == True):
      if (self.sprinting == False) and (self.sprint_cd == False):
        self.sprinting = True
        self.speed_x = 2
        self.speed_y = 2
        self.sprint_timer = p5.millis()

    #limits sprinting to 1 second
    if (self.sprinting == True) and (p5.millis() - self.sprint_timer >= 1000):
      self.sprinting = False
      self.speed_x = 0.5
      self.speed_y = 0.5
      self.shiftPressed = False
      #starts cd
      self.sprint_cd = True
      self.sprint_cd_timer = p5.millis()

    #limits cd to x seconds
    if (self.sprint_cd == True):
      p5.fill('rgba(0, 0, 0, 0.5)')
      p5.rect(30, 30, 30, 30, 5)
      self.shiftPressed = False #prevents trigger sprinting when in cd
      if (p5.millis() - self.sprint_cd_timer >= 3000):
        self.sprint_cd = False

  def draw(self):
    self.sprint()
    self.draw_character()


class Map_movement(Movement):
  def draw_map(self):
    p5.push()
    p5.translate(self.x, self.y)
    p5.image(map, 0, 0, 1000, 1000)

    # hitbox
    # k = 0
    # while(k < len(map_hitbox_list)):
    #   map_hitbox_list[k].draw()
    #   k += 1

    # #enemy bullet hitbox
    # l = 0
    # while l < len(enemy_bullet_hitbox_list):
    #   enemy_bullet_hitbox_list[l].draw()
    #   l += 1
    
    
    #as if the bullet is part of the map
    i = 0
    while(i < len(player_bullet_list)):
      player_bullet_list[i].draw()
      i += 1

    #drawing enemy
    j = 0
    while(j < len(enemy_list)):
      enemy_list[j].draw()
      j += 1
    
    p5.pop()


  def position_x(self):
    if (self.aPressed == True):
      if self.x < 400:
        self.x += self.speed_x
        i = 0
        while i < len(map_hitbox_list):
          map_hitbox_list[i].x += self.speed_x
          i += 1
      else:
        self.x = 400

    if (self.dPressed == True):
      if self.x > 100:
        self.x -= self.speed_x
        i = 0
        while i < len(map_hitbox_list):
          map_hitbox_list[i].x -= self.speed_x
          i += 1
      else:
        self.x = 100

  def position_y(self):
    if (self.wPressed == True):
      if self.y < 400:
        self.y += self.speed_y
        i = 0
        while i < len(map_hitbox_list):
          map_hitbox_list[i].y += self.speed_y
          i += 1
      else:
        self.y = 400

    if (self.sPressed == True):
      if self.y > -100:
        self.y -= self.speed_y
        i = 0
        while i < len(map_hitbox_list):
          map_hitbox_list[i].y -= self.speed_y
          i += 1
      else:
        self.y = -100

  def draw(self):
    self.sprint()
    self.draw_map()
    
character_movement = Movement(250, 150)
character_hitbox = Hitbox(character_movement.x, character_movement.y, 10, 10)
map_movement = Map_movement(250, 150)

map_hitbox_list = []

hitbox1 = Map_hitbox(-170, 60, 50, 100)
map_hitbox_list.append(hitbox1)

hitbox2 = Map_hitbox(-220, 110, 100, 50)
map_hitbox_list.append(hitbox2)

hitbox3 = Map_hitbox(170, 30, 100, 170)
map_hitbox_list.append(hitbox3)

hitbox4 = Map_hitbox(95, 40, 50, 90)
map_hitbox_list.append(hitbox4)

hitbox5 = Map_hitbox(55, -120, 90, 20)
map_hitbox_list.append(hitbox5)

hitbox6 = Map_hitbox(-200, -200, 200, 200)
map_hitbox_list.append(hitbox6)

hitbox7 = Map_hitbox(200, 330, 200, 200)
map_hitbox_list.append(hitbox7)

hitbox8 = Map_hitbox(240, -220, 200, 200)
map_hitbox_list.append(hitbox8)

hitbox9 = Map_hitbox(90, -330, 100, 200)
map_hitbox_list.append(hitbox9)

hitbox10 = Map_hitbox(70, -250, 100, 50)
map_hitbox_list.append(hitbox10)


class Aim():
  bullet_speed = 5
  bullet_x = 0
  bullet_y = 0
  character_x = 0
  character_y = 0
  bullet_initial_x = 0
  bullet_initial_y = 0
  angle = 0

  def draw_bullet(self):
    p5.push()
    p5.translate(self.bullet_x, self.bullet_y)
    p5.stroke(255, 150, 50)
    p5.fill(255)
    p5.rect(0, 0, 10, 3)
    p5.triangle(5, 1.5, 5, -1.5, 8, 0)
    p5.fill(255, 100, 100)
    p5.triangle(-6, 1.5, -6, -1.5, -15, 0)
    p5.pop()

  def angle_to_player(self):
    self.bullet_initial_x = p5.mouseX
    self.bullet_initial_y = p5.mouseY
    #calculates angle from curser to character
    diff_x = self.bullet_initial_x - character_movement.x
    diff_y = self.bullet_initial_y - character_movement.y
    self.angle = math.atan2(diff_y, diff_x)
    #need a record of translate value here because this code only needs to run once everytime a bullet if fired
    self.character_x = character_movement.x - map_movement.x #to account for the translate in map_movement
    self.character_y = character_movement.y - map_movement.y

  def animate_bullet(self):
    p5.push()
    p5.translate(self.character_x, self.character_y)
    p5.rotate(self.angle)
    self.draw_bullet()
    self.bullet_x += self.bullet_speed
    p5.pop()

    #remove bullet after x greater than 1000
    if self.bullet_x > 1000:
      i = 0
      while i < len(player_bullet_list):
        player_bullet_list.pop(0)
        i += 1

  def draw(self):
    self.animate_bullet()

player_bullet_list = []
enemy_bullet_list = []
enemy_bullet_hitbox_list = []

class Enemy():
  bullet_timer = 0
  action_executed = False
  angle_list = [0, 0, 0, 0]
  
  def __init__(self, x, y):
    self.enemy_x = x
    self.enemy_y = y
    

  def draw(self):
    p5.push()
    p5.scale(-1, 1)
    p5.image(enemy_img, -self.enemy_x, self.enemy_y, 15, 28)
    p5.pop()

    distance_to_character = p5.dist(character_movement.x - map_movement.x, character_movement.y - map_movement.y, self.enemy_x, self.enemy_y)

    j = 0
    while j < len(enemy_list):
      if distance_to_character <= 200:
        #automaticlly fires bullet every 1 second
        if(p5.millis() >= self.bullet_timer + 4000): 
          enemy_bullet = Enemy_aim()
          enemy_bullet.angle_to_player()
          enemy_bullet_list.append(enemy_bullet)
          enemy_bullet_hitbox = EnemyBullet_hitbox(enemy_list[j].enemy_x, enemy_list[j].enemy_y, 100, 3)
          enemy_bullet_hitbox_list.append(enemy_bullet_hitbox)
          self.bullet_timer = p5.millis()
      j += 1
      
    i = 0
    while(i < len(enemy_bullet_list)):
      enemy_bullet_list[i].draw()
      i += 1
    
enemy_list = []

enemy1 = Enemy(135, -190)
enemy_list.append(enemy1)

enemy2 = Enemy(110, -210)
enemy_list.append(enemy2)

# enemy3 = Enemy(50, 50)
# enemy_list.append(enemy3)


class Enemy_aim(Aim):
  angle_list = [0, 0, 0, 0, 0 ,0]
  bullet_speed = 5 / (len(enemy_list))
  within_range = False
  distance2character = 0
  diff_x = 0
  diff_y = 0

  def draw_bullet(self):
    p5.push()
    p5.translate(self.bullet_x, self.bullet_y)
    p5.stroke(200, 100, 50)
    p5.fill(255)
    p5.rect(0, 0, 10, 3)
    p5.triangle(5, 1.5, 5, -1.5, 8, 0)
    p5.fill(255, 100, 100)
    p5.triangle(-6, 1.5, -6, -1.5, -15, 0)
    p5.pop()

  def angle_to_player(self):
    i = 0
    while(i < len(enemy_list)):
      self.bullet_initial_x = character_movement.x - map_movement.x
      self.bullet_initial_y = character_movement.y - map_movement.y
      #calculates angle from curser to character
      self.diff_x = self.bullet_initial_x - enemy_list[i].enemy_x
      self.diff_y = self.bullet_initial_y - enemy_list[i].enemy_y
      self.angle = math.atan2(self.diff_y, self.diff_x)
      self.angle_list[i] = self.angle

      # self.distance2character = p5.dist(0, 0, self.diff_x, self.diff_y)
      # if self.distance2character <= 300:
      #   self.within_range = True
      # else:
      #   self.within_range = False
      i += 1
    
    #need a record of translate value here because this code only needs to run once everytime a bullet if fired
    self.character_x = character_movement.x - map_movement.x #to account for the translate in map_movement
    self.character_y = character_movement.y - map_movement.y

 

  def animate_bullet(self):
    i = 0
    while(i < len(enemy_list)):
      p5.push()
      p5.translate(enemy_list[i].enemy_x, enemy_list[i].enemy_y)
      p5.rotate(self.angle_list[i])
      self.draw_bullet()
      p5.pop()
      i += 1
      
    self.bullet_x += self.bullet_speed

    #remove bullet after x greater than 1000
    if self.bullet_x > 1000:
      j = 0
      while j < len(enemy_bullet_list):
        enemy_bullet_list.pop(0)
        j += 1

  def update_hitbox(self):
    # Update hitbox position to match bullet position
    pass

  
  def draw(self):
    if program_state == 'PLAY':
      self.animate_bullet()
      self.update_hitbox()




def draw_start_button():
  p5.push()
  p5.translate(p5.width/2, p5.height/2 + 60)
  if (p5.mouseX >= 200) and (p5.mouseX <= 300) and (p5.mouseY >= 185) and (p5.mouseY <= 235):
    p5.fill('rgba(255, 255, 255, 0.8)')
  else:
    p5.fill('rgba(255, 255, 255, 0.5)')
  p5.strokeWeight(2)
  p5.stroke(50, 50, 50)
  p5.rect(0, 0, 100, 50, 10)
  p5.fill(0)
  p5.noStroke()
  p5.textSize(30)
  p5.textAlign(p5.CENTER)
  p5.textFont(start_font)
  p5.text('Start', 0, 10)
  p5.pop()

def hitbox_stop_x():
  #detects hitbox collision and stops movement
  i = 0
  while i < len(map_hitbox_list):
    if global_aPressed and character_hitbox.collision(map_hitbox_list[i]) and character_hitbox.x >= map_hitbox_list[i].x:
      character_movement.x += character_movement.speed_x
      character_hitbox.x += character_movement.speed_x
      if global_dPressed:
        character_movement.x = map_hitbox_list[i].x + map_hitbox_list[i].width/2
        character_hitbox.x = map_hitbox_list[i].x + map_hitbox_list[i].width/2
    elif global_dPressed and character_hitbox.collision(map_hitbox_list[i]) and character_hitbox.x <= map_hitbox_list[i].x:
      character_movement.x -= character_movement.speed_x
      character_hitbox.x -= character_movement.speed_x
      if global_aPressed:
        character_movement.x = map_hitbox_list[i].x - map_hitbox_list[i].width/2
        character_hitbox.x = map_hitbox_list[i].x - map_hitbox_list[i].width/2
    i += 1

def hitbox_stop_y():
  i = 0
  while i < len(map_hitbox_list):
    if global_wPressed and character_hitbox.collision(map_hitbox_list[i]) and character_hitbox.y >= map_hitbox_list[i].y:
      character_movement.y += character_movement.speed_y
      character_hitbox.y += character_movement.speed_y
      if global_sPressed:
        character_movement.y = map_hitbox_list[i].y + map_hitbox_list[i].height/2
        character_hitbox.y = map_hitbox_list[i].y + map_hitbox_list[i].height/2
    elif global_sPressed and character_hitbox.collision(map_hitbox_list[i]) and character_hitbox.y <= map_hitbox_list[i].y:
      character_movement.y -= character_movement.speed_y
      character_hitbox.y -= character_movement.speed_y
      if global_wPressed:
        character_movement.y = map_hitbox_list[i].y - map_hitbox_list[i].height/2
        character_hitbox.y = map_hitbox_list[i].y - map_hitbox_list[i].height/2
    i += 1

#logic for map and character position interaction
def character_map_movement_draw():
  global global_aPressed, global_dPressed, global_sPressed, global_wPressed
  global program_state

  #draw map & character
  map_movement.draw()
  character_movement.draw()
  
  if program_state == 'START':
    draw_start_button()
  else:
    #reset which to move, had to divide x and y movement
    if (character_movement.x < 150) or (character_movement.x > 350):
      hitbox_stop_x()
      map_movement.position_x()
      if (global_dPressed) and (character_movement.x < 150):
        character_movement.x = 150
      if (global_aPressed) and (character_movement.x > 350):
        character_movement.x = 350
    else:
      #detects hitbox collision and stops movement
      hitbox_stop_x()
      character_movement.position_x()

  
    if (character_movement.y < 130) or (character_movement.y > 250):
      hitbox_stop_y()
      map_movement.position_y()
      if (global_sPressed) and (character_movement.y < 130):
        character_movement.y = 130
      if (global_wPressed) and (character_movement.y > 250):
        character_movement.y = 250
    else:
      #detects hitbox collision and stops movement
      hitbox_stop_y()
      character_movement.position_y()
        


  #box for character border
  # p5.push()
  # p5.noFill()
  # p5.rect(p5.width/2, p5.height/2 + 40, 200, 120)
  # p5.pop()


def draw_aim():
  p5.push()
  p5.noFill()
  p5.strokeWeight(2)
  p5.translate(p5.mouseX, p5.mouseY)
  p5.ellipse(0, 0, 10)
  p5.noStroke()
  p5.fill(0)
  p5.rect(5, 0, 7, 2)
  p5.rect(-5, 0, 7, 2)
  p5.rect(0, 5, 2, 7)
  p5.rect(0, -5, 2, 7)
  p5.pop()


def setup():
  p5.createCanvas(500, 300)
  p5.rectMode(p5.CENTER)
  p5.imageMode(p5.CENTER)

def draw():
  p5.background(255)   
  p5.fill(0)

  character_map_movement_draw()
  draw_aim()


  # cursor_xy = (int(p5.mouseX), int(p5.mouseY))
  # p5.text(cursor_xy, 10, 20)



# event function below need to be included,
# even if they don't do anything

def keyPressed(event):
  #print('keyPressed.. ' + str(p5.key))
  global global_aPressed, global_dPressed, global_sPressed, global_wPressed
  
  if p5.key == 'a' or p5.key == 'A':
    global_aPressed = True
    character_movement.aPressed = True
    map_movement.aPressed = True
  elif p5.key == 'd' or p5.key == 'D':
    global_dPressed = True
    character_movement.dPressed = True
    map_movement.dPressed = True
  elif p5.key == 'w' or p5.key == 'W':
    global_wPressed = True
    character_movement.wPressed = True
    map_movement.wPressed = True
  elif p5.key == 's' or p5.key == 'S':
    global_sPressed = True
    character_movement.sPressed = True
    map_movement.sPressed = True
    
  if (p5.keyCode == p5.SHIFT):
    character_movement.shiftPressed = True
    map_movement.shiftPressed = True
  

def keyReleased(event):
  #print('keyReleased.. ' + str(p5.key))
  global global_aPressed, global_dPressed, global_sPressed, global_wPressed
  
  if p5.key == 'a' or p5.key == 'A':
    global_aPressed = False
    character_movement.aPressed = False
    map_movement.aPressed = False
  elif p5.key == 'd' or p5.key == 'D':
    global_dPressed = False
    character_movement.dPressed = False
    map_movement.dPressed = False
  elif p5.key == 'w' or p5.key == 'W':
    global_wPressed = False
    character_movement.wPressed = False
    map_movement.wPressed = False
  elif p5.key == 's' or p5.key == 'S':
    global_sPressed = False
    character_movement.sPressed = False
    map_movement.sPressed = False

def mousePressed(event):
  global program_state, global_mouse_pressed
  
  #print('mousePressed..')
  if program_state == 'PLAY':
    aim = Aim()
    aim.angle_to_player()
    player_bullet_list.append(aim)

  if program_state == 'START':
    if (p5.mouseX >= 200) and (p5.mouseX <= 300) and (p5.mouseY >= 185) and (p5.mouseY <= 235):
      program_state = 'PLAY'

  global_mouse_pressed = True

  

def mouseReleased(event):
  #print('mouseReleased..')
  global global_mouse_pressed

  global_mouse_pressed = False


  
