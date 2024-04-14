import sqlite3
import pandas as pd
from flask import jsonify


def get_station_data(station):

    if not station.isdigit():
        return jsonify({'error': 'Invalid station format'}), 400

    conn = sqlite3.connect('data/ecad.db')
    table_name = 'TG_STAID' + str(station).zfill(6)
    try:
        query = f'''
        SELECT * FROM {table_name}
        '''
        df = pd.read_sql(query, conn)
    except pd.errors.DatabaseError:
        return jsonify({'error': 'Nonexistent station ID'}), 404

    return df
