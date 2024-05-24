import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os

# Initialize the app
app = dash.Dash(__name__)
app.title = "Interactive Bar Chart with Filters"

# Translate the tags to the actual research fields
field_dict = {
    "All": "All Fields",
    "EM": "Economics",
    "CP": "Quantitative Finance",
    "AT": "Mathematics",
    "AP": "Statistics",
    "AI": "Computer Science"
}

# Translate the source path to more readable source name
source_dict = {
    "abstracts": "Only abstracts",
    "in_paper": "Inside paper",
    "prompt": "Inside prompt"
}

# Split all possible filters into same size divs, style them and define possible values
app.layout = html.Div([
    html.Div([
        html.H1(
            "Interactive Bar Chart with Filters",
            style={'text-align': 'center', 'font-family': 'Arial, sans-serif', 'font-size': '1.5em',
                   'margin-bottom': '20px', 'color': '#2C3E50'}
        ),
    ]),

    html.Div([
        html.Div([
            html.Label("Data Source", style={'font-weight': 'bold', 'font-size': '1.2em', 'color': '#2C3E50'}),
            dcc.Dropdown(
                id='data-source',
                options=[{'label': values, 'value': keys} for keys, values in source_dict.items()],
                value='abstracts',
                style={'width': '100%', 'font-size': '1em'}
            )
        ], style={'display': 'inline-block', 'width': '23%', 'padding': '3px', 'vertical-align': 'top'}),

        html.Div([
            html.Label("Field Filter", style={'font-weight': 'bold', 'font-size': '1.2em', 'color': '#2C3E50'}),
            dcc.Dropdown(
                id='field-filter',
                options=[{'label': values, 'value': keys} for keys, values in field_dict.items()],
                value='All',  # Default value
                style={'width': '100%', 'font-size': '1em'}
            )
        ], style={'display': 'inline-block', 'width': '23%', 'padding': '3px', 'vertical-align': 'top'}),

        html.Div([
            html.Label("Selected Dimensions", style={'font-weight': 'bold', 'font-size': '1.2em', 'color': '#2C3E50'}),
            dcc.Dropdown(
                id='selected-dimensions',
                options=[
                    {'label': 'Originality', 'value': 'Originality'},
                    {'label': 'Method', 'value': 'Method'},
                    {'label': 'Credibility', 'value': 'Credibility'},
                    {'label': 'Understandability', 'value': 'Understandability'},
                    {'label': 'Relevance', 'value': 'Relevance'},
                    {'label': 'Quality of Citations', 'value': 'Quality of Citations'},
                    {'label': 'Grammar', 'value': 'Linguistic style and soundness of grammar'},
                    {'label': 'Overall Score', 'value': 'Overall score'}
                ],
                value=['Overall score'],
                multi=True,
                style={'width': '100%', 'font-size': '1em'}
            )
        ], style={'display': 'inline-block', 'width': '23%', 'padding': '3px', 'vertical-align': 'top'}),

        html.Div([
            html.Label("Sort By", style={'font-weight': 'bold', 'font-size': '1.2em', 'color': '#2C3E50'}),
            dcc.Dropdown(
                id='sort-by',
                options=[
                    {'label': 'Originality', 'value': 'Originality'},
                    {'label': 'Method', 'value': 'Method'},
                    {'label': 'Credibility', 'value': 'Credibility'},
                    {'label': 'Understandability', 'value': 'Understandability'},
                    {'label': 'Relevance', 'value': 'Relevance'},
                    {'label': 'Quality of Citations', 'value': 'Quality of Citations'},
                    {'label': 'Grammar', 'value': 'Linguistic style and soundness of grammar'},
                    {'label': 'Overall Score', 'value': 'Overall score'}
                ],
                value='Overall score',
                style={'width': '100%', 'font-size': '1em'}
            )
        ], style={'display': 'inline-block', 'width': '23%', 'padding': '3px', 'vertical-align': 'top'}),

        html.Div([
            html.Label("Group By", style={'font-weight': 'bold', 'font-size': '1.2em', 'color': '#2C3E50'}),
            dcc.RadioItems(
                id='group-by',
                options=[
                    {'label': 'University', 'value': 'university_association'},
                    {'label': 'Country', 'value': 'country_association'}
                ],
                value='university_association',
                labelStyle={'display': 'inline-block', 'margin-right': '10px', 'font-size': '1em', 'color': '#2C3E50'}
            )
        ], style={'display': 'inline-block', 'width': '23%', 'padding': '3px', 'vertical-align': 'top'}),
    ], style={'display': 'flex', 'justify-content': 'space-around', 'flex-wrap': 'wrap', 'margin-bottom': '5px'}),

    dcc.Graph(id='bar-chart', style={'height': '700px'})
])


@app.callback(
    Output('bar-chart', 'figure'),
    Input('data-source', 'value'),
    Input('field-filter', 'value'),
    Input('group-by', 'value'),
    Input('selected-dimensions', 'value'),
    Input('sort-by', 'value')
)
def update_bar_chart(data_source, field_filter, group_by, selected_dimensions, sort_by):
    # Construct the file path
    file_path = f'../../raw_data/ratings_{data_source}.csv'

    # Check if the file exists, if not don't show something (avoid errors)
    if not os.path.exists(file_path):
        return {
            'data': [],
            'layout': {
                'title': 'Error: Data source file not found!'
            }
        }

    # Load the data, if not possible don't show something (avoid errors)
    try:
        raw_df = pd.read_csv(file_path, delimiter=',')
    except Exception as e:
        print(f"Error loading data source {data_source}: {e}")
        return {
            'data': [],
            'layout': {
                'title': 'Error: Unable to load data!'
            }
        }

    # Filter the data based on the selected field with special case if you want all fields
    if field_filter == 'All':
        filtered_df = raw_df
    else:
        filtered_df = raw_df[raw_df['title'].str.contains(field_filter, case=False, na=False)]

    # Calculate the average values for each group
    average_values = filtered_df.groupby(group_by).mean().reset_index()

    # Sort the data by the selected dimension
    average_values = average_values.sort_values(by=sort_by, ascending=True)

    # Create the bar chart
    figure = px.bar(
        average_values,
        x=group_by,
        y=selected_dimensions,
        barmode='group',
        labels={group_by: group_by.replace('_', ' ').title()},
        title=f'Average ratings by {group_by.replace("_", " ").title().lower()} sorted by {sort_by.replace("_", " ").title().lower()}'
    )

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
