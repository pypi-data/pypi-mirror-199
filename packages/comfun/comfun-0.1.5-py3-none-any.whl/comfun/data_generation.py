#!/usr/bin/env python3

import logging
import matplotlib.pyplot as plt
import os
import pandas as pd


# TODO: Add vodual tracers of clicks


def record_clicks(xlims: tuple = (0, 1), ylims: tuple = (0, 1)) -> dict:

    def onclick(event):
        x, y = event.xdata, event.ydata
        logging.info(f"Recorded click at: x:{x}, y:{y}")
        coords["x"].append(event.xdata)
        coords["y"].append(event.ydata)

    coords = {"x": [],
              "y": []}
    fig, ax = plt.subplots()
    ax.set_ylim(ylims)
    ax.set_xlim(xlims)
    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    return coords


def save_coordinates_to_csv(coordinates: dict, fpath="", xlims = (0, 1), ylims = (0, 1)):
    if not fpath:
        fpath = os.path.join(os.path.expanduser('~'), 'Desktop', "test_data.csv")
    data = pd.DataFrame(coordinates)
    data.to_csv(fpath, index=False)


def clicks_to_csv(fpath: str = "", xlims: tuple = (0, 1), ylims: tuple = (0, 1)):
    if not fpath:
        fpath = os.path.join(os.path.expanduser('~'), 'Desktop', "test_data.csv")
    coordinates = record_clicks(xlims=xlims, ylims=ylims)
    save_coordinates_to_csv(coordinates=coordinates, fpath=fpath, xlims=xlims, ylims=ylims)


if __name__ == "__main__":
    loglvl = logging.DEBUG
    logformat = "[%(levelname)s]\t%(funcName)s:  %(message)s"
    logging.basicConfig(level=loglvl, format=logformat)

    clicks_to_csv(xlims=(0, 10), ylims=(0, 100))
