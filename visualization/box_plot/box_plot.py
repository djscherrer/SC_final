import pandas as pd
import plotly.express as px

# Load the data
# source = "abstracts"
# source = "in_paper"
source = "prompt"
raw_df = pd.read_csv(f'../../raw_data/ratings_{source}.csv', delimiter=',')

# "Melt" the df to match required format
melted_df = raw_df.melt(id_vars=['country_association'],
                        value_vars=['Originality',
                                    'Method',
                                    'Credibility',
                                    'Understandability',
                                    'Relevance',
                                    'Quality of Citations',
                                    'Linguistic style and soundness of grammar',
                                    'Overall score'],
                        var_name='Category', value_name='Score')
melted_df['Category'] = melted_df['Category'].replace('Linguistic style and soundness of grammar', 'Grammar')

# Create the boxplot
fig = px.box(melted_df, x='Category', y='Score', title=f'Boxplot of ratings for each category ({source} data set)')

# Update layout for better readability
fig.update_layout(
    title_font_size=20,
    margin=dict(l=100, r=100, t=100, b=100),
    width=1500,
    height=800,
    yaxis=dict(range=[1, 10])
)

# Save the plot to an HTML file
fig.write_html(f"html/category_{source}_boxplot.html")

# Show the plot
fig.show()
