import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output


def plot_cases(country):
    filtered = df[df['location'] == country]
    fig = px.line(filtered, x = 'date', y = 'total_cases', title = f'Total COVID-19 Cases in {country}')
    return fig

df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
print(df.columns)
df = df[['location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'people_vaccinated', 'continent']]
df['date'] = pd.to_datetime(df['date'])
df = df[df['continent'].notnull()]

app = dash.Dash(__name__)

available_countries = df['location'].unique()

app.layout = html.Div([
    html.H1("COVID-19 Dashboard", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in available_countries],
        value='United States'
    ),
    dcc.Graph(id='covid-graph')
])

@app.callback(
    Output('covid-graph', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_graph(selected_country):
    return plot_cases(selected_country)

if __name__ == '__main__':
    app.run_server(debug=True)