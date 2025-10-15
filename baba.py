import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ast
L = 180

df = pd.read_excel('general_information_about_auctions.xlsx')
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
filtered_df['number'] = filtered_df['ParticipantsInfos'].apply(lambda x: len(ast.literal_eval(x)))
