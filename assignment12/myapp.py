from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.data as pldata

df = pldata.gapminder(return_type='pandas')

countries = df['country'].drop_duplicates().sort_values()

app = Dash(__name__)
server = app.server  # needed for deployment

app.layout = html.Div([
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in countries],
        value='Canada'
    ),
    dcc.Graph(id='gdp-growth')
])

@app.callback(
    Output('gdp-growth', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_graph(country):
    filtered = df[df['country'] == country]
    fig = px.line(
        filtered,
        x='year',
        y='gdpPercap',
        title=f'GDP Per Capita Over Time — {country}'
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
