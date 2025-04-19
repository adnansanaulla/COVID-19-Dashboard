#COVID-19 Dashboard

An interactive, data-driven dashboard built with Dash, Plotly, and Dash Bootstrap Components, showcasing global COVID-19 trends, vaccination progress, and country specific data-using real time information from 'Our World in Data'.

## Features

- Dual-axis graph showing total cases and deaths over time
- Bar and line graph of daily new cases with a 7-day rolling average
- Vaccination progress plot showing percentage of population vaccinated
- Country summary cards with mortality rate, case count, and more
- Dark mode theme using Dash Bootstrap's DARKLY stylesheet
- Dropdown to explore any country with real-time updates
- Source: [Our World in Data - COVID-19 Dataset](https://ourworldindata.org/coronavirus)

## Tech used

- [Dash](https://dash.plotly.com/)
- [Plotly](https://plotly.com/)
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
- [Pandas](https://pandas.pydata.org/)
- Python 3.8+

## Getting Started

### Clone this repository

'''bash
git clone https://github.com/adnansanaulla/COVID-19-Dashboard.git
cd COVID-19-Dashboard

### Install libraries

pip install -r requirements.txt

### Open the app

python app.py
Open link: http://127.0.0.1:8050/
