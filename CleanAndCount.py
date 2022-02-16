#!/usr/bin/env python
# coding: utf-8
# Source: https://github.com/jjrunner/stackoverflow


import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt



#Question 3
def total_count(df, col1, col2, look_for):
    '''
    INPUT:
    df - the pandas dataframe you want to search
    col1 - the column name you want to look through
    col2 - the column you want to count values from
    look_for - a list of strings you want to search for in each row of df[col]

    OUTPUT:
    new_df - a dataframe of each look_for with the count of how often it shows up
    '''
    new_df = defaultdict(int)
    #loop through list of ed types
    for val in look_for:
        #loop through rows
        for idx in range(df.shape[0]):
            #if the ed type is in the row add 1
            if val in df[col1][idx]:
                new_df[val] += int(df[col2][idx])
    new_df = pd.DataFrame(pd.Series(new_df)).reset_index()
    new_df.columns = [col1, col2]
    new_df.sort_values('count', ascending=False, inplace=True)
    return new_df


def clean_and_plot(df, column, possible_vals, title='', plot=True):
    '''
    INPUT 
        df - a dataframe holding the CousinEducation column
        title - string the title of your plot
        axis - axis object
        plot - bool providing whether or not you want a plot back
        
    OUTPUT
        study_df - a dataframe with the count of how many individuals
        Displays a plot of pretty things related to the CousinEducation column.
    '''
    study = df[column].value_counts().reset_index()
    study.rename(columns={'index': 'method', column: 'count'}, inplace=True)
    study_df = total_count(study, 'method', 'count', possible_vals)
    study_df.set_index('method', inplace=True)
    if plot:
        norm_df = (study_df/study_df.sum()).sort_values(by = ['count'], ascending= True)
        print(norm_df)
        norm_df.plot(kind='barh', legend=None, figsize=(7, 5))
        plt.title(title);
        plt.show()
    props_study_df = (study_df/study_df.sum())
    return props_study_df


