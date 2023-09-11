from RussianPostIndexes import resource_path
import os
import sqlite3
import pandas as pd
import numpy as np

base_name = 'PIndx16.dbf'
target_name = 'PIndx16.db'
# Формируем команду для вызова dbf-to-sqlite
command = f'dbf-to-sqlite {resource_path(base_name)} {resource_path(target_name)}'
os.system(command)

con = sqlite3.connect(resource_path('PIndx16.db'))
df = pd.read_sql('SELECT * FROM PIndx16', con=con)
df.drop(columns=['actdate', 'indexold', 'opstype'], inplace=True)
# Объединяем Region и Autonom, результат сохраняем в Region
df['region'] = df['region'].combine_first(df['autonom'])
# Удаляем колонку Autonom
df.drop(columns=['autonom'], inplace=True)
df['region'] = df['region'].str.strip().replace('', np.nan)
df['area'] = df['area'].str.strip().replace('', np.nan)
df['city'] = df['city'].str.strip().replace('', np.nan)
df['city_1'] = df['city_1'].str.strip().replace('', np.nan)
# Формируем новую колонку, где region, area, city и city1 через запятую, а оригиналы удаляем
df['Location'] = df[['region', 'area', 'city', 'city_1']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df.drop(columns=['region', 'area', 'city', 'city_1'], inplace=True)
csv_filename = 'PIndx16.csv'
# Сохраняем DataFrame в Excel
df.to_csv(csv_filename, index=False)
