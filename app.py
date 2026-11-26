"""Telecom traffic forecast map (Telecom Italia, Trentino).

Interactive map of forecast traffic per cell, coloured by utilisation (traffic / assumed capacity).
Run:  streamlit run app.py        (the folder app_data must be next to this file)
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(page_title='Telecom traffic forecast map', layout='wide')
DATA = Path(__file__).resolve().parent / 'app_data'

# traffic level -> colour (red, green, blue, opacity)
COLORS = {'Low': [46, 160, 67, 190], 'Medium': [245, 205, 50, 190], 'High': [245, 130, 32, 205],
          'Over capacity': [205, 40, 40, 225], 'No data': [170, 170, 170, 110]}


@st.cache_data
def load_data():
    fc = pd.read_parquet(DATA / 'forecasts.parquet')
    cells = pd.read_parquet(DATA / 'cells.parquet')
    cells['polygon'] = cells['polygon'].apply(lambda p: [[float(x), float(y)] for x, y in p])   # arrays -> plain lists
    metrics = pd.read_csv(DATA / 'metrics.csv', index_col=0)
    importance = pd.read_csv(DATA / 'feature_importance.csv', index_col=0)
    with open(DATA / 'info.json') as f:
        info = json.load(f)
    return fc, cells, metrics, importance, info


def classify(util):
    return np.select([np.isnan(util), util < 0.5, util < 0.8, util < 1.0],
                     ['No data', 'Low', 'Medium', 'High'], default='Over capacity')


fc, cells, metrics, importance, info = load_data()
dates = info['dates']

# ------------------------------------------------------------------ sidebar controls
st.sidebar.header('Controls')
default_date = '2013-12-28' if '2013-12-28' in dates else dates[-1]
date = st.sidebar.selectbox('Date', dates, index=dates.index(default_date))
hour = st.sidebar.slider('Hour of day', 0, 23, 15)
view = st.sidebar.radio('Show', ['Forecast', 'Actual (where known)'])
headroom = st.sidebar.slider('Assumed capacity = cell\u2019s normal peak (P99) x', 0.8, 2.0, float(info['default_headroom']), 0.05)
uplift = st.sidebar.slider('Demand uplift on the forecast (%)', 0, 50, 0, 5)
st.sidebar.caption(f"In the late-December surge the model under-predicts by about {abs(info['surge_bias_pct']):.0f} %. "
                   'Try an uplift of 15\u201320 % to see the effect.')

# ------------------------------------------------------------------ data for the selected hour
sel = fc[(fc['date'] == date) & (fc['hod'] == hour)].merge(cells, on='cell_id')
value = sel['forecast'] * (1 + uplift / 100) if view == 'Forecast' else sel['actual']
capacity = np.maximum(sel['p99'] * headroom, 1.0)
util = (value / capacity).to_numpy(dtype=float)
sel = sel.assign(value=value, capacity=capacity, util=util, level=classify(util))
sel['color'] = sel['level'].map(COLORS)
sel['tip'] = ('<b>Cell ' + sel['cell_id'].astype(str) + '</b><br/>' + view.split(' ')[0] + ': ' + sel['value'].round(1).astype(str)
              + '<br/>Assumed capacity: ' + sel['capacity'].round(1).astype(str)
              + '<br/>Utilisation: ' + (100 * sel['util']).round(0).astype(str) + ' %<br/>Level: ' + sel['level'])

# ------------------------------------------------------------------ header and key figures
st.title('Telecom traffic forecast map \u2013 Trentino')
st.caption('Internet activity per cell and hour (an activity index, not Mbps). Capacity is an assumption: the dataset has no real capacity.')

known = sel['level'] != 'No data'
n_over, n_high = int((sel['level'] == 'Over capacity').sum()), int((sel['level'] == 'High').sum())
c1, c2, c3, c4 = st.columns(4)
c1.metric('Total traffic shown', f"{sel['value'].sum():,.0f}")
c2.metric('Actual total (where known)', f"{sel['actual'].sum():,.0f}" if sel['actual'].notna().any() else 'no data')
c3.metric('Cells over assumed capacity', f'{n_over}', f'{100 * n_over / max(known.sum(), 1):.1f} % of cells', delta_color='off')
c4.metric('Cells at high level (80\u2013100 %)', f'{n_high}', f'{100 * n_high / max(known.sum(), 1):.1f} % of cells', delta_color='off')

st.markdown('**Traffic level:** \U0001F7E2 Low (< 50 % of capacity) \u00a0 \U0001F7E1 Medium (50\u201380 %) \u00a0 '
            '\U0001F7E0 High (80\u2013100 %) \u00a0 \U0001F534 Over capacity (> 100 %) \u00a0 \u26AA No data')

# ------------------------------------------------------------------ map
layer = pdk.Layer('PolygonLayer', data=sel[['cell_id', 'polygon', 'color', 'tip']], get_polygon='polygon',
                  get_fill_color='color', get_line_color=[70, 70, 70, 70], line_width_min_pixels=0.2,
                  stroked=True, filled=True, pickable=True, auto_highlight=True)
view_state = pdk.ViewState(latitude=float(cells['lat'].mean()), longitude=float(cells['lon'].mean()), zoom=8.3, pitch=0)
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, map_provider='carto', map_style='light',
                         tooltip={'html': '{tip}'}))

# ------------------------------------------------------------------ cells at highest level + cell explorer
left, right = st.columns([1, 2])
top = sel[known].nlargest(10, 'util')
with left:
    st.subheader('Ten busiest cells (vs capacity)')
    st.dataframe(top.assign(utilisation_pct=(100 * top['util']).round(0))[['cell_id', 'value', 'capacity', 'utilisation_pct']]
                 .rename(columns={'value': view.split(' ')[0].lower()}).round(1), hide_index=True)
    options = top['cell_id'].tolist() or cells['cell_id'].head(10).tolist()
    cell_id = st.selectbox('Cell to inspect', options)
    typed = st.text_input('...or type any cell id')
    if typed.strip().isdigit() and int(typed) in set(cells['cell_id']):
        cell_id = int(typed)

with right:
    st.subheader(f'Cell {cell_id}: actual, forecast and assumed capacity')
    ts = fc[fc['cell_id'] == cell_id].copy()
    ts['time'] = pd.to_datetime(ts['date']) + pd.to_timedelta(ts['hod'], unit='h')
    ts = ts.set_index('time').sort_index()[['actual', 'forecast', 'yesterday']]
    ts.columns = ['Actual', 'Forecast', 'Same hour yesterday']
    base = float(cells.loc[cells['cell_id'] == cell_id, 'p99'].iloc[0])
    ts['Assumed capacity'] = max(base * headroom, 1.0)
    st.line_chart(ts)

# ------------------------------------------------------------------ about
with st.expander('About the model and its accuracy'):
    st.write('**Improved method:** XGBoost predicting traffic relative to the cell\u2019s recent level, trained with an absolute-error loss '
             '(weighted by traffic). **Baselines:** same hour last week, same hour yesterday, last week scaled by the recent level change. '
             'Every forecast uses only data at least 24 hours old. Accuracy is the error (WAPE, %) on 600 cells the model never saw.')
    st.dataframe(metrics.round(1))
    st.write('**What the model relies on** (average share of each input in the forecasts, %):')
    st.bar_chart(importance)
    st.write('**Limits:** 62 days of data, one late-December surge that the model under-predicts, and assumed (not real) capacities. '
             'Traffic values are an activity index.')
