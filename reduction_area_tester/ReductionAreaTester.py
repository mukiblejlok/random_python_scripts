'''
This script allows create and test MostRepresentativeDB
reduction method along with anomaly detection.

It does following:
1.  Opens empty plot where you can add points by clicking on figure.
    When you are done just close the figure.
2.  Reduces provided dataset by applying MostRepresentativeDB.
    Dataset is reduced to REDUCED_SET_SIZE value.
4.  Draws a heatmap plot with reduced dataset.
'''

# Libraries import
import numpy as np
import matplotlib.pyplot as plt
# SDMS import
from sdms_diagnostic.ml.reduction import MostRepresentativeDataSet
from sdms_diagnostic.ml.anomaly import ZiemowitNN
from sdms_diagnostic.plot import *

# SETTINGS
REDUCED_SET_SIZE = 25
MAX_POINTS_NUMBER = 100
NORMALISATION_RANGE = (-1, 1)
METRIC_P = 6
SAVE_TO_FILE = True
SAVE_PATH = r"D:/reduced_area_data.npy"


# Global variables
global ax
global coords
coords = []


# Click function definition
def onclick(event):
    try:
        ix, iy = event.xdata, event.ydata
        ax.plot(ix, iy, marker='o', color='red')
        # Append point to Coords list
        coords.append([ix, iy])
        # Prepare text box with information
        normal_textstr = "Number of Points: {:3d}".format(len(coords))
        min_textstr = "Keep on clicking.\n{}".format(normal_textstr)
        ok_textstr = "Enough points.\n{}".format(normal_textstr)
        max_textstr = "Maximum number of points.\n{}.".format(normal_textstr)
        if len(coords) <= REDUCED_SET_SIZE:
            textstr = min_textstr
        elif len(coords) <= MAX_POINTS_NUMBER + 2:
            textstr = ok_textstr
        else:
            textstr = max_textstr
        props = dict(boxstyle='round', facecolor='wheat', alpha=1)
        ax.text(0.8, 1.1, textstr, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props)
        # update figure
        fig.canvas.draw()
    except ValueError:
        print("You have clicked outside the area.")
    # Max Points Limit
    if len(coords) >= MAX_POINTS_NUMBER:
        fig.canvas.mpl_disconnect(cid)
    return np.array(coords)


##########################
# 1. Prepare a figure to input dateset points
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(NORMALISATION_RANGE)
ax.set_ylim(NORMALISATION_RANGE)
title = ["Click on plot area",
         "to provide dataset points",
         "when done close figure window"]
ax.set_title("\n".join(title))
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show(fig)

# 2. Prepare and save data
in_data = np.array(coords)
if SAVE_TO_FILE:
    np.save(SAVE_PATH, in_data)
    print("Data {} saved to {}".format(in_data.shape, SAVE_PATH))
    


# 3. Reduce provided dataset
zr = MostRepresentativeDataSet(in_data, remove_duplicates=False)
zr.normalize(*NORMALISATION_RANGE)
x_r = zr.reduce(REDUCED_SET_SIZE)
dm, dstd = zr.last_point_statistics(use_min=True)
dm, dstd = zr.dataset_statistics()


# 4. Calculate and draw anomaly area for reduced dataset
za = ZiemowitNN(X=x_r,
                distance_mean=dm,
                distance_std=dstd,
                metric_p=METRIC_P)

fig = plot_znn(za,
               xmin=-5, xmax=5,
               ymin=-5, ymax=5,
               h=100, mode='anomaly')
plt.show(fig)







