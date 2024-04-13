from flask import Flask, render_template, send_file
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import io



app = Flask(__name__)

stations = pd.read_csv('data/data_misc/stations.txt', skiprows=17)
stations = stations[['STAID', 'STANAME                                 ', 'CN']]


@app.route('/')
def index():
    """
    Renders the home page, displaying a table of available weather stations.
    """
    return render_template('index.html', data=stations.to_html())

@app.route('/api/v1/<station>/<date>')
def temperature_in_date(station, date):
    """
    Provides temperature data for a specific station and date.

    Args:
        station (str): The station ID.
        date (str): The date in YYYYMMDD format.

    Returns:
        dict: A dictionary containing temperature information:
            - station: The station ID.
            - date: The requested date (formatted as YYYY-MM-DD).
            - temperature_in_date: The temperature on the specified date.
            - temperature_mean: The mean temperature for the station.
            - temperature_max: The maximum recorded temperature for the station.
            - temperature_min: The minimum recorded temperature for the station.
    """
    conn = sqlite3.connect('data/ecad.db')
    table_name = 'TG_STAID' + str(station).zfill(6)
    query = f'''
    SELECT * FROM {table_name}
    '''
    df = pd.read_sql(query, conn)

    df['tg0'] = df['tg'].mask(df['tg'] == -9999, np.nan)
    df['tg'] = df['tg0'] / 10
    modified_date = date[0:4] + '-' + date[4:6] + '-' + date[6:9]
    temperature = df.loc[df['date'] == date]['tg'].squeeze()
    temperature_mean = df['tg'].mean()
    temperature_min = df['tg'].min()
    temperature_max = df['tg'].max()

    response = {
        'station': station,
        'date': modified_date,
        'temperature_in_date': temperature,
        'temperature_mean': temperature_mean,
        'temperature_max': temperature_max,
        'temperature_min': temperature_min,
    }

    return response


@app.route('/api/v1/<station>')
def all_data(station):
    """
    Provides all temperature data for a specific station.

    Args:
        station (str): The station ID.

    Returns:
        list: A list of dictionaries, each representing a temperature record.
    """
    conn = sqlite3.connect('data/ecad.db')
    table_name = 'TG_STAID' + str(station).zfill(6)
    query = f'''
        SELECT * FROM {table_name}
        '''
    df = pd.read_sql(query, conn)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
    df['tg0'] = df['tg'].mask(df['tg'] == -9999, np.nan)
    df['tg'] = df['tg0'] / 10

    result = df.to_dict(orient='records')
    return result

@app.route('/api/v1/annual/<station>/<year>')
def annual_data(station, year):
    """
    Provides temperature data for a specific station and year.

    Args:
        station (str): The station ID.
        year (str): The year.

    Returns:
        list: A list of dictionaries, each representing a temperature record.
    """
    conn = sqlite3.connect('data/ecad.db')
    table_name = 'TG_STAID' + str(station).zfill(6)
    query = f'''
        SELECT * FROM {table_name}
        '''
    df = pd.read_sql(query, conn)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
    df['tg0'] = df['tg'].mask(df['tg'] == -9999, np.nan)
    df['tg'] = df['tg0'] / 10
    result = df[df['date'].str.startswith(str(year))].to_dict(orient='records')
    return result




if __name__ == '__main__':
    app.run(debug=False)