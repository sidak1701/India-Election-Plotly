import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd

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



merged_map_data = pd.read_csv('data/merged_data (1).csv')


def get_party_votes_for_state(state):
  if not state or state == '':
    filtered_merge_df = merge_df.copy()
  else:
    filtered_merge_df = merge_df[merge_df['State'] == state]
  
  display_name = 'Party Votes for All States' if state is None or state  == '' else state

  total_votes = filtered_merge_df.groupby('Party').sum().reset_index()

  top_5 = total_votes.sort_values(by='Total Votes', ascending=False).head()

  fig = px.bar(top_5, x='Party', y='Total Votes', color='Party', title=f'{display_name}')
  
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
  fig.update_layout(title='Distribution of Total Votes over the states')
  fig.update_layout(mapbox_style='carto-positron')
  fig.update_layout(showlegend=False)

  graph_data = json.dumps(fig, cls= plotly.utils.PlotlyJSONEncoder)
  return graph_data

def get_map_data2():
  # generate choropleth map using json
  fig = px.choropleth(
      merged_map_data,
      geojson=merged_map_data.geometry,
      locations=merged_map_data.index,
      color='ID_1',
      color_continuous_scale=px.colors.qualitative.Set3,
      hover_name='state_name',
      hover_data={'Party': True, 'Total Votes': True, 'ID_1': False},
  )

  fig.update_geos(
      center={"lat": 20.5937, "lon": 78.9629},
      fitbounds="locations",
      visible=False,
      projection_scale=7
  )

  # Remove the scale on the side and make it unmovable
  fig.update_layout(coloraxis_showscale=False, dragmode=False)

  # Remove the logo of Plotly and buttons on top
  config = {
      'displayModeBar': False,
      'displaylogo': False,
  }

  graph_data = json.dumps(fig, cls= plotly.utils.PlotlyJSONEncoder)
  return graph_data

def get_piechart_data(state):
  if not state or state == '':
    filtered_merge_df = merge_df.copy()
  else:
    filtered_merge_df = merge_df[merge_df['State'] == state]

  total_votes = filtered_merge_df.groupby('Party').sum().reset_index()

  top_10 = total_votes.sort_values(by='Total Votes', ascending=False).head()

  display_name = 'All States' if state is None or state  == '' else state
  fig = px.pie(top_10, values='Total Votes', names='Party', title=f'Top 5 Party for {display_name}')

  graph_data = json.dumps(fig, cls= plotly.utils.PlotlyJSONEncoder)
  return graph_data

def get_vote_type_distribution(state):

  if not state or state == '':
    filtered_merge_df = merge_df.copy()
  else:
    filtered_merge_df = merge_df[merge_df['State'] == state]
  
  total_votes = filtered_merge_df.groupby('Party').sum().reset_index()

  top_5 = total_votes.sort_values(by='Total Votes', ascending=False).head()

  # Sample data
  # categories = ['Category A', 'Category B', 'Category C']
  # values_stack1 = [10, 15, 20]
  # values_stack2 = [5, 10, 15]

  # Calculate the total for each category
  totals = [v1 + v2 for v1, v2 in zip(top_5['EVM Votes'],top_5['Postal Votes'])]

  # Normalize the values to percentages
  percent_stack1 = [v1 / total * 100 for v1, total in zip(top_5['EVM Votes'], totals)]
  percent_stack2 = [v2 / total * 100 for v2, total in zip(top_5['Postal Votes'], totals)]

  # Create the figure
  fig = go.Figure()

  # Add the first stack (normalized)
  fig.add_trace(go.Bar(
      x=top_5['Party'],
      y=percent_stack1,
      name='EVM Votes',
      marker_color='blue'  # Color for the first stack
  ))

  # Add the second stack (normalized)
  fig.add_trace(go.Bar(
      x=top_5['Party'],
      y=percent_stack2,
      name='Postal Votes',
      marker_color='orange'  # Color for the second stack
  ))

  # Update layout to make it stacked
  fig.update_layout(
      barmode='stack',
      title='Normalized Stacked Bar Chart for Percentage of Vote Types',
      xaxis_title='Categories',
      yaxis_title='Percentage (%)',
      legend_title='Stacks',
      yaxis=dict(tickformat=".1f"),  # Format y-axis as percentage,
  )

  # Pre-zoomed range for y-axis (focus on values between 99 and 100)
  fig.update_layout(
      yaxis=dict(
          title="Values",
          range=[97, 100]  
      )
  )

  # Show the figure
  # fig.show()
  
  graph_data = json.dumps(fig, cls= plotly.utils.PlotlyJSONEncoder)
  return graph_data
  