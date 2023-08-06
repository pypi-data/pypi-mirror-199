import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime as dt
path = os.getcwd()

class Montana:
    @staticmethod
    def input_dropdown_micro(macro_period: str) -> list:
        """
        Generate a list of dictionaries containing the available micro periods for the given macro period.

        Args:
            macro_period (str): The macro period to consider (e.g., 'alltime', 'tax year', 'year', 'quarter', 'month', 'week').

        Returns:
            A list of strings containing the available micro periods as options for the input dropdown.
        """
        micro_periods = {'alltime': ['tax year', 'year', 'quarter', 'month', 'week', 'day', 'weekday'],
                         'tax year': ['quarter', 'month', 'week', 'day', 'weekday'],
                         'year': ['quarter', 'month', 'week', 'day', 'weekday'],
                         'quarter': ['month', 'week', 'day', 'weekday', 'date'],
                         'month': ['week', 'day', 'weekday', 'date'],
                         'week': ['day', 'weekday', 'date'],
                         }

        options = []
        for period in micro_periods[macro_period]:
            options.append({'label': period, 'value': period})

        return options

    @staticmethod
    def input_dropdown_column_set(df: pd.DataFrame, column: str) -> list:
        """
        Generate a list of dictionaries containing the unique values in the specified DataFrame column.

        Args:
            df (pd.DataFrame): The DataFrame containing the column to extract unique values from.
            column (str): The column name to extract unique values from.

        Returns:
            A list of strings containing the unique values as options for the input dropdown.
        """
        unique_values = pd.Series(df[column].unique().astype(str)).to_list()
        options = []

        for value in unique_values:
            options.append({'label': value, 'value': value})

        return options
    
    def filter_time_period(df,main_dropdown_value,sub_dropdown_1):
        data = df.copy()
        if main_dropdown_value != 'alltime':
            data = data[data[main_dropdown_value] == sub_dropdown_1]
        else:
            data = data
        return data
