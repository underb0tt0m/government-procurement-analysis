import geopandas as gpd
import pandas as pd
from matplotlib import pyplot as plt
from shapely.ops import transform
import numpy as np
scheme_method = [
    'boxplot', 'equalinterval', 'fisherjenks',
    'fisherjenkssampled', 'headtailbreaks',
    'jenkscaspall', 'jenkscaspallforced', 'jenkscaspallsampled',
    'maxp', 'maximumbreaks', 'naturalbreaks', 'quantiles', 'percentiles',
    'prettybreaks', 'stdmean'
    ]


#url = "https://raw.githubusercontent.com/timurkanaz/Russia_geojson_OSM/master/GeoJson's/Countries/Russia_regions.geojson"
#districts.to_file("Карта России.geojson", driver="GeoJSON")
russia_regions = gpd.read_file("Карта России.geojson")
region_meanPriceDynamics = gpd.read_file("region-meanPriceDynamics.xlsx")
russia_regions = pd.merge(russia_regions, region_meanPriceDynamics, how='left')
russia_regions['sample_size'] = russia_regions['sample_size'].fillna(0)
russia_regions.head()
'''
for method in scheme_method:
    ax = russia_regions.plot(column='meanPriceDynamics',
                             missing_kwds={'color': 'lightgrey', 'label': 'Данные отсутствуют'},
                             scheme=method, 
                             figsize=(10,6),
                             cmap='RdYlGn', #viridis, Blues, RdYlGn
                             alpha=0.5,
                             linewidth=1,
                             edgecolor='black',
                             legend=True)
    ax.set_title(method, fontsize=16, pad=20)
    plt.savefig(f'{method}.png', dpi=300, bbox_inches='tight')
'''
# Построение карты среднего снижения цены по регионам
ax = russia_regions.plot(
    column='meanPriceDynamics',
    missing_kwds={'color': 'lightgrey', 'label': 'Данные отсутствуют', 'linewidth': 0.5},
    scheme='prettybreaks',
    figsize=(10,6),
    cmap='bone', #viridis, Blues, RdYlGn
    alpha=0.5,
    linewidth=0.5,
    edgecolor='black',
    legend=True,
    legend_kwds={
        'fmt': "{:.1f}",
        'title': 'Снижение цены, %',
        'title_fontsize': 8,
        'fontsize': 8,
        'markerscale': 0.6,
        'framealpha': 0.5,
        'borderpad': 0.3,
        'labelspacing': 0.3
        }
    )
ax.set_axis_off()
legend = ax.get_legend()
for text in legend.get_texts():
        current_text = text.get_text()
        if ',' in current_text:
            new_text = current_text.replace(' ', '').replace(',', '-')
            text.set_text(new_text)
plt.savefig(f'Снижение цены по регионам.png', dpi=300, bbox_inches='tight')

# Построение карты размера выборки по регионам
custom_bins = [0, 10, 50, 100, 500, 1000]
ax1 = russia_regions.plot(
    column='sample_size',
    scheme='User_Defined',
    classification_kwds={'bins': custom_bins},
    figsize=(10,6),
    cmap='bone', #viridis, Blues, RdYlGn
    alpha=0.5,
    linewidth=0.5,
    edgecolor='black',
    legend=True,
    legend_kwds={
        'fmt': "{:.0f}",
        'title': 'Размер выборки',
        'title_fontsize': 8,
        'fontsize': 8,
        'markerscale': 0.6,
        'framealpha': 0.5,
        'borderpad': 0.3,
        'labelspacing': 0.3
        }
    )
legend = ax1.get_legend()
for text in legend.get_texts():
        current_text = text.get_text()
        if current_text == '   0,    0':
                new_text = '0'
                text.set_text(new_text)
                continue
        if ',' in current_text:
            new_text = current_text.replace(' ', '').replace(',', '-')
            text.set_text(new_text)
ax1.set_axis_off()
plt.savefig(f'Размер выборки по регионам.png', dpi=300, bbox_inches='tight')

plt.show()


