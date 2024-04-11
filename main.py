from flask import Flask, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/v1/<station>/<date>')
def about(station, date):
    filename = 'data/TG_STAID' + str(station).zfill(6) + '.txt'
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    df['TG0'] = df['   TG'].mask(df['   TG'] == -9999, np.nan)
    df['TG'] = df['TG0'] / 10
    modified_date = date[0:4] + '-' + date[4:6] + '-' + date[6:9]
    temperature = df.loc[df['    DATE'] == modified_date]['TG'].squeeze()
    temperature_mean = df['TG'].mean()
    temperature_min = df['TG'].min()
    temperature_max = df['TG'].max()


    response = {
        'station': station,
        'date': modified_date,
        'temperature_in_date': temperature,
        'temperature_mean': temperature_mean,
        'temperature_max': temperature_max,
        'temperature_min': temperature_min,
    }
    return response #render_template('api')

if __name__ == '__main__':
    app.run(debug=True)