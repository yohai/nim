import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


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
        c = mpl.patches.Circle([self.x, len(self.circles) + 1], radius=0.46)
        self.game.ax.add_artist(c)
        self.circles.append(Circle(c, self))
        self.game.fig.canvas.draw()

    def remove_circle(self):
        if self.circles:
            self.circles[-1].circ.remove()
            self.circles = self.circles[:-1]
            self.game.fig.canvas.draw()


class ClicakbleCircle:
    def __init__(self, circ, column):
        self.clicked_in = False
        self.circ = circ
        self.column = column
        self.cidpress = self.circ.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.circ.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)

    def on_release(self, event):
        if not (self.clicked_in and self.circ.get_visible()):
            return
        contains, _ = self.circ.contains(event)
        if contains:
            self.action()

    def on_press(self, event):
        contains, _ = self.circ.contains(event)
        if contains:
            self.clicked_in = True
        else:
            self.clicked_in = False

    def action(self):
        raise NotImplementedError()


class Circle(ClicakbleCircle):
    def __init__(self, circ, column):
        super().__init__(circ, column)

    def action(self):
        pass


class EditCircle(ClicakbleCircle):
    def __init__(self, circ, column, add):
        super().__init__(circ, column)
        self.add = add

    def action(self):
        if self.add:
            self.column.add_circle()
        else:
            self.column.remove_circle()


class Game:
    def __init__(self):
        self.setup = True
        self.cols = []
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(-2, 10)
        self.ax.set_aspect(1)

        self.ax_start = plt.axes([0.7, 0.1, 0.1, 0.075])
        self.ax_go = plt.axes([0.59, 0.1, 0.1, 0.075])
        self.ax_undo = plt.axes([0.48, 0.1, 0.1, 0.075])
        self.btn_start = mpl.widgets.Button(self.ax_start,
                                            'Start\nplaying')
        self.btn_go = mpl.widgets.Button(self.ax_go, 'Go!')
        self.btn_undo = mpl.widgets.Button(self.ax_undo,
                                           'Reset\nmove')
        self.btn_start.on_clicked(self.start_game)

        self.ax_go.set_visible(False)
        self.ax_undo.set_visible(False)
        for i in range(1, 8):
            col = Column(i, self)

            if i <= 4:
                for k in range(6):
                    col.add_circle()
            self.cols.append(col)

    def start_game(self, *args, **kwargs):
        self.setup = False
        self.ax_go.set_visible(True)
        self.ax_undo.set_visible(True)
        self.ax_start.set_visible(False)
        for col in self.cols:
            col.add.circ.set_visible(False)
            col.rem.circ.set_visible(False)
        self.fig.canvas.draw()


if __name__ == '__main__':
    Game()
    plt.show()
