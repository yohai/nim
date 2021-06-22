import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from enum import Enum
import pdb
import time
import nim


class GameState(Enum):
    SETUP = 1
    EDIT_MOVE = 2
    CPU_MOVE = 3


class Column:
    def __init__(self, x, game):
        self.x = x
        self.circles = []
        self.game = game

        add = mpl.patches.Circle([self.x, 0], radius=0.46, color='r')
        rem = mpl.patches.Circle([self.x, -1], radius=0.46, color='g')
        self.game.ax.add_artist(add)
        self.game.ax.add_artist(rem)
        self.add = EditCircle(add, self, True)
        self.rem = EditCircle(rem, self, False)

    def add_circle(self):
        c = mpl.patches.Circle([self.x, len(self.circles) + 1], radius=0.4)
        self.game.ax.add_artist(c)
        self.circles.append(Node(c, self, self.game))
        self.game.fig.canvas.draw()

    def remove_circle(self, circle=None):
        if self.circles:
            if circle is None:
                circle = self.circles[-1]
            circle.artist.remove()
            self.circles.remove(circle)
            self.game.fig.canvas.draw()


class ClicakbleCircle:
    def __init__(self, artist, column):
        self.clicked_in = False
        self.artist = artist
        self.column = column
        self.cidpress = self.artist.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.artist.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)

    def on_release(self, event):
        if not (self.clicked_in and self.artist.get_visible()):
            return
        contains, _ = self.artist.contains(event)
        if contains:
            self.action()

    def on_press(self, event):
        contains, _ = self.artist.contains(event)
        if contains:
            self.clicked_in = True
        else:
            self.clicked_in = False

    def action(self):
        raise NotImplementedError()


class Node(ClicakbleCircle):
    def __init__(self, artist, column, game):
        super().__init__(artist, column)
        self.game = game
        self.tentative = False

    def action(self):
        if self.game.state == GameState.SETUP:
            return
        elif self.game.state == GameState.EDIT_MOVE:
            if self.game.move is None:
                self.game.move = [self.column, 0]

            if self.game.move[0] is not self.column:
                # A column is set, but it's not ours!
                return

            if not self.tentative:
                self.tentative = True
                self.game.move[1] += 1
                self.artist.set_alpha(0.5)
                self.game.fig.canvas.draw()
            else:
                assert self.game.move[1] > 0
                self.tentative = False
                self.game.move[1] -= 1
                if self.game.move[1] == 0:
                    self.game.move = None

                self.artist.set_alpha(1)
                self.game.fig.canvas.draw()


class EditCircle(ClicakbleCircle):
    """Circle for adding/removing pawns"""

    def __init__(self, artist, column, add):
        super().__init__(artist, column)
        self.add = add

    def action(self):
        if self.add:
            self.column.add_circle()
        else:
            self.column.remove_circle()


class Game:
    def __init__(self):
        self.state = GameState.SETUP
        self.move = None  # move is [column, number of nodes to pop]
        self.columns = []
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(-2, 10)
        self.ax.set_aspect(1)

        self.ax_start = plt.axes([0.7, 0.1, 0.1, 0.075])
        self.ax_go = plt.axes([0.59, 0.1, 0.1, 0.075])
        self.btn_start = mpl.widgets.Button(self.ax_start,
                                            'Start\nplaying')
        self.btn_go = mpl.widgets.Button(self.ax_go, 'Go!')
        self.btn_start.on_clicked(self.start_game)
        self.btn_go.on_clicked(self.do_user_move)

        self.ax_go.set_visible(False)
        for i in range(1, 8):
            col = Column(i, self)

            if i <= 4:
                for k in range(6):
                    col.add_circle()
            self.columns.append(col)

    def do_user_move(self, *args, **kwargs):
        if self.move is None:
            return
        col = self.move[0]
        to_remove = [c for c in col.circles if c.tentative]
        for c in to_remove:
            col.remove_circle(c)
            plt.pause(0.3)
        self.move = None

    def start_game(self, *args, **kwargs):
        self.state = GameState.EDIT_MOVE
        self.ax_go.set_visible(True)
        self.ax_start.set_visible(False)
        for col in self.columns:
            col.add.artist.set_visible(False)
            col.rem.artist.set_visible(False)
        self.fig.canvas.draw()
        self.gametree = nim.GameTree(
            tuple(len(c.circles) for c in self.columns if len(c.circles))
        )


if __name__ == '__main__':
    game = Game()
    plt.show()
