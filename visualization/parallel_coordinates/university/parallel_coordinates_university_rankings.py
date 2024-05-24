import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Load the data, if you want to change the dataset, do it here
source = "abstracts"
# source = "in_paper"
# source = "prompt"
raw_df = pd.read_csv(f'../../../raw_data/ratings_{source}.csv', delimiter=',')

# Load the ranking data
rankings_df = pd.read_csv('../../../raw_data/ranking.csv', delimiter=',')

# Calculate the average values for each university
average_values = raw_df.groupby('university_association').mean().reset_index()

# Replace missing values with NaN
rankings_df['times_higher_education'] = rankings_df['times_higher_education'].replace('', np.nan)
rankings_df['qs_world'] = rankings_df['qs_world'].replace('', np.nan)

# Merge the average values with the ranking data
merged_df = pd.merge(average_values, rankings_df, on='university_association', how='left')

# Sort the DataFrame by 'Overall score'
merged_df = merged_df.sort_values(by='Overall score', ascending=True).reset_index(drop=True)

# Add a categorical column for university names with the new order
merged_df['university_code'] = pd.Categorical(merged_df.index)

# Define the dimensions to be included in the parallel coordinates plot
dimensions = [
    dict(label='University', values=merged_df['university_code'], tickvals=list(range(len(merged_df))),
         ticktext=merged_df['university_association']),
    dict(range=[merged_df['Originality'].min(), merged_df['Originality'].max()],
         label='Originality', values=merged_df['Originality']),
    dict(range=[merged_df['Method'].min(), merged_df['Method'].max()],
         label='Method', values=merged_df['Method']),
    dict(range=[merged_df['Credibility'].min(), merged_df['Credibility'].max()],
         label='Credibility', values=merged_df['Credibility']),
    dict(range=[merged_df['Understandability'].min(), merged_df['Understandability'].max()],
         label='Understandability', values=merged_df['Understandability']),
    dict(range=[merged_df['Relevance'].min(), merged_df['Relevance'].max()],
         label='Relevance', values=merged_df['Relevance']),
    dict(range=[merged_df['Quality of Citations'].min(), merged_df['Quality of Citations'].max()],
         label='Quality of Citations', values=merged_df['Quality of Citations']),
    dict(range=[merged_df['Linguistic style and soundness of grammar'].min(),
                merged_df['Linguistic style and soundness of grammar'].max()],
         label='Grammar', values=merged_df['Linguistic style and soundness of grammar']),
    dict(range=[merged_df['Overall score'].min(), merged_df['Overall score'].max()],
         label='Overall Score', values=merged_df['Overall score']),
    dict(range=[1401, 1],
         label='QS World', values=merged_df['qs_world'])
]

# Put this inside dimensions to also visualize "times higher education ranking"
"""
dict(range=[1401, 1],
     label='Times Higher Education', values=merged_df['times_higher_education'],
     constraintrange=[1, merged_df['times_higher_education'].max()]), # needed because of NaN values
 """

# Create the parallel coordinates plot
fig = go.Figure(data=
go.Parcoords(
    line=dict(color=merged_df['Overall score'], colorscale='Viridis', showscale=True),
    dimensions=dimensions
)
)

# Update layout for better readability
fig.update_layout(
    title=f'Average ratings of university in all dimensions including ranking ({source} data set)',
    title_font_size=20,
    margin=dict(l=270, t=100),
    width=1400,
    height=800
)

fig.write_html(f"html/university_with_ranking_{source}_parallel_coordinates.html")

# Show the plot
fig.show()
