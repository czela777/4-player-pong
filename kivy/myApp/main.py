from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
import random


class Powerup(Widget):

    def takepowerup(self, ball):
        if self.collide_widget(ball) and self.visible==1:
            self.visible = 0
            ball.velocity = Vector(ball.velocity[0], ball.velocity[1]).rotate(randint(0, 360))

    def create(self):
        y = randint(0, 300)
        if y == 1 and self.visible == 0:
            self.xpos = random.uniform(0, 1)
            self.ypos = random.uniform(0, 1)
            self.visible=1


    r = NumericProperty(1)
    g = NumericProperty(0.5)
    b = NumericProperty(0.5)
    visible=NumericProperty(0)
    col=ReferenceListProperty(r,g,b,visible)
    Color = col
    xpos=NumericProperty(0)
    ypos=NumericProperty(0)




class PongGame(Widget):

    pup = ObjectProperty(None)
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    player3 = ObjectProperty(None)
    player4 = ObjectProperty(None)
    Color = [1, 0, 0, 1]

    def PlayPressed(self, instance):
        self.serve_ball(4, 0)
        try:
            self.remove_widget(self.playbutton)
            self.remove_widget(self.playlabel)

        except:
            pass
    '''
   
    def countdown(self,x,y):
            self.countlabel = Label(size_hint=(None, None), text='3', font_size=100)
            self.countlabel.pos = (self.width / 2, self.height * 2 / 3)
            Clock.schedule_once(lambda dt: self.add_widget(self.countlabel), 0)
            Clock.schedule_once(lambda dt: self.remove_widget(self.countlabel), 1)

            self.countlabel1 = Label(size_hint=(None, None), text='2', font_size=100)
            self.countlabel1.pos = (self.width / 2, self.height * 2 / 3)
            Clock.schedule_once(lambda dt: self.add_widget(self.countlabel1), 1)
            Clock.schedule_once(lambda dt: self.remove_widget(self.countlabel1), 2)

            self.countlabel2 = Label(size_hint=(None, None), text='1', font_size=100)
            self.countlabel2.pos = (self.width / 2, self.height * 2 / 3)
            Clock.schedule_once(lambda dt: self.add_widget(self.countlabel2), 2)
            Clock.schedule_once(lambda dt: self.remove_widget(self.countlabel2), 3)

            self.countlabel3 = Label(size_hint=(None, None), text='0', font_size=100)
            self.countlabel3.pos = (self.width / 2, self.height * 2 / 3)
            Clock.schedule_once(lambda dt: self.add_widget(self.countlabel3), 3)
            Clock.schedule_once(lambda dt: self.remove_widget(self.countlabel3), 4)

            Clock.schedule_once(lambda dt: self.serve_ball(x,y), 4)
    '''

    def serve_ball(self, x, y):
        self.ball.center = self.center
        self.ball.velocity = Vector(x, y).rotate(randint(0, 360))

        self.pup.visible = 0

    def update(self, dt):
        self.ball.move()







        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        self.player3.bounce_ball(self.ball)
        self.player4.bounce_ball(self.ball)
        self.pup.takepowerup(self.ball)

        if self.ball.velocity!=[0,0]:

            self.pup.create()

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # went of to a side to score a point?
        if self.ball.x + self.ball.size[0] < self.x:
            self.playerScored(self.player2)
        if self.ball.x > self.width:
            self.playerScored(self.player1)

    def playerScored(self, player):
        player.score += 1

        if player.score > 4:
            self.serve_ball(0, 0)
            self.winlabel = Label(size_hint=(None, None), text=player.Teamname + ' wins!', font_size=140,
                                  color=player.Color)
            self.winlabel.pos = (self.width / 2, self.height / 2)
            self.add_widget(self.winlabel)
            self.contbutton = Button(size_hint=(.5, 1), text='Play again', font_size=20, background_color=player.Color)
            self.contbutton.bind(on_press=self.PlayAgainPressed)
            self.contbutton.pos = (self.width / 2 - self.contbutton.width / 2, self.height / 4)
            self.add_widget(self.contbutton)
        else:
            self.scorelabel = Label(size_hint=(None, None), text=player.Teamname + ' scores!', font_size=100,
                                    color=player.Color)
            self.scorelabel.pos = (self.width / 2, self.height * 2 / 3)
            self.add_widget(self.scorelabel)
            self.serve_ball(4, 0)
            Clock.schedule_once(lambda dt: self.remove_widget(self.scorelabel), 1)

    def PlayAgainPressed(self, instance):

        try:
            self.remove_widget(self.winlabel), self.remove_widget(self.contbutton)
        except:
            pass

        self.player1.score = 0
        self.player2.score = 0

        self.serve_ball(4, 0)

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            if touch.y < self.height / 2 - (self.player1.width/2):
                self.player1.center_y = touch.y
            elif touch.y > self.height / 2 + (self.player1.width/2):
                self.player3.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            if touch.y < self.height / 2 - (self.player1.width/2):
                self.player2.center_y = touch.y
            elif touch.y > self.height / 2 + (self.player1.width/2):
                self.player4.center_y = touch.y
    def play(self):
        self.pup.visible=0
        self.playbutton = Button(size_hint=(1, 1), text='Play ', font_size=20)
        self.playbutton.bind(on_press=self.PlayPressed)
        self.playbutton.pos = (0,0)
        self.add_widget(self.playbutton)

        self.playlabel = Label( text='Welcome to the 4-player pong game', font_size=40,color=[0,0.5,0,7,1] )
        self.playlabel.pos = (self.width*3,self.height*3 )
        self.add_widget(self.playlabel)

class PongBall(Widget):
    Color = [1, 1, 0, 1]
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)




    def move(self):
        self.pos = Vector(self.velocity) + self.pos


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongPaddleBlue(PongPaddle):
    Color = [0, 0.5, 1, 1]
    Teamname = 'Blue'


class PongPaddleRed(PongPaddle):
    Color = [1, 0, 0, 1]
    Teamname = 'Red'


class PongApp(App):
    def build(self):
        game = PongGame()
        game.play()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    PongApp().run()
