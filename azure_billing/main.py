from os import getcwd
from flask import Flask, Response, abort
from scrape import data


app = Flask(__name__)

app.config.from_pyfile(getcwd()+"/application.cfg")


@app.route("/health")
def health():
    return 'ok'


@app.route("/metrics", methods=['GET'])
def metrics():

    try:
        metrics = data(app.config['ENROLLMENT'],
                       token=app.config['TOKEN']
                       )
    except Exception as e:
        abort(Response('Scrape failed: %s' % e, status=502))

    return metrics, 200, {'Content-Type': 'text/plain; charset=utf-8'}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')