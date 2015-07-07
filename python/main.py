from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from math import sin, cos

class PongPaddle (Widget):
    score = NumericProperty(0)
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + 10 * offset
            self.size[1] *= randint(1,2)/1.414
            ball.x += ball.velocity[0] / abs (ball.velocity[0]) * ball.width

class PongBall (Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty (velocity_x, velocity_y)

    def move (self):
        self.pos = Vector (*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty (None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball (self):
        self.ball.center = self.center
        self.ball.velocity = Vector (5, 0)

    def update (self, dt): 
        self.ball.move()

        self.player1.bounce_ball (self.ball)
        self.player2.bounce_ball (self.ball)

        #bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.y > self.height):
            self.ball.velocity_y *= -1

        #bounce off left and right
        if self.ball.x < self.x:
            self.player2.score += 1
            self.ball.center = self.center
            self.ball.velocity = Vector (5, 0)

        if self.ball.x + self.ball.width > self.width:
            self.player1.score += 1
            self.ball.center = self.center
            self.ball.velocity = Vector (-5, 0)

    def on_touch_move(self, touch):
        # if touch.x < self.width / 3:
            self.player1.center_y = touch.y
            self.player1.center_x = touch.x
        # if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame ()
        game.serve_ball ()
        Clock.schedule_interval (game.update, 1.0/100.0)
        return game


if __name__ == '__main__':
    PongApp().run()
