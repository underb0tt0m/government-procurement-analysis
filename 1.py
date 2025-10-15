import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ast
L = 13

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
filtered_df = filtered_df[~filtered_df['number'].isin([0])]

def graphs():

    # Построение боксплота с выбросами
    plt.figure()
    filtered_df['PriceDynamics'].plot.box(
        title='',
        grid=True,
        figsize=(8, 6),
        showfliers=True
    )
    plt.ylabel("Итоговое снижение цены, %")
    plt.xticks([])
    # Построение боксплота без выбросов
    plt.figure()
    filtered_df['PriceDynamics'].plot.box(
        title='',
        grid=True,
        figsize=(8, 6),
        showfliers=False
    )
    plt.ylabel("Итоговое снижение цены, %")
    plt.xticks([])
    # Построение зависимости снижения цены от количества участников и типа шага аукциона
    plt.figure()
    plt.scatter(filtered_df['number'], filtered_df['PriceDynamics'], color='blue', s=10, alpha=0.7)
    plt.title("Зависимость: снижение цены ↔ количество участников", fontsize=14)
    plt.xlabel("Количество участников", fontsize=12)
    plt.ylabel("Итоговое снижение цены, %", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)

    genDict = {el: 0 for el in set(filtered_df['number'])}
    percStDict = {el: 0 for el in set(filtered_df['number'])}
    fixStDict = {el: 0 for el in set(filtered_df['number'])}
    for el in genDict:
        genDict[el] = np.mean(filtered_df['PriceDynamics'][filtered_df['number'] == el])
        percStDict[el] = np.mean(
            filtered_df['PriceDynamics'][
                (filtered_df['number'] == el) & (filtered_df['StepType'] == 'Процент от НМЦ')
                ]
            )
        fixStDict[el] = np.mean(
            filtered_df['PriceDynamics'][
                (filtered_df['number'] == el) & (filtered_df['StepType'] == 'Фиксированная сумма')
                ]
            )
    genDict = dict(sorted({k: genDict[k] for k in genDict if not np.isnan(genDict[k])}.items()))
    percStDict = dict(sorted({k: percStDict[k] for k in percStDict if not np.isnan(percStDict[k])}.items()))
    fixStDict = dict(sorted({k: fixStDict[k] for k in fixStDict if not np.isnan(fixStDict[k])}.items()))

    plt.figure()
    plt.plot(genDict.keys(), genDict.values(), marker='None', linestyle='-', color='blue')
    plt.title("", fontsize=14)
    plt.xlabel("Количество участников", fontsize=12)
    plt.ylabel("Итоговое снижение цены, %", fontsize=12)
    plt.xlim([1, L+1])
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.figure()
    plt.plot(percStDict.keys(), percStDict.values(), marker='o', linestyle='-', color='blue', label='Процент от НМЦ')
    plt.plot(fixStDict.keys(), fixStDict.values(), marker='x', linestyle='-', color='red', label='Фиксированная сумма')
    plt.title("", fontsize=14)
    plt.xlabel("Количество участников", fontsize=12)
    plt.ylabel("Итоговое снижение цены, %", fontsize=12)
    plt.xlim([1, L+1])
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    # Построение зависимости снижения цены от наличия второй фазы
    plt.figure()
    plt.boxplot([filtered_df['PriceDynamics'][filtered_df['WithSecondPhase']==False],
                 filtered_df['PriceDynamics'][filtered_df['WithSecondPhase']==True]])
    plt.title('')
    plt.ylabel('Итоговое снижение цены, %')
    plt.xticks([1, 2], ['Без второй фазы', 'Со второй фазой'])
    plt.grid(True, linestyle='--', alpha=0.5)

    print('Данные по боксплоту общего распределения снижения цены')
    print(filtered_df['PriceDynamics'].describe())
    print('Данные по боксплоту распределения снижения цены для аукционов без второй фазы')
    print(filtered_df['PriceDynamics'][filtered_df['WithSecondPhase']==False].describe())
    print('Данные по боксплоту распределения снижения цены для аукционов со второй фазой')
    print(filtered_df['PriceDynamics'][filtered_df['WithSecondPhase']==True].describe())

    bidCountFreq = {i: list(filtered_df['number']).count(i) for i in set(filtered_df['number'])}
    bidCountFreq = dict(sorted(bidCountFreq.items()))
    plt.figure()
    plt.bar(
        bidCountFreq.keys(),
        [count / 1000 for count in bidCountFreq.values()],
        color='blue',
        alpha=0.7
        )
    plt.xlabel("Количество участников", fontsize=12)
    plt.ylabel("Частота, тыс.", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlim(0, 15)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))

def corrMatrix():
    corr_df = filtered_df.iloc[:, [3, -2, -1, 6]]
    corr_df = corr_df[corr_df['number']<=L]
    corr_df.rename(columns={'StartingPrice': 'Начальная цена лота',
                            'PriceDynamics': 'Итоговое снижение цены',
                            'number': 'Количество участников аукциона',
                            'AuctionDurationSec': 'Длительность аукциона'}, inplace = True)
    correlation_matrix = corr_df.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='Greys')
    plt.title('', pad=20)

corrMatrix()
#graphs()

plt.show()  # Показать график

