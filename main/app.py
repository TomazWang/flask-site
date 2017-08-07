import logging

from flask import Flask, render_template, request
from main.dev.chl_parser import charles_parser

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


# @main.route('/hello/')
# def hello_world():
#     return 'Hello World!'


@app.route('/dev/charles_parser', methods=['POST'])
def route_charles_parser():
    json_dict = request.get_json()

    file_url = json_dict['file_url']
    parse_result = charles_parser.from_url(file_url)

    return parse_result.url

if __name__ == '__main__':
    # main.run()
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
