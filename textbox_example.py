from matplotlib import pyplot as plt
import numpy as np
from matplotlib.widgets import TextBox
fig, ax = plt.subplots()
ax.plot(np.random.rand(10))

def onclick(event):
    ax.plot(event.xdata, event.ydata, 'og')
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    fig.canvas.draw_idle()


def submit(text):
    ydata = eval(text)
    l.set_ydata(ydata)
    ax.set_ylim(np.min(ydata), np.max(ydata))
    plt.draw()

t = np.arange(-2.0, 2.0, 0.001)
s = t ** 2
initial_text = "t ** 2"
l, = plt.plot(t, s, lw=2)
axbox = plt.axes([0.1, 0.05, 0.8, 0.075])
text_box = TextBox(axbox, 'Evaluate', initial=initial_text)
text_box.on_submit(submit)

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
