from flask import Flask, request
from flask_cors import CORS
import bcb
import pandas as pd
from pandas.tseries.offsets import BDay
import numpy
import investpy
import datetime

app = Flask(__name__)
CORS(app)

@app.route("/ptax")
def get_PTAX():
    endpoint = bcb.PTAX().get_endpoint('CotacaoMoedaDia')

    if request.args.get('date'):
        day_request = request.args.get('date')
        date = day_request
    else:
        last_bussines_day = (pd.Timestamp.today() - BDay(1)).strftime("%m/%d/%Y")
        date = last_bussines_day


    ptax = endpoint.query().parameters(moeda='USD', dataCotacao=date).collect()
    
    if len(ptax.keys()) != 0:
        print(True)
    else:
        return { "code": 404 }

    ptax = endpoint.query().parameters(moeda='USD', dataCotacao=date).collect()

    list = ptax['cotacaoVenda'].values.tolist()

    return {
        "code": 200,
        "date": date,
        "interm": {
            "10:00": str(list[0] * 1000), 
            "11:00": str(list[1] * 1000), 
            "12:00": str(list[2] * 1000), 
            "13:00": str(list[3] * 1000)  
        }, 
        "mean": numpy.mean(list) * 1000,
        "std": numpy.std(list) * 1000
    }

@app.route("/economic-calendar")
def get_economic_calendar():
    data = investpy.news.economic_calendar(from_date="11/08/2023", to_date="12/08/2023", countries=["United States", "Brazil"])
    
    return data.to_json()