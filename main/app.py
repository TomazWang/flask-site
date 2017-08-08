import json
import logging
import os

import flask
from flask import Flask, render_template, request, json, url_for
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

    return json.jsonify(parse_result.__dict__)
    # return parse_result.download_url


@app.route('/dev/charles_parser/download/<path:filename>', methods=['GET', 'POST'])
def route_charles_parser_download(filename):
    logging.warning('[WARNING][app] >> route_charles_parser_download: filename = ' + filename)
    download_dir = os.path.join(flask.current_app.root_path, charles_parser.DOWNLAOD_DIR)
    logging.warning(
        '[WARNING][app] >> route_charles_parser_download: download_dir = ' + download_dir)
    logging.warning('[WARNING][app] >> route_charles_parser_download: dl_dir exists ? '
                    + str(os.path.exists(download_dir)))

    return flask.send_from_directory(directory=download_dir, filename=filename)


if __name__ == '__main__':
    # main.run()
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
