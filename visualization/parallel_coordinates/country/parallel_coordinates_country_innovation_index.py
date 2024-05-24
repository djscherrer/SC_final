import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Load the data, if you want to change the dataset, do it here
source = "abstracts"
# source = "in_paper"
# source = "prompt"
raw_df = pd.read_csv(f'../../../raw_data/ratings_{source}.csv', delimiter=',')

# Load the global innovation index data
innovation_index_df = pd.read_csv('../../../raw_data/global_innovation_index.csv', delimiter=',')

# Calculate the average values for each country
average_values = raw_df.groupby('country_association').mean().reset_index()

# Replace missing values with NaN if needed
innovation_index_df['global_innovation_index'] = innovation_index_df['global_innovation_index'].replace('', np.nan)

# Merge the average values with the global innovation index data
merged_df = pd.merge(average_values, innovation_index_df, left_on='country_association', right_on='country_association', how='left')

# Sort the DataFrame by 'Overall score'
merged_df = merged_df.sort_values(by='Overall score', ascending=True).reset_index(drop=True)

# Add a categorical column for country names with the new order
merged_df['country_code'] = pd.Categorical(merged_df.index)

# Define the dimensions to be included in the parallel coordinates plot
dimensions = [
    dict(label='Country', values=merged_df['country_code'], tickvals=list(range(len(merged_df))),
         ticktext=merged_df['country_association']),
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
    dict(range=[merged_df['global_innovation_index'].min(), merged_df['global_innovation_index'].max()],
         label='Global Innovation Index', values=merged_df['global_innovation_index'])
]

# Create the parallel coordinates plot
fig = go.Figure(data=
go.Parcoords(
    line=dict(color=merged_df['Overall score'], colorscale='Viridis', showscale=True),
    dimensions=dimensions
)
)

# Update layout for better readability
fig.update_layout(
    title=f'Average ratings of country in all dimensions including Global Innovation Index ({source} data set)',
    title_font_size=20,
    margin=dict(l=270, t=100),
    width=1500,
    height=800
)

fig.write_html(f"html/country_with_innovation_index_{source}_parallel_coordinates.html")

# Show the plot
fig.show()
