import config
from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def title_page():
    return render_template('meteo.html', graphs=config.GRAPH_PATHS)
