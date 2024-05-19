import pandas as pd
import plotly.graph_objects as go

# Load the data, if you want to change the dataset, do it here
source = "abstracts"
# source = "in_paper"
# source = "prompt"
raw_df = pd.read_csv(f'../../raw_data/ratings_{source}.csv', delimiter=',')

# Calculate the average values for each university
average_values = raw_df.groupby('country_association').mean().reset_index()

# Sort the DataFrame by 'Overall score'
average_values = average_values.sort_values(by='Overall score', ascending=True).reset_index(drop=True)

# Add a categorical column for country names with the new order
average_values['country_code'] = pd.Categorical(average_values.index)

# Define the dimensions to be included in the parallel coordinates plot
dimensions = [
    dict(label='Country', values=average_values['country_code'], tickvals=list(range(len(average_values))),
         ticktext=average_values['country_association']),
    dict(range=[average_values['Originality'].min(), average_values['Originality'].max()],
         label='Originality', values=average_values['Originality']),
    dict(range=[average_values['Method'].min(), average_values['Method'].max()],
         label='Method', values=average_values['Method']),
    dict(range=[average_values['Credibility'].min(), average_values['Credibility'].max()],
         label='Credibility', values=average_values['Credibility']),
    dict(range=[average_values['Understandability'].min(), average_values['Understandability'].max()],
         label='Understandability', values=average_values['Understandability']),
    dict(range=[average_values['Relevance'].min(), average_values['Relevance'].max()],
         label='Relevance', values=average_values['Relevance']),
    dict(range=[average_values['Quality of Citations'].min(), average_values['Quality of Citations'].max()],
         label='Quality of Citations', values=average_values['Quality of Citations']),
    dict(range=[average_values['Linguistic style and soundness of grammar'].min(),
                average_values['Linguistic style and soundness of grammar'].max()],
         label='Grammar', values=average_values['Linguistic style and soundness of grammar']),
    dict(range=[average_values['Overall score'].min(), average_values['Overall score'].max()],
         label='Overall Score', values=average_values['Overall score']),
]

# Create the parallel coordinates plot
fig = go.Figure(data=
go.Parcoords(
    line=dict(color=average_values['Overall score'], colorscale='Viridis', showscale=True),
    dimensions=dimensions
)
)

# Update layout for better readability
fig.update_layout(
    title=f'Average ratings of country in all dimensions and the {source} data set',
    title_font_size=20,
    margin=dict(l=270, t=100),
    width=1500,
    height=800
)

fig.write_html(f"../html/country_{source}_parallel_coordinates.html")

# Show the plot
fig.show()
