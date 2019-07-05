"""
Pong Game implemented using Python and Kivy.

"""

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget

from kivy.properties import NumericProperty
from kivy.properties import ReferenceListProperty
from kivy.properties import ObjectProperty

from kivy.vector import Vector
from kivy.config import Config

from random import randint

Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '200')
Config.set('kivy', 'window_icon', 'successLogo.png')


class PongBall(Widget):
    """
    This class represents the Ball.

    Attributes:
        velocity_x (NumericProperty): represents the velocity of the ball along the x axis.
        velocity_y (NumericProperty): represents the velocity of the ball along the y axis.
        velocity (ReferenceListProperty): allows shorthand for velocity_x/velocity_y i.e. velocity.x.

    """
    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    # Referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ''move'' function will move the ball on one step. THis
    # will be called in equal intervals to animate movement
    def move(self):
        """
        This method moves the ball using velocity.
        """
        self.pos = Vector(*self.velocity) + self.pos


class PongPaddle(Widget):
    """
    This class is used to represent the Paddle and players functionality.

    PongPaddle object is used to provide the players behavior and maintain score state.

    Attributes:
        score (NumericProperty):  The current score of the player controlling this paddle.

    """
    score = NumericProperty(0)

    def bounce_ball(self, ball: PongBall):
        """
        The method used to bounce the ball off of paddle upon collision.
        Args:
            ball (PongBall):  The ball to be bounced.
        """
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongGame(Widget):
    """
    This widget is used to represent the PongGame as a whole.

    Attributes:
        ball (ObjectProperty): Will hold the id of the PongBall associated with this PongGame.
        player1 (ObjectProperty): Will hold the id of the PongPaddle associated with player1.
        player2 (ObjectProperty): Will hold the id of the PongPaddle associated with player2.
    """
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel: Vector = (4, 0)):
        """
        This method sets the ball object in motion.
        Args:
            vel (Tuple): the velocity to be applied to the ball.
        """
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        """
        This method handles updating the game state each frame
        Args:
            dt: kivy required param provided by default
        """
        self.ball.move()

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))

        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        """
        This method handles the input behavior for our game, moving the paddles.

        Which of the paddles moved is determined based on the x coordinate of the input.
        The y coordinate of the paddle is
        Args:
            touch (Input): the touch/mouse input on screen.
        """
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    """Pong Game GUI Application"""

    def build(self):
        game = PongGame()
        game.serve_ball()
        self.icon = 'game/successLogo.png'
        Clock.schedule_interval(game.update, 1.0 / 60.0) # makes the game update at 60 frames per sec
        return game


if __name__ == '__main__':
    PongApp().run()
