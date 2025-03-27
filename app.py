from flask import Flask, render_template, request
import sqlite3
import pandas as pd

app = Flask(__name__)

def get_data():
    conn = sqlite3.connect('real_estate.db')
    df = pd.read_sql_query("SELECT * FROM property_list", conn)
    conn.close()
    return df

@app.route('/')
def index():
    view = request.args.get('view', 'table')
    search = request.args.get('search', '').lower()

    df = get_data()
    if search:
        df = df[df['project_name_matched'].str.lower().str.contains(search)]

    data = df.to_dict(orient='records')
    return render_template('index.html', data=data, view=view, search=search)

if __name__ == '__main__':
    app.run(debug=True)
