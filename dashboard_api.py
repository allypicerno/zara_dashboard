import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import base64

df = pd.read_excel('fashion_data_2018_2022.xls')
df = df[['price', 'year_of_sale', 'category', 'average_rating', 'age_group', 'gender']].dropna()

# below code taken from https://community.plotly.com/t/png-image-not-showing/15713
image_filename_model = 'model.png'  # Update with your model image filename
encoded_image_model = base64.b64encode(open(image_filename_model, 'rb').read()).decode('utf-8')
image_filename_zara = 'zara logo.png'  # Update with your ZARA logo image filename
encoded_image_zara = base64.b64encode(open(image_filename_zara, 'rb').read()).decode('utf-8')

app = Dash(__name__)

age_groups_sorted = sorted(df['age_group'].unique()) # get unique age groups for checklist

app.layout = html.Div(style={'padding': '20px'}, children=[ # create initial heading with zara logo and text
    html.Div(style={'background-color': '#F0F0F0', 'display': 'flex', 'align-items': 'center', 'padding': '20px'}, children=[
        html.Div([
            html.Img(src='data:image/png;base64,{}'.format(encoded_image_model),
                     style={'height': '100%', 'max-width': '20%', 'object-fit': 'cover', 'margin-right': '10px'}),
            html.Img(src='data:image/png;base64,{}'.format(encoded_image_zara),
                     style={'width': '150px', 'height': '100px', 'margin': '0 auto', 'margin-left': '10px'}),

        ]),
        html.Div([
            html.P(
                'Are you interested in seeing how the prices of certain items of clothing have changed over the years? '
                'Use the filtering options below to gain deeper insight in fashion trends!',
                style={'fontSize': '18px', 'font-family': 'didot', 'color': 'black'}
            )
        ], style={'background-color': '#F0F0F0','margin-left': '20px'}),
    ]),
    html.Hr(style={'border-top': '2px solid black', 'margin': '20px 0',}),  # Solid black line, chat gpt
    html.Div(style={'display': 'flex', 'background-color': '#F0F0F0'}, children=[  # place all filterings on left side of the screen
        html.Div(style={'flex': '1', 'padding': '20px'}, children=[
            html.H2('Filter your search', style={'textAlign': 'left', 'color': 'black', 'fontFamily': 'didot', 'text-decoration': 'italicize'}),
            html.Div([
                html.H4('Required: Select Clothing Category of Interest', style={'fontFamily': 'didot'}),
                dcc.Dropdown(
                    id='dropdown',
                    options=[{'label': cat, 'value': cat} for cat in df['category'].unique()],
                    value=df['category'].unique()[0],
                    clearable=False,
                    style={'color': 'black', 'width': '50%'}
                )
            ]),
            html.Br(),
            html.Div([
                html.H4('Optional Filtering', style={'textAlign': 'left', 'color': 'black', 'fontFamily': 'didot'}),
                html.H5('Select Gender of interest', style={'color': 'black', 'fontFamily': 'didot'}),
                dcc.RadioItems(
                    id='radio',
                    options=[{'label': 'Male', 'value': 'Male'}, {'label': 'Female', 'value': 'Female'}],
                    value=None
                ),
                html.Br(),
                html.H5('Select an Age Group of Interest', style={'color': 'black', 'fontFamily': 'didot'}),
                dcc.Checklist(
                    id='age-group-checklist',
                    options=[{'label': ag, 'value': ag} for ag in age_groups_sorted],
                    value=[],
                    inline=True
                ),
                html.Br(),
                html.H5(
                    'Select Minimum Rating of Interest (if you select 3.2, data will be restricted to items with rating above 3.2)',
                    style={'color': 'black', 'fontFamily': 'didot'}
                ),
                dcc.Slider(
                    id='rating-slider',
                    min=df['average_rating'].min(),
                    max=df['average_rating'].max(),
                    value=df['average_rating'].min(),
                    marks={str(rating): str(rating) for rating in df['average_rating'].unique()},
                    step=None
                )
            ]),
        ]),
        html.Div(style={'flex': '1', 'background-color': '#F0F0F0'}, children=[
            dcc.Graph( # place graph on right side of the screen
                id='graph',
                config={'displayModeBar': False},
                style={'border': '2px solid darkpurple'}
            )
        ])
    ])
])


@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown', 'value'),
     Input('radio', 'value'),
     Input('age-group-checklist', 'value'),
     Input('rating-slider', 'value')]
)
def update_graph(selected_category, selected_gender, selected_age_groups, selected_rating):
    filtered_data = df[df['category'] == selected_category] # mandatory filter by category

    # optional filterings if selected
    if selected_age_groups:
        filtered_data = filtered_data[filtered_data['age_group'].isin(selected_age_groups)]
    filtered_data = filtered_data[filtered_data['average_rating'] >= selected_rating]
    if selected_gender:
        filtered_data = filtered_data[filtered_data['gender'] == selected_gender]
    data = filtered_data.groupby('year_of_sale')['price'].mean().reset_index() # get the average price for each year

    # create line plot with years on x axis price on y
    years = data['year_of_sale']
    prices = data['price']
    fig = go.Figure(data=go.Scatter(x=years, y=prices, mode='markers+lines', connectgaps=True))

    # format the graph
    fig.update_layout(
        title=f'Average {selected_category} Price over the Years',
        xaxis_title='Year',
        yaxis_title='Price',
        xaxis=dict(tickmode='linear'),
        title_font=dict(size=25, family='didot', color='black'),
        title_x=.5,
        plot_bgcolor='#F0F0F0',
        paper_bgcolor='#F0F0F0'
        )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
