from flask import Flask
import bcb
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    ptax = bcb.PTAX().get_endpoint('CotacaoMoedaDia')
    df = ptax.query().parameters(moeda='USD', dataCotacao='03/08/2022').collect()
    cotacao_venda_list = df['cotacaoVenda'].values.tolist()
    return { "ptax": cotacao_venda_list }