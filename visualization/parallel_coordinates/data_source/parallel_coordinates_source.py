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
new_df = combined_df.pivot(index='source', columns='category', values='value').reset_index()

# Sort the DataFrame by 'Overall score'
new_df = new_df.sort_values(by='Overall score', ascending=True).reset_index(drop=True)

# Add a categorical column for sources with the new order
new_df['source_code'] = pd.Categorical(new_df.index)

# Define the dimensions to be included in the parallel coordinates plot, use 1-10
dimensions = [
    dict(label='Source', values=new_df['source_code'], tickvals=list(range(len(new_df))),
         ticktext=new_df['source']),
    dict(range=[1, 10],
         label='Originality', values=new_df['Originality']),
    dict(range=[1, 10],
         label='Method', values=new_df['Method']),
    dict(range=[1, 10],
         label='Credibility', values=new_df['Credibility']),
    dict(range=[1, 10],
         label='Understandability', values=new_df['Understandability']),
    dict(range=[1, 10],
         label='Relevance', values=new_df['Relevance']),
    dict(range=[1, 10],
         label='Quality of Citations', values=new_df['Quality of Citations']),
    dict(range=[1, 10],
         label='Grammar', values=new_df['Linguistic style and soundness of grammar']),
    dict(range=[1, 10],
         label='Overall Score', values=new_df['Overall score']),
]

# Create the parallel coordinates plot
fig = go.Figure(data=
    go.Parcoords(
        line=dict(color=new_df['Overall score'], colorscale='Viridis', showscale=True),
        dimensions=dimensions
    )
)

# Update layout for better readability
fig.update_layout(
    title='Average ratings of sources across all categories',
    title_font_size=20,
    margin=dict(l=270, t=100),
    width=1400,
    height=800
)

# Save the plot to an HTML file
fig.write_html("html/sources_parallel_coordinates.html")

# Show the plot
fig.show()
