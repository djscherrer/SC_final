import pandas as pd
import plotly.graph_objects as go

# Load the data from all sources
sources = ["abstracts", "in_paper", "prompt"]
dataframes = [pd.read_csv(f'../../../raw_data/ratings_{source}.csv', delimiter=',') for source in sources]

# Calculate the average values for each source
average_values_list = []
for df, source in zip(dataframes, sources):
    overall_average = df.mean().reset_index()
    overall_average.columns = ['category', 'value']
    overall_average['source'] = source
    average_values_list.append(overall_average)

# Combine the data into a single DataFrame
combined_df = pd.concat(average_values_list, ignore_index=True)

# Pivot the data to have categories as columns and sources as rows
pivot_df = combined_df.pivot(index='source', columns='category', values='value').reset_index()

# Sort the DataFrame by 'Overall score'
pivot_df = pivot_df.sort_values(by='Overall score', ascending=True).reset_index(drop=True)

# Add a categorical column for sources with the new order
pivot_df['source_code'] = pd.Categorical(pivot_df.index)

# Define the dimensions to be included in the parallel coordinates plot
dimensions = [
    dict(label='Source', values=pivot_df['source_code'], tickvals=list(range(len(pivot_df))),
         ticktext=pivot_df['source']),
    dict(range=[1, 10],
         label='Originality', values=pivot_df['Originality']),
    dict(range=[1, 10],
         label='Method', values=pivot_df['Method']),
    dict(range=[1, 10],
         label='Credibility', values=pivot_df['Credibility']),
    dict(range=[1, 10],
         label='Understandability', values=pivot_df['Understandability']),
    dict(range=[1, 10],
         label='Relevance', values=pivot_df['Relevance']),
    dict(range=[1, 10],
         label='Quality of Citations', values=pivot_df['Quality of Citations']),
    dict(range=[1, 10],
         label='Grammar', values=pivot_df['Linguistic style and soundness of grammar']),
    dict(range=[1, 10],
         label='Overall Score', values=pivot_df['Overall score']),
]

# Create the parallel coordinates plot
fig = go.Figure(data=
    go.Parcoords(
        line=dict(color=pivot_df['Overall score'], colorscale='Viridis', showscale=True),
        dimensions=dimensions
    )
)

# Update layout for better readability
fig.update_layout(
    title='Average ratings of sources across all categories',
    title_font_size=20,
    margin=dict(l=270, t=100),
    width=1500,
    height=800
)

# Save the plot to an HTML file
fig.write_html("html/sources_parallel_coordinates.html")

# Show the plot
fig.show()
