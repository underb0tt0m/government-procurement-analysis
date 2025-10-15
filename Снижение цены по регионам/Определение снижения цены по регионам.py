import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
L = 180

def clean_region_name(name):
    name = re.sub(r'<[^>]+>', '', name).replace('г.', '').replace('г ', '')
    name = name.replace('город ', '').replace('область', 'обл.').replace('Обл.', 'обл.').strip()
    return name

df = pd.read_excel('general_information_about_auctions.xlsx')
dfPlaces = pd.read_excel('89к аукционов с адресами.xlsx')
# Форматирование данных
df['PriceDynamics'] = (
    df['PriceDynamicsString']
    .str.replace(',', '.', regex=False)
    .replace('Не определено', np.nan)
    .astype(float)
)
filtered_df = df
outliers = df['PriceDynamics'][(df['PriceDynamics'] < 0) |
                               (df['PriceDynamics'] > 100) |
                               (df['AuctionDurationSec'] < 0)]
filtered_df = filtered_df[~filtered_df['PriceDynamics'].isin(outliers)]
filtered_df = filtered_df.dropna()

fullDf = pd.merge(filtered_df, dfPlaces, on='idBid', how='inner').dropna()
print(len(fullDf))
fullDf['region'] = [clean_region_name(name.split(',')[1]) for name in list(fullDf.iloc[:, -1])]
print(len(fullDf))
regionDict = {el: 0 for el in set(fullDf['region'])}
for el in regionDict:
    regionDict[el] = list(fullDf['PriceDynamics'][fullDf['region']==el])
regionDict = dict(sorted(regionDict.items()))

regionDict['Амурская обл.'] = regionDict['Амурская обл.'] + regionDict['обл. Амурская']
del regionDict['обл. Амурская']
regionDict['Московская обл.'] = regionDict['Московская обл.'] + regionDict['обл. Московская']
del regionDict['обл. Московская']
regionDict['Свердловская обл.'] = regionDict['Свердловская обл.'] + regionDict['Екатеринбург']
del regionDict['Екатеринбург']
regionDict['Кемеровская обл. - Кузбасс'] = regionDict['Кемеровская Область - Кузбасс обл.']
del regionDict['Кемеровская Область - Кузбасс обл.']
regionDict['Республика Саха (Якутия)'] = regionDict['Республика Саха /Якутия/']
del regionDict['Республика Саха /Якутия/']
regionDict['Ханты-Мансийский АО - Югра'] = regionDict['Ханты-Мансийский Автономный окру- Югра']
del regionDict['Ханты-Мансийский Автономный окру- Югра']
regionDict['Ямало-Ненецкий АО'] = regionDict['Ямало-Ненецкий автономный округ']
del regionDict['Ямало-Ненецкий автономный округ']
regionDict['г. Москва'] = regionDict['Москва']
del regionDict['Москва']
regionDict['г. Санкт-Петербург'] = regionDict['Санкт-Петербург']
del regionDict['Санкт-Петербург']
regionDict['город федерального значения Севастополь'] = regionDict['Севастополь']
del regionDict['Севастополь']

df_for_excel = pd.DataFrame({
    'region': regionDict.keys(),
    'meanPriceDynamics': [np.mean(el) for el in regionDict.values()],
    'sample_size': [len(el) for el in regionDict.values()]
    })

df_for_excel.to_excel('region-meanPriceDynamics.xlsx', index=False)















