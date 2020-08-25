import argparse
import logging

import sfsb

parser = argparse.ArgumentParser()
parser.add_argument("-P", action="store_true")
parser.add_argument("-v", action="store_true")
args = parser.parse_args()

if args.v:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

if args.P:
    import threading
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    fig, ax = plt.subplots()
    im = ax.imshow(np.zeros((5, 5)), extent=[0, 1, 0, 1], vmin=0, vmax=1)

    y_values = ["AF4", "T8", "Pz", "T7", "AF3"]
    x_values = ["theta", "alpha", "betaL", "betaH", "gamma"]

    ax.set_xticks([0.1, 0.3, 0.5, 0.7, 0.9])
    ax.set_yticks([0.1, 0.3, 0.5, 0.7, 0.9])

    ax.set_xticklabels(x_values)
    ax.set_yticklabels(y_values)

    fig.colorbar(im)


    def animate(i):
        im.set_data(sfsb.pow_listener.data)
        im.autoscale()
        return im


    anim = FuncAnimation(fig, animate, interval=100)

    t = threading.Thread(target=sfsb.api.run)
    t.start()
    plt.show()
    t.join()
else:
    sfsb.api.run()
