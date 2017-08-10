import json
import os
from typing import Dict, Tuple, List

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

    host = data['host']
    path = data['path']
    method = data['method']
    request = data['request']
    response = data['response']

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

    line_sum = '# ' + method + ' ' + host + path
    out_file.write(line_sum)
    out_file.write('\n\n')

    # Request
    out_file.write('+ Request')
    out_file.write('\n\n')

    # request header
    out_file.write('\t' + '> Headers' + '\n')

    for header in request['header']['headers']:
        out_file.write('\t\t')
        out_file.write(header['name'])
        out_file.write(': ')
        out_file.write(header['value'])
        out_file.write('\n')

    out_file.write('\n\n\n')

    if 'body' in request:
        # request body
        out_file.write('\t' + '> Body' + '\n')
        body_content_json = request['body']['text']
        parsed_body_json = json.loads(body_content_json, encoding='utf-8')
        parsed_body_str = json \
            .dumps(parsed_body_json, indent=4, sort_keys=True, ensure_ascii=False)
        for line in parsed_body_str.split('\n'):
            out_file.write('\t\t')
            out_file.write(line)
            out_file.write('\n')
        out_file.write('\n\n\n')

    out_file.write('===========================================================================')
    out_file.write('\n\n\n')

    # Response
    response_code = response['status']
    out_file.write('+ Response (' + str(response_code) + ')')
    out_file.write('\n\n')

    # response header
    out_file.write('\t' + '> Headers' + '\n')

    for header in response['header']['headers']:
        out_file.write('\t\t')
        out_file.write(header['name'])
        out_file.write(': ')
        out_file.write(header['value'])
        out_file.write('\n')

    out_file.write('\n\n\n')

    if 'body' in response:
        # response body
        out_file.write('\t' + '> Body' + '\n')
        body_content_json = response['body']['text']
        parsed_body_json = json.loads(body_content_json, encoding='utf-8')
        parsed_body_str = json \
            .dumps(parsed_body_json, indent=4, sort_keys=True, ensure_ascii=False)

        for line in parsed_body_str.split('\n'):
            out_file.write('\t\t')
            out_file.write(line)
            out_file.write('\n')

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
    with open(in_file_name, 'r', encoding='utf-8') as in_file:
        data_arr = json.load(in_file, encoding='utf-8')
        folder = str(data_arr[0]['path']).split('/')[-1].replace('.', '')
        if len(suffix) > 0:
            folder = folder + suffix

        if len(data_arr) > 1:
            for i in range(len(data_arr)):
                data = data_arr[i]
                result_arr.append(parse_chlsj(data, folder=folder, out_file_suffix=str(i)))
        else:
            result_arr.append(parse_chlsj(data_arr[0], folder=folder))

    return folder, result_arr
