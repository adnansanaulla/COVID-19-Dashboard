import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
print(df.columns)
df['date'] = pd.to_datetime(df['date'])
df = df[df['continent'].notnull()]
key_columns = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'people_vaccinated', 'people_fully_vaccinated', 'population']
initial_columns = ['location', 'date', 'continent']
columns = initial_columns + key_columns
df = df[[col for col in columns if col in df.columns]]

for col in df.columns:
    if col not in initial_columns:
        df[col] = df[col].fillna(0)

if 'people_vaccinated' in df.columns and 'population' in df.columns:
    df['vaccination_percentage'] = (df['people_vaccinated'] / df['population'] * 100).round(2)

available_countries = sorted(df['location'].unique())

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

def plot_cases_deaths(country):
    filtered = df[df['location'] == country]
    fig = make_subplots(specs = [[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x = filtered['date'], 
                   y = filtered['total_cases'], 
                   name = "Total Cases", 
                   line = dict(color = "#0099ff", width = 3)), 
        secondary_y = False,
    )
    fig.add_trace(
        go.Scatter(x = filtered['date'], 
                   y = filtered['total_deaths'], 
                   name = "Total Deaths", 
                   line = dict(color = "#FF1800", width = 3)), 
        secondary_y = True,
    )
    fig.update_layout(
        title_text = f"COVID-19 Cases and Deaths in {country}", 
        hovermode = "x unified", 
        legend = dict(orientation = "h", 
                      yanchor = "bottom", 
                      y = 1.02, 
                      xanchor = "center", 
                      x = 0.5),
        margin = dict(l = 60, 
                      r = 60, 
                      t = 80, 
                      b = 60),
        paper_bgcolor = "#000000",
        plot_bgcolor = "#000000",
        font = dict(color = "white")
    )
    fig.update_xaxes(title_text = "Date", gridcolor = "#555555")
    fig.update_yaxes(title_text = "Total Cases", secondary_y = False, gridcolor = "#555555")
    fig.update_yaxes(title_text = "Total Deaths", secondary_y = True, gridcolor = "#555555")

    return fig

def plot_daily_cases(country):
    filtered = df[df['location'] == country].sort_values('date')
    if 'new_cases' in filtered.columns:
        filtered['new_cases_avg'] = filtered['new_cases'].rolling(window = 7).mean()
    fig = go.Figure()
    if 'new_cases' in filtered.columns:
        fig.add_trace(
            go.Bar(x = filtered['date'],
                   y = filtered['new_cases'], 
                   name = "Daily New Cases",
                   marker_color = "#0099ff", 
                   opacity = 0.7)
        )
    if 'new_cases_avg' in filtered.columns:
        fig.add_trace(
            go.Scatter(x = filtered['date'],
                       y = filtered['new_cases_avg'], 
                       name = "7-Day Average", 
                       line = dict(color = "#00ff6c", width = 3))
        )
    fig.update_layout(
        title_text = f"Daily New COVID-19 Cases in {country}",
        xaxis_title = "Date", 
        yaxis_title = "New Cases",
        hovermode = "x unified", 
        legend = dict(orientation = "h",
                      yanchor = "bottom",
                      y = 1.02, 
                      xanchor = "center", 
                      x = 0.5),
        margin = dict(l = 60, 
                      r = 60, 
                      t = 80, 
                      b = 60),
        paper_bgcolor = "#000000", 
        plot_bgcolor = "#000000",
        font = dict(color = "white")
    )
    fig.update_xaxes(gridcolor = "#555555")
    fig.update_yaxes(title_text = "New Cases", gridcolor = "#555555")

    return fig

def plot_vaccination_progress(country):
    filtered = df[df['location'] == country].sort_values('date')
    fig = go.Figure()
    if 'vaccination_percentage' in filtered.columns:
        latest_vax_data = filtered[filtered['vaccination_percentage'] > 0].iloc[-1] if not filtered[filtered['vaccination_percentage'] > 0].empty else None
        fig.add_trace(
            go.Scatter(x = filtered['date'], 
                       y = filtered['vaccination_percentage'], 
                       name = "Population Vaccinated (%)", 
                       line = dict(color = "#b500ff", width = 3)
            )
        )
        if latest_vax_data is not None:
            latest_date = latest_vax_data['date']
            latest_pct = latest_vax_data['vaccination_percentage']
            fig.add_annotation(
                x = latest_date,
                y = latest_pct, 
                text = f"{latest_pct:.1f}%",
                showarrow = True, 
                arrowhead = 1,
                ax = 40, 
                ay = -40
            )
    fig.update_layout(
        title_text = f"COVID-19 Vaccination Progress in {country}", 
        xaxis_title = "Date", 
        yaxis_title = "Population Vaccinated (%)", 
        hovermode = "x unified", 
        margin = dict(l = 60, 
                      r = 60, 
                      t = 80, 
                      b = 60),
        paper_bgcolor = "#000000", 
        plot_bgcolor = "#000000",
        font = dict(color = "white")
    )
    fig.update_xaxes(gridcolor = "#555555")
    fig.update_yaxes(gridcolor = "#555555", range = [0, 100])

    return fig

def get_country_summary(country):
    filtered = df[df['location'] == country]
    latest = filtered.sort_values('date').iloc[-1] if not filtered.empty else None
    if latest is None:
        return {}
    summary = {}
    if 'total_cases' in latest and latest['total_cases'] > 0:
        summary['Total Cases'] = f"{int(latest['total_cases']):,}"
    if 'total_deaths' in latest and latest['total_deaths'] > 0:
        summary['Total Deaths'] = f"{int(latest['total_deaths']):,}"
    if 'total_cases' in latest and 'total_deaths' in latest and latest['total_cases'] > 0:
        mortality = (latest['total_deaths'] / latest['total_cases'] * 100)
        summary['Mortality Rate'] = f"{mortality:.2f}%"
    if 'vaccination_percentage' in latest and latest['vaccination_percentage'] > 0:
        summary['Vaccination Rate'] = f"{latest['vaccination_percentage']:.2f}%"
    if 'population' in latest and latest['population'] > 0:
        summary['Population'] = f"{int(latest['population']):,}"
    
    return summary
latest_date = df['date'].max() if not df.empty else None
latest_date_str = df['date'].max().strftime('%B %d, %Y') if not df.empty else "Data not available"

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div([
            html.H1("COVID-19 Dashboard", className="text-center my-4"),
            html.P("Interactive visualization of COVID-19 data from Our World in Data", className="text-center text-muted mb-5")
        ]), width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Select a Country"),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': c, 'value': c} for c in available_countries],
                        value='United States',
                        style={"backgroundColor": "#444", "color": "#000"}
                    )
                ])
            ], className="mb-4")
        ], md=12, lg=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card(
                id="summary-stats",
                className="mb-4"
            )
        ], md=12, lg=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Cases and Deaths Over Time"),
                dbc.CardBody([
                    dcc.Graph(id='cases-deaths-graph', config={'responsive': True})
                ])
            ], className="mb-4")
        ], md=12, lg=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Daily New Cases"),
                dbc.CardBody([
                    dcc.Graph(id='daily-cases-graph', config={'responsive': True})
                ])
            ], className="mb-4")
        ], md=12, lg=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Vaccination Progress"),
                dbc.CardBody([
                    dcc.Graph(id='vaccination-graph', config={'responsive': True})
                ])
            ], className="mb-4")
        ], md=12, lg=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.P("Data source: Our World in Data", className="text-muted"),
                html.P(f"Last updated: {latest_date_str}", className="text-muted")
            ], className="text-center mb-4")
        ], width=12)
    ])
], fluid=True, style={"backgroundColor": "#000000", "minHeight": "100vh", "color": "white"})

@app.callback(
    Output('cases-deaths-graph', 'figure'),
    Output('daily-cases-graph', 'figure'),
    Output('vaccination-graph', 'figure'),
    Output('summary-stats', 'children'),
    [Input('country-dropdown', 'value')]
)

def update_graphs(selected_country):
    cases_deaths_fig = plot_cases_deaths(selected_country)
    daily_cases_fig = plot_daily_cases(selected_country)
    vaccination_fig = plot_vaccination_progress(selected_country)
    summary = get_country_summary(selected_country)
    summary_cards = []
    if summary:
        summary_cards = [
            dbc.CardHeader(f"Key Statistics for {selected_country}"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H5(key, className="card-title text-center"),
                                html.H3(value, className="card-text text-center")
                            ])
                        ], color="dark", inverse=True, className="mb-3")
                    ], md=6, lg=3) for key, value in summary.items()
                ])
            ])
        ]
    return cases_deaths_fig, daily_cases_fig, vaccination_fig, summary_cards

if __name__ == '__main__':
    app.run(debug=True)