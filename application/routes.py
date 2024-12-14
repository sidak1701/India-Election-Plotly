from application import app
from flask import render_template, url_for, request, jsonify
import pandas as pd
import json
import plotly
import plotly.express as px
from application.data import get_party_votes_for_state, get_map_data, get_piechart_data, get_vote_type_distribution


df = pd.read_csv("application/eci_cor.csv")

@app.route("/")
def index():
    data = get_party_votes_for_state('')
    return render_template("index.html", title = "Home")


@app.route("/barchart", methods=['POST'])
def barchart():
    state = request.json['state']
    data = get_party_votes_for_state(state)
    return jsonify(data)


@app.route("/barchart2", methods=['POST'])
def barchart2():
    state = request.json['state']
    data = get_vote_type_distribution(state)
    return jsonify(data)


@app.route("/map", methods=['POST'])
def map():
    data = get_map_data()
    return jsonify(data)


@app.route("/piechart", methods=['POST'])
def piechart():
    state = request.json['state']
    data = get_piechart_data(state)
    return jsonify(data)