import base64
import json
import os
from json import JSONDecodeError
from typing import Dict, Tuple, List

import logging

from main.dev.chl_parser import charles_parser


def parse_chlsj(data: Dict, **kwargs) -> str:
    """
    Parse json dict to a str 
    :param data: a json dict for chlsj session
    :type data: dict
    
    :keyword out_file_suffix: suffix of output file
    
    :return: output file name, ( parsed_<url>_<suffix>.json)
    :rtype: str
    """

    status = data.get('status', '')
    scheme = data.get('scheme', '') or ''
    host = data.get('host', '') or ''
    path = data.get('path', '') or ''
    port = data.get('port', None)
    actualPort = data.get('actualPort', None)
    query = data.get('query', None)
    method = data.get('method', '') or 'UNKNOWN METHOD'
    request = data.get('request', '') or ''
    response = data.get('response', '') or ''

    # create a file name base on url
    last_part = str(path).split('/')[-1].replace('.', '')

    out_file_suffix = str(kwargs.get('out_file_suffix', ''))
    if len(out_file_suffix) > 0:
        out_file_suffix = out_file_suffix + '_'

    folder = kwargs.get('folder', last_part)
    folder_path = './{}/{}'.format(charles_parser.TEMP_FILE_FOLDER, folder)

    # check if temp folder exists
    if not os.path.exists('./{}'.format(folder_path)):
        os.mkdir('./{}'.format(folder_path))

    out_file_name = '{}/parsed_{}{}.txt' \
        .format(folder_path, out_file_suffix, last_part)

    # create a file
    out_file = open(out_file_name, 'w+', encoding='utf-8')
    out_file.write('')

    if port not in [80, 443, None]:
        port = ':' + str(port)
    else:
        port = ''

    if query:
        query = '?' + query
    else:
        query = ''

    if scheme:
        scheme = scheme + '://'

    line_sum = '# ' + method + ' ' + scheme + host + port + path + query

    out_file.write(line_sum)
    out_file.write('\n\n')
    out_file.write('+ Status: {}'.format(status))
    out_file.write('\n\n')

    # Request
    out_file.write('+ Request')
    out_file.write('\n\n')

    # request header
    out_file.write('\t' + '> Headers' + '\n')

    if 'headers' in request.get('header', {}):
        for header in request.get('header').get('headers', []):
            out_file.write('\t\t')
            out_file.write(header.get('name', ''))
            out_file.write(': ')
            out_file.write(header.get('value', ''))
            out_file.write('\n')

    out_file.write('\n\n\n')

    if 'body' in request:
        # request body
        body = request.get('body')
        encoding = body.get('encoding', 'utf-8')

        if encoding == 'base64':
            encoded_raw = body.get('encoded')

            out_file.write('\t' + '> Body' + '\n')
            decoded = base64.b64decode(encoded_raw).decode('utf-8')

            for line in decoded.split('\n'):
                out_file.write('\t\t{}\n'.format(line))

        elif 'text' in request.get('body', {}):
            body_content_json = request.get('body').get('text')
            try:
                parsed_body_json = json.loads(body_content_json, encoding='utf-8')
                out_file.write('\t' + '> Body' + '\n')
                parsed_body_str = json \
                    .dumps(parsed_body_json, indent=4, sort_keys=True, ensure_ascii=False)

                for line in parsed_body_str.split('\n'):
                    out_file.write('\t\t{}\n'.format(line))
            except JSONDecodeError:
                pass

        out_file.write('\n\n\n')

    out_file.write('===========================================================================')
    out_file.write('\n\n\n')

    # Response
    response_code = response.get('status', 'N/A')
    out_file.write('+ Response (' + str(response_code) + ')')
    out_file.write('\n\n')

    # response header
    out_file.write('\t' + '> Headers' + '\n')

    if 'headers' in response.get('header', {}):
        for header in response.get('header').get('headers', []):
            out_file.write('\t\t')
            out_file.write(header.get('name', ''))
            out_file.write(': ')
            out_file.write(header.get('value', ''))
            out_file.write('\n')

    out_file.write('\n\n\n')

    if 'body' in response:
        # response body
        body = response.get('body')
        encoding = body.get('encoding', 'utf-8')

        if encoding == 'base64':
            encoded_raw = body.get('encoded')

            out_file.write('\t' + '> Body' + '\n')
            decoded = base64.b64decode(encoded_raw).decode('utf-8')

            for line in decoded.split('\n'):
                out_file.write('\t\t{}\n'.format(line))

        elif 'text' in response.get('body', {}):
            body_content_json = response.get('body').get('text')
            try:
                parsed_body_json = json.loads(body_content_json, encoding='utf-8')
                out_file.write('\t' + '> Body' + '\n')
                parsed_body_str = json \
                    .dumps(parsed_body_json, indent=4, sort_keys=True, ensure_ascii=False)

                for line in parsed_body_str.split('\n'):
                    out_file.write('\t\t{}\n'.format(line))
            except JSONDecodeError:
                pass

    out_file.write('\n\n\n\n')
    out_file.close()

    return out_file_name


def parse(in_file_name, **kwargs):
    """
    :param in_file_name: input file path  
    :return: array of file output path
    :rtype: (str, [str])
    """
    result_arr = []
    suffix = kwargs.get('suffix', '')
    json_content = kwargs.get('json_content')
    url_path = json_content[0]['path']
    folder = str(url_path).split('/')[-1].replace('.', '')
    if len(suffix) > 0:
        folder = folder + suffix

    if len(json_content) > 1:
        for i in range(len(json_content)):
            data = json_content[i]
            result_arr.append(parse_chlsj(data, folder=folder, out_file_suffix=str(i)))
    else:
        result_arr.append(parse_chlsj(json_content[0], folder=folder))

    return folder, result_arr
