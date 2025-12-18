from flask import Blueprint
from controllers.etf_controller import EtfController

# Crea un Blueprint per le route degli ETF
etf_bp = Blueprint("etf", __name__)


# Route per visualizzare tutti gli ETF
@etf_bp.route("/")
@etf_bp.route("/etfs")
def index():
    return EtfController.index()


# Route per mostrare il form di creazione
@etf_bp.route("/etfs/create")
def create():
    return EtfController.create()


# Route per salvare un nuovo ETF
@etf_bp.route("/etfs/store", methods=["POST"])
def store():
    return EtfController.store()


# Route per mostrare i dettagli di un ETF
@etf_bp.route("/etfs/<string:ticker>")
def show(ticker):
    return EtfController.show(ticker)


# Route per mostrare il form di modifica
@etf_bp.route("/etfs/<string:ticker>/edit")
def edit(ticker):
    return EtfController.edit(ticker)


# Route per aggiornare un ETF
@etf_bp.route("/etfs/<string:ticker>/update", methods=["POST"])
def update(ticker):
    return EtfController.update(ticker)


# Route per eliminare un ETF
@etf_bp.route("/etfs/<string:ticker>/delete", methods=["POST"])
def delete(ticker):
    return EtfController.delete(ticker)


# Made with Bob
