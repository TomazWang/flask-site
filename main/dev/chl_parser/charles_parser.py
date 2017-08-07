from datetime import datetime

import requests

TEMP_FILE_FOLDER = 'charles_parser'


class Result:
    RC_SUCCESS = 0
    RC_ERR_FILE_EXT = -100
    RC_ERR_FILE_TYPE = -101

    def __init__(self, rc) -> None:
        super().__init__()
        self.rc = rc
        self.url = ''


def from_url(url: str) -> Result:
    """
    Parse charles session file with json format from a url.
     
    :param url: a link to charles session file with .chlsj extension
    :type url: str
    
    :return: a Result obj.
    :rtype: Result
    """

    if not url.endswith('.chlsj'):
        return Result(Result.RC_SUCCESS)

    # get file from url
    r = requests.get(url)

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S');
    temp_file_name = '{}/temp_{}'.format(TEMP_FILE_FOLDER, timestamp)

    with open(temp_file_name, 'w', encoding='utf-8') as temp_file:
        temp_file.write(r.content)

    return
    # TODO: 06/08/2017, @tomaz: download file from url.
    # TODO: 06/08/2017, @tomaz: read file.
    # TODO: 06/08/2017, @tomaz: parse json file one at a time.
    # TODO: 06/08/2017, @tomaz: compress all output file as a zip
    # TODO: 06/08/2017, @tomaz: return a url link to the output zip file
