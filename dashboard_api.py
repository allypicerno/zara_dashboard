import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
pip install xlrd

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
    dcc.Graph(id='graph')
])

# Define callback to update the graph
@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown', 'value')]
)
def update_graph(selected_category):
    filtered_data = df[df['category'] == selected_category]
    data = filtered_data.groupby('year_of_sale')['price'].mean().reset_index()

    years = data['year_of_sale']
    prices = data['price']
   

    # Create line graph
    fig = go.Figure(data=go.Scatter(x=years, y=prices, mode='markers+lines', connectgaps=True))

    # Update layout
    fig.update_layout(title=f'Price over Years for Category {selected_category}',
                      xaxis_title='Year',
                      yaxis_title='Price',
                      xaxis=dict(tickmode='linear'))

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


