from quart import Quart
from quart_cors import cors, route_cors

app = Quart(__name__)
app = cors(app, allow_origin="*")

@app.route('/login/<telf>', methods=['GET'])
async def login():
  return jsonify({'success': 'ok'})

if __name__ == "__main__":
  app.run(host='92.177.190.5', port=8000, debug=True)