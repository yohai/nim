import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


class Column:
    def __init__(self, x):
        self.x = x
        self.circles = []

        add = mpl.patches.Circle([self.x, 0], radius=0.46, color='r')
        rem = mpl.patches.Circle([self.x, -1], radius=0.46, color='g')
        ax.add_artist(add)
        ax.add_artist(rem)
        self.add = EditCircle(add, self, True)
        self.rem = EditCircle(rem, self, False)

    def add_circle(self):
        c = mpl.patches.Circle([self.x, len(self.circles) + 1], radius=0.46)
        ax.add_artist(c)
        self.circles.append(Circle(c, self))
        fig.canvas.draw()

    def remove_circle(self):
        if self.circles:
            self.circles[-1].circ.remove()
            self.circles = self.circles[:-1]
            fig.canvas.draw()


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


def start_game(self):
    for col in cols:
        col.add.circ.set_visible(not col.add.circ.get_visible())
        col.rem.circ.set_visible(not col.rem.circ.get_visible())
    fig.canvas.draw()


setup = True
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(-3, 10)
ax.set_aspect(1)
cols = []

ax_play = plt.axes([0.7, 0.1, 0.1, 0.075])
ax_go = plt.axes([0.59, 0.1, 0.1, 0.075])
ax_undo = plt.axes([0.48, 0.1, 0.1, 0.075])
btn_play = mpl.widgets.Button(ax_play, 'Start\nplaying')
btn_go = mpl.widgets.Button(ax_go, 'Go!')
btn_undo = mpl.widgets.Button(ax_undo, 'Reset\nmove')
btn_play.on_clicked(start_game)

for i in range(1, 8):
    col = Column(i)

    if i <= 4:
        for k in range(6):
            col.add_circle()
    cols.append(col)

plt.show()
if setup:
    pass
