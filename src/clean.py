# -*- coding: UTF-8 -*-

# Author: Merve Sahin, Huayue Lu January 2019

"""This script cleans the input data set by droping irrelevant 
columns and transforming strings(money symbol, lbs inches, goalkeeping-specific
columns, etc).

It also adds a BMI column calculated from height and weight.

Usage: clean.py --file_path=<file_path> --out_file_path=<out_file_path>

Options:
--file_path=<file_path>           file path for untidy data set
--out_file_path=<out_file_path>   name and file path of output clean data set
"""

# example to run: python clean.py --file_path="../data/raw/fifa_data_train.csv" --out_file_path="../data/cleaned/cleaned_data.csv"
import pandas as pd
from docopt import docopt

opt = docopt(__doc__)

def convert_heigt_inches(height_str):
    '''
    convert inches to cm
    '''
    height = height_str.split("'")
    return int(height[0]) * 12 + int(height[1])

def main(file_path, out_file_path):

    df = pd.read_csv(file_path, index_col = 0)

    df = df.drop(columns = ['X','ID', 'Photo', 'Flag', 'Club.Logo', 'Loaned.From','Joined', 'Contract.Valid.Until'])

    df = df.dropna()

    df['Wage'] = df['Wage'].replace({'K': '', 'M': '*1e3', '€' : ""}, 
                                    regex=True).map(pd.eval).astype(int)

    df['Value'] = df['Value'].replace({'K': '', 'M': '*1e3', '€' : ""}, 
                                    regex=True).map(pd.eval).astype(int)

    df['Release.Clause'] = df['Release.Clause'].replace({'K': '', 'M': '*1e3', '€' : ""}, 
                                                        regex=True).map(pd.eval).astype(int)

    df['Height_Inches'] = df['Height'].apply(convert_heigt_inches).astype(int)
    df['Weight_Pounds'] = df['Weight'].replace({'lbs': ''}, regex=True).astype(int)
    df['BMI'] = (df['Weight_Pounds']/df['Height_Inches']**2)*703
    df = df.drop(columns = ['Height_Inches', 'Weight_Pounds', 'Weight', 'Height', 'Body.Type', 
                            'LS', 'ST','RS','LW','LF','CF','RF','RW','LAM',
                            'CAM','RAM','LM','LCM','CM','RCM','RM','LWB','LDM',
                            'CDM','RDM','RWB','LB','LCB','CB','RCB','RB','Jersey.Number'])
    df['Work.Rate.Former'] = df['Work.Rate'].apply(lambda x: x.split("/")[0])
    df['Work.Rate.Later'] = df['Work.Rate'].apply(lambda x: x.split("/")[1])
    df = df.drop(columns = ['Work.Rate'])
    df = df.loc[df['Position'] != 'GK']  
    df.to_csv(path_or_buf = out_file_path)
    test = pd.DataFrame([1,2])    
    assert type(df) == type(test) #######test if df is in proper file type
    assert df.shape[1] == 53      #######test if df is in proper shape

if __name__ == "__main__":
    main(opt["--file_path"], opt["--out_file_path"])


