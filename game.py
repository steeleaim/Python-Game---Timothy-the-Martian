import random
import pygame
import turtle

pygame.mixer.init()
explosion_sound = pygame.mixer.Sound("explosion.wav")
crash_sound = pygame.mixer.Sound("crash.wav")
laser_sound = pygame.mixer.Sound("laser.wav")  

pygame.mixer.music.load("space.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()


turtle.fd(0)
turtle.speed(0)
turtle.bgpic
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(1)


screen = turtle.Screen()
screen.bgpic("space.gif")
screen.setup(width=600, height=600) 
screen.addshape("enemysship.gif")  
screen.addshape("timothysship.gif") 
screen.addshape("allysship.gif") 
screen.addshape("meteor.gif")



class Game():

    turtle.update()
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "Active"
        self.pen = turtle.Turtle()
        
    def border(self):
        self.pen.speed(0)
        self.pen.color("black")
        self.pen.pensize(5)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range (4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
    
    def show_status(self):
        self.pen.clear()
        self.pen.penup()
        self.pen.goto(-290, 260)
        self.pen.color("white")
        self.pen.write(f"Score: {self.score}", font=("Courier New", 16, "bold"))

game = Game()

game.border()

game.show_status()

class Ships(turtle.Turtle):
    def __init__(self, shipshape, color, existing_ships=None, startx=None, starty=None, min_distance=50):
        turtle.Turtle.__init__(self, shape = shipshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.shapesize(stretch_wid=2, stretch_len=2)
        self.fd(0)
        self.move_speed = 1

        if existing_ships is None:
            existing_ships = []

        while True:
            if startx is None:
                startx = random.randint(-300, 300)
            if starty is None:
                starty = random.randint(-300, 300)

            if not self.is_colliding(startx, starty, existing_ships, min_distance):
                break
        
        self.goto(startx, starty)
    
    def is_colliding(self, startx, starty, existing_ships, min_distance):

        for ship in existing_ships:
            distance = ((ship.xcor() - startx) ** 2 + (ship.ycor() - starty) **2) ** 0.5
                        

            if distance < min_distance:
                return True
        
        return False

    def move(self):
        self.fd(self.move_speed)

        if self.xcor() > 280:
            self.setx(280)
            self.rt(random.randint(50, 180)) 
        if self.xcor() < -280:
            self.setx(-280)
            self.rt(random.randint(50, 180)) 
        if self.ycor() > 280:
            self.sety(280)
            self.rt(random.randint(50, 180)) 
        if self.ycor() < -280:
            self.sety(-280)
            self.rt(random.randint(50, 180)) 
    
    def collision(self, other):
        
    
        distance = self.distance(other)
        if distance < 30: 
            return True
        else:
            return False

class Player(Ships):
    def __init__(self, shipshape, color, existing_ships):
        Ships.__init__(self, shipshape, color, existing_ships=ships_list)
        self.move_speed = 4 
        self.lives = 5

    def turn_left(self):
        self.lt(20)
    def turn_right(self):
        self.rt(20)
    def thrusters(self):
        if self.move_speed < 10:
            self.move_speed += 1
    def reverse_thrusters(self):
        if self.move_speed < 10:
            self.move_speed -= 1


class Enemy(Ships):
    def __init__(self, shipshape, color, existing_ships):
        Ships.__init__(self, shipshape, color, existing_ships=existing_ships)
        self.move_speed = 4
        self.shapesize(stretch_wid = 1, stretch_len = 1)
        self.setheading(random.randint(0,360))
        self.laser = EnemyLaser("triangle", "light green", 0, 0)

    def move_and_attack(self):
        self.move()  # Move the enemy like usual
        if random.randint(1, 100) < 8:  # Random chance to fire laser
            self.laser.fire(self)  # Fire the laser at the player
        self.laser.move()  # Move the enemy's laser


class Meteor(Ships):
    def __init__(self, shipshape, color, existing_ships):
        Ships.__init__(self, shipshape, color, existing_ships=existing_ships)
        self.move_speed = 2
        self.shapesize(stretch_wid = 1, stretch_len = 1)
        self.setheading(random.randint(0,360))

ships_list = []


class Ally(Ships):
    def __init__(self, shipshape, color, existing_ships):
        Ships.__init__(self, shipshape, color, existing_ships=existing_ships)
        self.move_speed = 4
        self.shapesize(stretch_wid = 1, stretch_len = 1)
        self.setheading(random.randint(0,360))
        self.laser = AllyLaser("triangle", "blue", 0, 0)  # Ally's laser

    def move_and_attack(self, enemy_ship):
        self.move()  # Move like usual
        if random.randint(1, 100) < 10:  # Random chance to fire laser
            self.laser.fire(self, enemy_ship)  # Fire the laser at the enemy
        self.laser.move()  # Move the ally's laser
    
    def move(self):
        self.fd(self.move_speed)

        if self.xcor() > 280:
            self.setx(280)
            self.lt(random.randint(50, 180)) 
        if self.xcor() < -280:
            self.setx(-280)
            self.lt(random.randint(50, 180)) 
        if self.ycor() > 280:
            self.sety(280)
            self.rt(random.randint(50, 180)) 
        if self.ycor() < -280:
            self.sety(-280)
            self.rt(random.randint(50, 180))


class Laser(Ships):
    def __init__(self, shipshape, color, startx, starty):
        Ships.__init__(self, shipshape, color, existing_ships=[], startx=startx, starty=starty)

        self.move_speed = 25
        self.status = "primed"
        self.shapesize(stretch_wid = 0.2, stretch_len = 2, outline=None)
        self.goto(-1000,1000)

    def fire(self):
        if self.status == "primed":
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())     
            self.status = "blasting lasers"
            pygame.mixer.Sound.play(laser_sound)

    def move(self):
        if self.status == "blasting lasers":
            self.fd(self.move_speed)

            if self.xcor() > 300 or self.xcor() < -300 or self.ycor() > 300 or self.ycor() < -300:
                self.goto(-1000, 1000)
                self.status = "primed"

class EnemyLaser(Ships):
    def __init__(self, shipshape, color, startx, starty):
        Ships.__init__(self, shipshape, color, existing_ships=[], startx=startx, starty=starty)
        self.move_speed = 15
        self.status = "primed"
        self.shapesize(stretch_wid=0.2, stretch_len=2, outline=None)
        self.goto(-1000, 1000)  
        

    def fire(self, enemy_ship):
        if self.status == "primed":
            self.goto(enemy_ship.xcor(), enemy_ship.ycor())
            self.setheading(enemy_ship.towards(player.xcor(), player.ycor()))  # Aim at player
            self.status = "fired"
            pygame.mixer.Sound.play(laser_sound)

    def move(self):
        if self.status == "fired":
            self.fd(self.move_speed)

            # Reset laser if it moves offscreen
            if self.xcor() > 300 or self.xcor() < -300 or self.ycor() > 300 or self.ycor() < -300:
                self.goto(-1000, 1000)
                self.status = "primed"


class AllyLaser(Ships):
    def __init__(self, shipshape, color, startx, starty):
        Ships.__init__(self, shipshape, color, existing_ships=[], startx=startx, starty=starty)
        self.move_speed = 15
        self.status = "primed"
        self.shapesize(stretch_wid=0.2, stretch_len=2, outline=None)
        self.goto(-1000, 1000)  
        

    def fire(self, ally_ship, enemy_ship):
        if self.status == "primed":
            self.goto(ally_ship.xcor(), ally_ship.ycor())
            self.setheading(ally_ship.towards(enemy_ship.xcor(), enemy_ship.ycor())) 
            self.status = "fired"
            pygame.mixer.Sound.play(laser_sound)

    def move(self):
        if self.status == "fired":
            self.fd(self.move_speed)

            # Reset laser if it moves offscreen
            if self.xcor() > 300 or self.xcor() < -300 or self.ycor() > 300 or self.ycor() < -300:
                self.goto(-1000, 1000)
                self.status = "primed"


player = Player("timothysship.gif", "lightgreen", ships_list)
ships_list.append(player)

enemy = Enemy("enemysship.gif", "grey", ships_list)
ships_list.append(enemy)

ally = Ally("allysship.gif", "blue", ships_list)
ships_list.append(ally)

meteor = Meteor("meteor.gif", "yellow", ships_list)
ships_list.append(meteor)

lasers = Laser("triangle", "red", 0, 0)



turtle.onkeypress(player.turn_left, "Left")
turtle.onkeypress(player.turn_right, "Right")
turtle.onkeypress(player.thrusters, "Up")
turtle.onkeypress(player.reverse_thrusters, "Down")
turtle.onkey(lasers.fire, "space")
turtle.listen()



while True:
    player.move()
    enemy.move()
    ally.move()
    meteor.move()
    lasers.move()
    enemy.move_and_attack()
    ally.move_and_attack(enemy)

    if ally.laser.collision(enemy):
        pygame.mixer.Sound.play(explosion_sound)
        enemy.ht()  # Hide the enemy temporarily
        game.score += 10  # Increase score for successful hit
        game.show_status()
        ally.laser.goto(-1000, 1000)  # Reset laser
        ally.laser.status = "primed"
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        turtle.ontimer(lambda: enemy.goto(x, y), 2000)  # Respawn enemy after delay
        turtle.ontimer(lambda: enemy.st(), 2000)  # Show enemy after delay

    if enemy.laser.collision(player):
        pygame.mixer.Sound.play(explosion_sound)
        player.lives -= 1
        game.score = max(0, game.score - 20)
        game.show_status()
        enemy.laser.goto(-1000, 1000)  # Reset the laser
        enemy.laser.status = "primed"
   

    if player.collision(enemy):
        pygame.mixer.Sound.play(crash_sound)
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        turtle.ontimer(lambda: setattr(enemy, 'move_speed', random.randint(2, 10)), 2000)
        game.score = max(0, game.score - 10)
        game.show_status()
        enemy.goto(x, y)

    if player.collision(ally):
        pygame.mixer.Sound.play(crash_sound)
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        game.score = max(0, game.score - 10)
        game.show_status()
        ally.goto(x, y)

    if lasers.collision(enemy):
        pygame.mixer.Sound.play(explosion_sound)
        enemy.ht()
        game.score = max(0, game.score + 10)
        game.show_status()
        lasers.goto(-1000,1000)
        lasers.status = "primed"
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        turtle.ontimer(lambda: enemy.goto(x,y), 2000)
        turtle.ontimer(lambda: setattr(enemy, 'move_speed', random.randint(2, 10)), 2000)
        turtle.ontimer(lambda: enemy.st(), 2000)

     
    if lasers.collision(ally):
        pygame.mixer.Sound.play(explosion_sound)
        ally.ht()
        game.score = max(0, game.score - 10)
        game.show_status()
        lasers.goto(-1000,1000)
        lasers.status = "primed"
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        turtle.ontimer(lambda: ally.goto(x,y), 2000)
        turtle.ontimer(lambda: ally.st(), 2000)    

    if lasers.collision(meteor):
        pygame.mixer.Sound.play(explosion_sound)
        meteor.ht()
        game.score = max(0, game.score + 50)
        game.show_status()
        lasers.goto(-1000,1000)
        lasers.status = "primed"
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        turtle.ontimer(lambda: meteor.goto(x,y), 10000)
        turtle.ontimer(lambda: meteor.st(), 10000)    
        
        
        lasers.goto(-1000, 1000)  
        lasers.status = "primed"