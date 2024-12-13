from application import app
from flask import render_template, url_for
import pandas as pd
import json
import plotly
import plotly.express as px



@app.route("/")
def index():
    df = pd.read_csv("application/eci_cor.csv")
    total_votes = df.groupby('State').sum()
    import plotly.express as px
    percentage_votes = (total_votes['EVM Votes']/total_votes['Total Votes'])*100
    fig1 = px.bar(total_votes, x=total_votes.index, y=percentage_votes, color=total_votes.index)
    fig1.update_layout(showlegend=False)
    graph1JSON = json.dumps(fig1, cls = plotly.utils.PlotlyJSONEncoder)
    return render_template("index.html", title = "Home", graph1JSON = graph1JSON)