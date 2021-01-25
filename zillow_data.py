import pandas as pd
import os
from datetime import datetime

path = os.getcwd()


def get_zillow_data(date_columns):

    with open(os.path.join(path, 'files/County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_mon.csv')) as file:
        df = pd.read_csv(file, converters={'StateCodeFIPS':str,'MunicipalCodeFIPS':str})
        column_dict = {}



        for col in df.columns.values:
            if '-' in col:
                date_parse = col.split('-')
                column_dict[col] = date_parse[0] + '-' + date_parse[1] + '-01'


        df = df.rename(columns=column_dict)
        date_columns = sorted([str(datetime.strptime(dt, "%m-%d-%Y").date()) for dt in date_columns])
        df = df[(['StateCodeFIPS','MunicipalCodeFIPS','RegionName'] + date_columns)]

        df[date_columns] = df[date_columns].pct_change(axis='columns').fillna(0)
        df = df.melt(id_vars=['StateCodeFIPS', 'MunicipalCodeFIPS','RegionName'], var_name='Date', value_name='Quarterly Price Change')
        df['CountyFIPS'] = df['StateCodeFIPS'] + df['MunicipalCodeFIPS']
        df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")

        return df.drop(columns=['StateCodeFIPS','MunicipalCodeFIPS'])


