from flask import Flask, render_template
import pandas as pd
import numpy as np
import sqlite3

app = Flask(__name__)

stations = pd.read_csv('data/data_misc/stations.txt', skiprows=17)
stations = stations[['STAID', 'STANAME                                 ', 'CN']]

@app.route('/')
def home():
    return render_template('index.html', data=stations.to_html())

@app.route('/api/v1/<station>/<date>')
def about(station, date):
    conn = sqlite3.connect('data/ecad.db')
    table_name = 'TG_STAID' + str(station).zfill(6)
    # # query = f'''
    # # SELECT TG FROM {table_name}
    # # WHERE date = ?
    # # '''
    # df = pd.read_sql(query, conn, params=[date])
    df = pd.read_sql_table(table_name, conn)

    df['tg0'] = df['tg'].mask(df['tg'] == -9999, np.nan)
    df['tg'] = df['tg0'] / 10
    modified_date = date[0:4] + '-' + date[4:6] + '-' + date[6:9]
    temperature = df.loc[df['date'] == modified_date]['tg'].squeeze()
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
    filename = 'data/TG_STAID' + str(station).zfill(6) + '.txt'
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    result = df.to_dict(orient='records')
    return result

@app.route('/api/v1/annual/<station>/<year>')
def annual_data(station, year):
    filename = 'data/TG_STAID' + str(station).zfill(6) + '.txt'
    df = pd.read_csv(filename, skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient='records')
    return result




if __name__ == '__main__':
    app.run(debug=True)