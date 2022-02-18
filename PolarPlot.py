#!/usr/bin/env python
# coding: utf-8

#Code for a nice polar plot creation. Source: https://www.python-graph-gallery.com/

import matplotlib.pyplot as plt
import numpy as np


def polar_plot(df, col_name):
    ''' 
        INPUT
        df - the input dataframe
        col_name - a string with the name of the column to plot
        
    '''
    # initialize the figure
    plt.figure(figsize=(20,10))
    ax = plt.subplot(111, polar=True)
    plt.axis('off')

    # Constants = parameters controling the plot layout:
    upperLimit = 120
    lowerLimit = 30
    labelPadding = 1000

    # Compute max and min in the dataset
    max = df[col_name].max()

    # Let's compute heights: they are a conversion of each item value in those new coordinates
    # In our example, 0 in the dataset will be converted to the lowerLimit (10)
    # The maximum will be converted to the upperLimit (100)
    slope = (max - lowerLimit) / max
    heights = slope * df[col_name] + lowerLimit

    # Compute the width of each bar. In total we have 2*Pi = 360°
    width = 2*np.pi / len(df.index)

    # Compute the angle each bar is centered on:
    indexes = list(range(1, len(df.index)+1))
    angles = [element * width +0.2 for element in indexes]


    # Draw bars
    bars = ax.bar(
        x=angles, 
        height=heights, 
        width=width, 
        bottom=lowerLimit,
        linewidth=2, 
        edgecolor="white",
        color="#61a4b2",
    )

    # Add labels
    for bar, angle, height, label in zip(bars,angles, heights, df.index):
        # Labels are rotated. Rotation must be specified in degrees :(
        rotation = np.rad2deg(angle)

        # Flip some labels upside down
        alignment = ""
        if angle >= np.pi/2 and angle < 3*np.pi/2:
            alignment = "right"
            rotation = rotation + 180
        else: 
            alignment = "left"

        # Finally add the labels
        ax.text(
            x=angle, 
            y=lowerLimit + bar.get_height() + labelPadding, 
            s=label, 
            ha=alignment, 
            va='center', 
            rotation=rotation, 
            rotation_mode="anchor") 

    #plt.savefig('Salary_vs_language_polar.png')

