from models.etf import Etf
from database import db


class EtfService:
    """Service layer per la gestione degli ETF"""

    @staticmethod
    def get_all_etfs():
        """Recupera tutti gli ETF dal database"""
        return Etf.query.all()

    @staticmethod
    def get_etf_by_ticker(ticker):
        """Recupera un ETF specifico tramite ticker"""
        return Etf.query.get(ticker)

    @staticmethod
    def create_etf(data):
        """Crea un nuovo ETF"""
        try:
            etf = Etf(
                ticker=data.get("ticker"),
                name=data.get("name"),
                isin=data.get("isin"),
                launchDate=data.get("launchDate"),
                capital=data.get("capital"),
                replication=data.get("replication"),
                volatility=data.get("volatility"),
                currency=data.get("currency"),
                dividend=data.get("dividend"),
                dividendFrequency=data.get("dividendFrequency"),
                yeld=data.get("yeld"),
            )
            db.session.add(etf)
            db.session.commit()
            return etf, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update_etf(ticker, data):
        """Aggiorna un ETF esistente"""
        try:
            etf = Etf.query.get(ticker)
            if not etf:
                return None, "ETF non trovato"

            # Aggiorna solo i campi forniti
            if "name" in data:
                etf.name = data["name"]
            if "isin" in data:
                etf.isin = data["isin"]
            if "launchDate" in data:
                etf.launchDate = data["launchDate"]
            if "capital" in data:
                etf.capital = data["capital"]
            if "replication" in data:
                etf.replication = data["replication"]
            if "volatility" in data:
                etf.volatility = data["volatility"]
            if "currency" in data:
                etf.currency = data["currency"]
            if "dividend" in data:
                etf.dividend = data["dividend"]
            if "dividendFrequency" in data:
                etf.dividendFrequency = data["dividendFrequency"]
            if "yeld" in data:
                etf.yeld = data["yeld"]

            db.session.commit()
            return etf, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete_etf(ticker):
        """Elimina un ETF"""
        try:
            etf = Etf.query.get(ticker)
            if not etf:
                return False, "ETF non trovato"

            db.session.delete(etf)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def etf_exists(ticker):
        """Verifica se un ETF esiste"""
        return Etf.query.get(ticker) is not None


# Made with Bob
