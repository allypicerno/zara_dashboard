import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
#pip install xlrd

df = pd.read_excel('fashion_data_2018_2022.xls')
df = df[['price', 'year_of_sale', 'category', 'average_rating', 'age_group', 'gender']].dropna()



# Create Dash app
app = Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H4('Interactive line graph with Dash'),
    html.P('Select category: '),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': cat, 'value': cat} for cat in df['category'].unique()],
        value=df['category'].unique()[0],
        clearable=True
    ),
    dcc.Graph(id='graph'),
    html.Br(),
    html.P('Filter by age group: '),
    dcc.Checklist(
        id='age-group-checklist',
        options=[{'label': ag, 'value': ag} for ag in df['age_group'].unique()],
        value=df['age_group'].unique(),
        inline=True)])

# Define callback to update the graph
@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown', 'value'),
     Input('age-group-checklist', 'value')]
)
def update_graph(selected_category, selected_age_groups):
    filtered_data = df[df['category'] == selected_category]
    if selected_age_groups:
        filtered_data = filtered_data[filtered_data['age_group'].isin(selected_age_groups)]
    data = filtered_data.groupby('year_of_sale')['price'].mean().reset_index()

    years = data['year_of_sale']
    prices = data['price']
   

    # Create line graph
    fig = go.Figure(data=go.Scatter(x=years, y=prices, mode='markers+lines', connectgaps=True))

    # Update layout
    fig.update_layout(title=f'Average {selected_category} Price over the Years',
                      xaxis_title='Year',
                      yaxis_title='Price',
                      xaxis=dict(tickmode='linear'))

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


