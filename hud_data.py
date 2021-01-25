import pandas as pd
import os
import re
import zillow_data

final_df = pd.DataFrame()

path = os.getcwd() + '/files'
for filename in os.listdir(path):
    if '90_Day_Defaults' in filename:
        data_column = '90 Days Delinquent'
        with open(os.path.join(path, filename)) as file:
            df = pd.read_csv('files/Single_Family_FHA_90_Day_Defaults_by_Tract.csv', converters={'STATEFP':str,'COUNTYFP':str})
    elif 'Active_Foreclosure' in filename:
        data_column = 'Active Foreclosures'
        with open(os.path.join(path, filename)) as file:
            df = pd.read_csv('files/Single_Family_FHA_Mortgages_in_Active_Foreclosure_by_Tract.csv', converters={'STATEFP':str,'COUNTYFP':str})
    else:
        continue

    columns_to_keep = ['STATEFP','COUNTYFP']
    date_columns_dict = {}

    for col in df.columns.values:
        if 'DEFAULTS_90_DAY' in col or 'FORECLOSURES_' in col:
            columns_to_keep.append(col)
            year = re.findall("(\d\d\d\d)", col)
            month = col[-2:]

            date_columns_dict[col] = col[-2:] + '-01-' + str(year[0])

    df = df[columns_to_keep]
    df['CountyFIPS'] = df['STATEFP'] + df['COUNTYFP']
    df = df.drop(columns=['STATEFP','COUNTYFP'])
    df = df.melt(id_vars=['CountyFIPS'], var_name='Date', value_name=data_column)
    df[data_column] = df[data_column].fillna(0)
    df[data_column][df[data_column] < 0] = 0
    df['Date'] = df['Date'].replace(date_columns_dict)
    df = df.groupby(['CountyFIPS','Date'], as_index=False).sum()

    if final_df.empty:
        final_df = df
    else:
        final_df = pd.merge(final_df, df, how='inner', left_on=['CountyFIPS','Date'], right_on=['CountyFIPS','Date'])



zillow_data = zillow_data.get_zillow_data(list(final_df['Date'].drop_duplicates()))

final_df['Date'] = pd.to_datetime(final_df['Date'], format="%m-%d-%Y")

final_df = pd.merge(final_df, zillow_data, how='inner', left_on=['CountyFIPS', 'Date'], right_on=['CountyFIPS', 'Date'])
final_df = final_df.melt(id_vars=['CountyFIPS','Date','RegionName'], var_name='Variable', value_name='Value')



final_df.to_csv('files/data.csv',index=False)

