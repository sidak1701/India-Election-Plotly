import pandas as pd
import json
import plotly
import plotly.express as px

df_cor = pd.read_csv('data/India States-UTs.csv')
df_eci = pd.read_csv('data/eci_data_2024.csv', encoding='mac_roman')


df_eci[['EVM Votes', 'Postal Votes', 'Total Votes']] = df_eci[['EVM Votes', 'Postal Votes', 'Total Votes']] \
  .apply(pd.to_numeric, errors='coerce')

# Group by State and Party, then sum the remaining columns
result = df_eci.groupby(['State', 'Party'], as_index=False)[['EVM Votes', 'Postal Votes', 'Total Votes']].sum()

column={
  'Andaman and Nicobar Islands': 'Andaman & Nicobar Islands', 
  'Dadra and Nagar Haveli and Daman and Diu': 'Dadra & Nagar Haveli and Daman & Diu',
  'Delhi':'NCT OF Delhi',
}

for i in column:
    df_cor = df_cor.replace(i,column[i])

merge_df = result.merge(df_cor, how='left', left_on='State', right_on='State/UT')
merge_df = merge_df.drop(columns=['State/UT'])


def get_party_votes_for_state(state):
  filtered_merge_df = merge_df[merge_df['State'] == state]
  total_votes = filtered_merge_df.groupby('Party').sum().reset_index()

  top_5 = total_votes.sort_values(by='Total Votes', ascending=False).head()

  fig = px.bar(top_5, x='Party', y='Total Votes', color='Party')
  fig.update_layout(showlegend=False)

  graph_data = json.dumps(fig, cls= plotly.utils.PlotlyJSONEncoder)
  return graph_data


def get_map_data():
  fig = px.scatter_mapbox(
    merge_df, 
    lat='Latitude', lon='Longitude', 
    zoom=3, 
    height=500, 
    size='Total Votes'
    # color_discrete_map=Utils.color_map()
  )
  fig.update_layout(title='')
  fig.update_layout(mapbox_style='carto-positron')
  fig.update_layout(showlegend=False)

  graph_data = json.dumps(fig, cls= plotly.utils.PlotlyJSONEncoder)
  return graph_data


def get_piechart_data(state):
  filtered_merge_df = merge_df[merge_df['State'] == state]
  total_votes = filtered_merge_df.groupby('Party').sum().reset_index()

  top_10 = total_votes.sort_values(by='Total Votes', ascending=False).head()

  fig = px.pie(top_10, values='Total Votes', names='Party', title='')

  graph_data = json.dumps(fig, cls= plotly.utils.PlotlyJSONEncoder)
  return graph_data