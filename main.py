import pandas.errors
from flask import Flask, render_template, send_file,jsonify
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import io



app = Flask(__name__)


@app.route('/')
def index():
    """
    Renders the home page, displaying a table of available weather stations.
    """
    stations = pd.read_csv('data/data_misc/stations.txt', skiprows=17)
    stations = stations[['STAID', 'STANAME                                 ', 'CN']]
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
    if not date.isdigit() or len(date) != 8:
        return jsonify({'error': 'Invalid date format or length'}), 400

    if not station.isdigit():
        return jsonify({'error': 'Invalid station format'}), 400

    conn = sqlite3.connect('data/ecad.db')

    table_name = 'TG_STAID' + str(station).zfill(6)
    try:
        query = f'''
        SELECT * FROM {table_name}
        '''
        df = pd.read_sql(query, conn)
    except pandas.errors.DatabaseError:
        return jsonify({'error': 'Nonexistent station ID'}), 404

    if date not in set(df['date']):
        return jsonify({'error': 'Nonexistent date for this station'}), 404


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
    if not station.isdigit():
        return jsonify({'error': 'Invalid station format'}), 400

    conn = sqlite3.connect('data/ecad.db')
    table_name = 'TG_STAID' + str(station).zfill(6)
    try:
        query = f'''
        SELECT * FROM {table_name}
        '''
        df = pd.read_sql(query, conn)
    except pandas.errors.DatabaseError:
        return jsonify({'error': 'Nonexistent station ID'}), 404

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
    if not year.isdigit() or len(year) != 4:
        return jsonify({'error': 'Invalid year format or length'}), 400


    if not station.isdigit():
        return jsonify({'error': 'Invalid station format'}), 400

    conn = sqlite3.connect('data/ecad.db')
    table_name = 'TG_STAID' + str(station).zfill(6)
    try:
        query = f'''
        SELECT * FROM {table_name}
        '''
        df = pd.read_sql(query, conn)
    except pandas.errors.DatabaseError:
        return jsonify({'error': 'Invalid station ID'}), 404

    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
    df['tg0'] = df['tg'].mask(df['tg'] == -9999, np.nan)
    df['tg'] = df['tg0'] / 10
    result = df[df['date'].str.startswith(str(year))].to_dict(orient='records')
    return result


@app.route('/visualization/<station>/<year>')
def visualization(station, year):
    """
    Generates a temperature visualization for a given station and year.

    Args:
        station (str): The station ID.
        year (str): The year.

    Returns:
        Flask send_file response: Sends a PNG image of the visualization.
    """
    if not year.isdigit() or len(year) != 4:
        return jsonify({'error': 'Invalid date format or length'}), 400

    data = annual_data(station, year)
    if 400 in data or 404 in data:
        return data[0], data[1]

    stations_local = pd.read_csv('data/data_misc/stations.txt', skiprows=17)
    station_name = stations_local.loc[stations_local['STAID'] == int(station)]['STANAME                                 '].squeeze()

    fig = px.line(data, x='date', y='tg', title=f'Visualization for Station {station_name.strip()} - {year}', width=1400, height=800).update_layout(
    xaxis_title="Date", yaxis_title="Temperature (C)")

    img = io.BytesIO()
    fig.write_image(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=False)