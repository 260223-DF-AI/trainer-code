# PANDAS DEMO

## Documentation and Introductory Resources
- [Official](https://pandas.pydata.org/docs/)
    - [10 Min Intro](https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html)
- [W3 Schools](https://www.w3schools.com/python/pandas/default.asp)
- [Geeks for Geeks](https://www.geeksforgeeks.org/pandas/pandas-tutorial/)
- [Kaggle](https://www.kaggle.com/learn/pandas)
- [Pandas Cheatsheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)

## Overview
- Pandas is a Python library used to create 2 dimensional arrays (table w/ columns and rows)  
  - Allows easy creation of spreadsheet-like collections of data  
- Why use Pandas?  
  - You COULD use a list of lists, dictionaries, or other forms of included collections but pandas is specialized.  
  - Pandas focuses on performance, readability, and includes methods for analyzing/manipulating data  
  - Has its own methods for reading and writing data from and to files  
  - Compared to built-in ways of file i/o (“with open(...),”) Pandas can read in a .csv file and organize it into a clean table with just one command: “df \= pd.read\_csv('data.csv')”  
  - Data analysis functions:  
    - analyze the correlation between columns in the dataset  
    - create backend for graphs/data plots. Combined with a data vis tool like matplotlib, it can make useful graphs   
  - Data manipulation:  
    - Combining data sets  
    - Handling missing data  
    - Mapping