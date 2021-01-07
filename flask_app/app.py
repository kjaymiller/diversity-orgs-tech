import os
from flask import Flask
from flask import (
        Flask,
        render_template,
        request,
        redirect,
        flash,
        url_for,
        session,
        )
from connection import app_search


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET']

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/search')
def search():
    """Return Search Results Based on Products"""
    query = request.args.get('query', '')
    results = app_search.search(os.environ.get('ENGINE_NAME', body=body))
    return render_template(
            "search.html",
            query=query,
            results=results,
    )
