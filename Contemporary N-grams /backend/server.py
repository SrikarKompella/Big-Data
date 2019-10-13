import json
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

MOCK_DATABASE = {
  'javascript': [
    {'date': '2018-07-01', 'value': 0},
    {'date': '2018-08-01', 'value': 2},
    {'date': '2018-09-01', 'value': 4},
    {'date': '2018-10-01', 'value': 8},
    {'date': '2018-11-01', 'value': 16},
    {'date': '2018-12-01', 'value': 32}
  ],
  'python': [
    {'date': '2018-07-01', 'value': 5},
    {'date': '2018-08-01', 'value': 4},
    {'date': '2018-09-01', 'value': 8},
    {'date': '2018-10-01', 'value': 16},
    {'date': '2018-11-01', 'value': 32},
    {'date': '2018-12-01', 'value': 64}
  ],
}

def fetch_ngrams(ngrams):
    return [fetch_ngram(ngram) for ngram in ngrams]

def fetch_ngram(ngram):
    # TODO: Connect to database and remove MOCK_DATABASE

    return {
        'ngram': ngram,
        'data': MOCK_DATABASE.get(ngram, []),
    }

@app.route('/ngrams', methods=['POST', 'OPTIONS'])
def ngrams():
    if request.method == 'POST':
        request_json = request.get_json()
        ngrams = request_json['query'].split(',')
        response_json = fetch_ngrams(ngrams)
        response = app.response_class(
            response=json.dumps(response_json),
            mimetype='application/json'
        )

        # CORS
        response.headers.add('Access-Control-Allow-Origin', '*')
    else:
        # CORS
        response = app.response_class()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'content-type')
        response.headers.add('Access-Control-Allow-Methods', '*')

    return response

if __name__=='__main__':
    app.run(debug=True)
