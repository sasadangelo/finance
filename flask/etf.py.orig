# Model
class Etf(db.Model):
   __tablename__ = "etfs"
   ticker = db.Column(db.String(10), primary_key=True)
   name = db.Column(db.String(50))
   isin = db.Column(db.String(15))
   launchDate = db.Column(db.String(20))
   capital = db.Column(db.Float)
   replication = db.Column(db.String(30))
   volatility = db.Column(db.Float)
   currency = db.Column(db.String(10))
   dividend = db.Column(db.String(20))
   dividendFrequency = db.Column(db.Integer)
   yeld = db.Column(db.Float)

   def create(self):
       db.session.add(self)
       db.session.commit()
       return self

   def __init__(self, ticker, name, isin, launchDate, 
                      capital, replication, volatility,
                      currency, dividend, dividendFrequency, 
                      yeld):
       self.ticker = ticker
       self.name = name
       self.isin = isin
       self.launchDate = launchDate
       self.capital = capital
       self.replication = replication
       self.currency = currency
       self.dividend = dividend
       self.dividendFrequency = dividendFrequency
       self.yeld = yeld

   def __repr__(self):
       return f"{self.id}"

db.create_all()

class EtfSchema(ModelSchema):
   class Meta(ModelSchema.Meta):
       model = Etf
       sqla_session = db.session
   ticker = fields.String(required=True)
   name = fields.String(required=True)
   isin = fields.String(required=True)
   launchDate = fields.String(required=True)
   capital = fields.Number(required=True)
   replication = fields.String(required=True)
   currency = fields.String(required=True)
   dividend = fields.String(required=True)
   dividendFrequency = fields.Number(required=True)
   yeld = fields.String(required=True)
