import os
import random
import pygame

pygame.mixer.init()
explosion_sound = pygame.mixer.Sound("explosion.wav")
crash_sound = pygame.mixer.Sound("crash.wav")
laser_sound = pygame.mixer.Sound("laser.wav")  

import turtle
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



class Game():
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
    def __init__(self, shipshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape = shipshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.shapesize(stretch_wid=2, stretch_len=2)
        self.fd(0)
        self.goto(startx, starty)
        self.move_speed = 1

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
    def __init__(self, shipshape, color, startx, starty):
        Ships.__init__(self, shipshape, color, startx, starty)
        self.move_speed = 4 
        self.lives = 5

    def turn_left(self):
        self.lt(20)
    def turn_right(self):
        self.rt(20)
    def thrusters(self):
        self.move_speed += 1
    def reverse_thrusters(self):
        self.move_speed -= 1


class Enemy(Ships):
    def __init__(self, shipshape, color, startx, starty):
        Ships.__init__(self, shipshape, color, startx, starty)
        self.move_speed = 5
        self.shapesize(stretch_wid = 1, stretch_len = 1)
        self.setheading(random.randint(0,360))

class Ally(Ships):
    def __init__(self, shipshape, color, startx, starty):
        Ships.__init__(self, shipshape, color, startx, starty)
        self.move_speed = 7
        self.shapesize(stretch_wid = 1, stretch_len = 1)
        self.setheading(random.randint(0,360))
    
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
        Ships.__init__(self, shipshape, color, startx, starty)
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



player = Player("timothysship.gif", "lightgreen", 0, 0)
enemy = Enemy("enemysship.gif", "grey", -100, 0)
ally = Ally("allysship.gif", "blue", 0, 0)
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
    lasers.move()

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
        game.score += 10
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
        game.score -= 10
        game.show_status()
        lasers.goto(-1000,1000)
        lasers.status = "primed"
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        turtle.ontimer(lambda: ally.goto(x,y), 2000)
        turtle.ontimer(lambda: ally.st(), 2000)    
        
        lasers.goto(-1000, 1000)  
        lasers.status = "primed"  