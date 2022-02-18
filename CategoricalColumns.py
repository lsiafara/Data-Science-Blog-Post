#!/usr/bin/env python
# coding: utf-8

import pandas as pd

# Question 1

def filter_employment(df, mask_ls):
    '''
    INPUT 
        df - a dataframe holding the Employment column
        mask_ls - a list holding the emplyment values to filter for
        
    OUTPUT
        df - a dataframe with the filtered rows as per the values defined in the mask
        '''
    
    mask = df['Employment'].isin(mask_ls)   
    return df[mask]



def expand_cat_column(df, column):
    '''
    INPUT
        df - a dataframe holding at least one categorical column
        column - a string holding the name of the categorical column to expand
        
    OUTPUT
        df - the original dataframe with the expanded categorical column
        df_cat - the dataframe containing only the expanded columns
    
    '''
    
    df[column] = df[column].str.split(';')
    df_cat = pd.get_dummies(df[column].apply(pd.Series).stack()).sum(level=0)
    df = pd.concat([df.drop(column, axis=1), df_cat], axis=1)
    return df, df_cat


def map_salary(df_salary, df_ones):
    '''
    INPUT 
        df_salary - a dataframe containing a column with salary data
        df_ones - a column with 0 or 1s, indicating whether salary information shall be mapped or not in the given row
    OUTPUT 
        df - a dataframe with the mapped salary values
    
    '''
    
    mul = lambda col: col * df_salary
    df = df_ones.apply(mul)
    return df


def convert_to_fulltime(df_workhours, df_filtered_cols):
    '''
    INPUT
        df_workhours - a dataframe with the column WorkWeekHrs
        df_filtered_cols - a dataframe containing only columns with salary data
     
    OUTPUT
        df - a dataframe with the converted salary to 40hrs/week
     
     '''
    
    df = 40 *df_filtered_cols.div(df_workhours, axis=0)
    return df


def create_df_with_agg_values(df):
    '''
    INPUT
        df - a dataframe with columns containing salary values
     
    OUTPUT
        df_agg - a new dataframe containing mean, standard deviation and number of counts for each column of the input dataframe 
    '''
        
    mask = df != 0 
    df_agg_mean = df[mask].median()
    df_agg_std = df[mask].std()
    df_agg_counts = df[mask].count()

    df_agg = pd.concat([df_agg_mean, df_agg_std, df_agg_counts], axis=1)
    df_agg = df_agg.rename(columns={0:'Median yearly compensation', 1:'Std compensation', 2:'Counts'})
    df_agg = df_agg.sort_values(by = ['Median yearly compensation'], ascending= True)
    return df_agg


def calculate_salary_per_category(df, cat_column):
    '''
    INPUT
        df - a dataframe with the column WorkWeekHrs, ConvertedComp, and a column with categorical values
        cat_column - a categorical column for each value of which we want to calculate the salary
    OUTPUT
        df_agg_results - a new dataframe containing median, standard deviation and number of counts for each column of the expandecategorical values 
     '''
    
    df_expand, df_cat = expand_cat_column(df, cat_column)
    df_salary = map_salary(df_expand['ConvertedComp'], df_cat)
    df_full_time = convert_to_fulltime(df['WorkWeekHrs'], df_salary)
    df_agg_results = create_df_with_agg_values(df_full_time)
    return df_agg_results


# In[ ]:




