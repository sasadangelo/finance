@app.route('/api/v1/etfs', methods=['GET'])
def index():
   get_etfs = Etf.query.all()
   etf_schema = EtfSchema(many=True)
   etfs = etf_schema.dump(get_etfs)
   return make_response(jsonify({"etfs": etfs}))

@app.route('/api/v1/etfs/<id>', methods=['GET'])
def get_etf_by_ticker(ticker):
   get_etf = Etf.query.get(ticker)
   etf_schema = EtfSchema()
   etf = etf_schema.dump(get_etf)
   return make_response(jsonify({"etf": etf}))
