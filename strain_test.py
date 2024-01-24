"""
program: df_basics.py

purpose: demonstrate basic operations with pandas library

comments: 

author: Russell Folks

history:
-------
12-08-2023  creation
01-18-2024  Refine comments, remove redundant examples, re-order examples.
"""
import pandas as pd

def basics(df):
    print('pandas ops with strain_nml_sample.csv data')
    print('------------------------------------------')
    print('show data head')
    print(df.head())
    print()

    print('show 1 col: ages')
    strain_ages = df['age']
    print(strain_ages)
    print(f'name of this series is: {strain_ages.name}')
    print(strain_ages.shape)
    print()

    print('show 3 col: pt code, TID, rest EF')
    code_tid_EF = df[['pt code', 'TID', 'rest EF']]
    print(code_tid_EF)
    print()

    print('show 1 col with condition, v1')
    print('...ages over 55, booleans')
    ages_over_55_true = df['age'] > 55
    print(ages_over_55_true)
    print(f'shape: {ages_over_55_true.shape}')
    print('...DataFrame found using the booleans:')
    print(df[ages_over_55_true])
    print()

    print('show 1 col with condition, v2')
    print('...ages over 55, using ".loc"')
    over_55 = df.loc[df['age'] > 55, ['pt code', 'age']]
    print(over_55)
    print(f'shape: {over_55.shape}')
    print()

    print('show all cols, filtered, v1')
    print('...ages 55 and 71, using isin()')
    restEF_55or71 = df[df['rest EF'].isin([55, 71])]
    print(restEF_55or71)
    print(f'shape: {restEF_55or71.shape}')
    print()

    print('show all cols, filtered, v2')
    print('ages 55 and 71, using conditionals')
    restEFequiv = df[(df['rest EF'] == 55) | (df['rest EF'] == 71)]
    print(restEFequiv)
    print(f'shape: {restEFequiv.shape}')
    print()

    print('show 1 row')
    r3 = df.iloc[2]
    print(f'3rd row: \n{r3}')
    print()

    print('show subset of rows')
    r5_10 = df.loc[4:9]
    print(f'rows 5-10: \n{r5_10}')
    print()

    print('show subset of rows and cols, last 5r and c2,3, v1')
    subset1 = df.iloc[-5:][['gender', 'age']]
    print(subset1)
    print()

    print('show subset of rows and cols, last 5 and 2,3, v2')
    subset2 = df.loc[17:21][['gender', 'age']]
    print(subset2)
    print()

    print('show subset of rows and cols, last 5 and 2,3, v3')
    subset1 = df.iloc[-5:, 1:3]
    print(subset1)
    print()

df = pd.read_csv('data/strain_nml_sample.csv')
basics(df)
