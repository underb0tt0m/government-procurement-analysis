import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
L = 180

dfOrgs = pd.read_excel('89к извещений и обеспечений.xlsx')
dfPlaces = pd.read_excel('89к аукционов с адресами.xlsx')

# 1. Merge по id (приоритетный способ)
df1 = dfOrgs.merge(
    dfPlaces[['idBid', 'place']],
    on='idBid',
    how='left'
)

# 2. Выделяем строки, где адрес не найден
missing_address = df1[df1['place'].isna()]

# 3. Объединяем их по organizer (для восстановления адресов по названию)
recovered = missing_address.drop(columns='place').merge(
    dfPlaces[['organizator', 'place']].drop_duplicates(),
    on='organizator',
    how='left'
)

# 4. Объединяем обратно с теми, у кого уже есть адрес
filled = pd.concat([
    df1[~df1['place'].isna()],
    recovered
], ignore_index=True)

'''
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

'''
