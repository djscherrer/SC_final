import pandas as pd
import plotly.graph_objects as go

# Load the data, if you want to change the dataset, do it here
source = "abstracts"
# source = "in_paper"
# source = "prompt"
raw_df = pd.read_csv(f'../../../raw_data/ratings_{source}.csv', delimiter=',')

# Dictionary to map field codes to field names
field_dict = {"EM": "economics",
              "CP": "quantitative finance",
              "AT": "mathematics",
              "AP": "statistics",
              "AI": "computer science"}

# Create a new DataFrame to store aggregated ratings by field
field_ratings = pd.DataFrame()

# Iterate through each field code to aggregate ratings
for field_code, field_name in field_dict.items():
    # Filter the dataframe for the current field
    field_df = raw_df[raw_df['title'].str.contains(field_code, case=False, na=False)]

    # Calculate the average values for each rating dimension
    average_values = field_df.mean().to_frame().transpose()

    # Add the field name as a column
    average_values['Field'] = field_name

    # Append the average values to the field_ratings df
    field_ratings = pd.concat([field_ratings, average_values], ignore_index=True)

# Add a categorical column for field names with the new order
field_ratings['Field_code'] = pd.Categorical(field_ratings.index)

# Define the dimensions to be included in the parallel coordinates plot
dimensions = [
    dict(label='Field', values=field_ratings['Field_code'], tickvals=list(range(len(field_ratings))),
         ticktext=field_ratings['Field']),
    dict(range=[field_ratings['Originality'].min(), field_ratings['Originality'].max()],
         label='Originality', values=field_ratings['Originality']),
    dict(range=[field_ratings['Method'].min(), field_ratings['Method'].max()],
         label='Method', values=field_ratings['Method']),
    dict(range=[field_ratings['Credibility'].min(), field_ratings['Credibility'].max()],
         label='Credibility', values=field_ratings['Credibility']),
    dict(range=[field_ratings['Understandability'].min(), field_ratings['Understandability'].max()],
         label='Understandability', values=field_ratings['Understandability']),
    dict(range=[field_ratings['Relevance'].min(), field_ratings['Relevance'].max()],
         label='Relevance', values=field_ratings['Relevance']),
    dict(range=[field_ratings['Quality of Citations'].min(), field_ratings['Quality of Citations'].max()],
         label='Quality of Citations', values=field_ratings['Quality of Citations']),
    dict(range=[field_ratings['Linguistic style and soundness of grammar'].min(),
                field_ratings['Linguistic style and soundness of grammar'].max()],
         label='Grammar', values=field_ratings['Linguistic style and soundness of grammar']),
    dict(range=[field_ratings['Overall score'].min(), field_ratings['Overall score'].max()],
         label='Overall Score', values=field_ratings['Overall score']),
]

# Create the parallel coordinates plot
fig = go.Figure(data=
go.Parcoords(
    line=dict(color=field_ratings['Overall score'], colorscale='Viridis', showscale=True),
    dimensions=dimensions
)
)

# Update layout for better readability
fig.update_layout(
    title=f'Average ratings for each field in all dimensions ({source} data set)',
    title_font_size=20,
    margin=dict(l=270, t=100),
    width=1500,
    height=800
)

# Save the plot to HTML
fig.write_html(f"html/field_{source}_parallel_coordinates.html")

# Show the plot
fig.show()
