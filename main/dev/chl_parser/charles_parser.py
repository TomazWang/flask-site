import os
from datetime import datetime
import zipfile

import requests

from main.dev.chl_parser import json_parser
from main.gcloud_util import cloud_storage

TEMP_FILE_FOLDER = 'temp_charles_parser'
DOWNLAOD_DIR = 'download'


class Result:
    RC_SUCCESS = 0
    RC_ERR_FILE_EXT = -100
    RC_ERR_FILE_TYPE = -101

    def __init__(self, rc) -> None:
        super().__init__()
        self._rc = -999
        self.rm = ''
        self.rc = rc

    @property
    def rc(self):
        return self._rc

    @rc.setter
    def rc(self, rc):
        self._rc = rc
        if rc == Result.RC_SUCCESS:
            self.rm = '處理成功'
        elif rc == Result.RC_ERR_FILE_EXT:
            self.rm = '檔案類型錯誤'
        elif rc == Result.RC_ERR_FILE_TYPE:
            self.rm = '請使用 session file'


def zipdir(dir_path, dest="") -> str:
    """
    input : Folder path and name
    output: using zipfile to ZIP folder
    """
    if dest == "":
        zf = zipfile.ZipFile(dir_path + '.zip', zipfile.ZIP_DEFLATED)
    else:
        zf = zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED)

    current_path = os.getcwd()
    os.chdir(dir_path)

    for root, dirs, files in os.walk("./"):
        for f in files:
            zf.write(os.path.join(root, f))

    zf.close()
    os.chdir(current_path)
    return dest


def from_url(url: str) -> Result:
    """
    Parse charles session file with json format from a url.
     
    :param url: a link to charles session file with .chlsj extension
    :type url: str
    
    :return: a Result obj.
    :rtype: Result
    """

    if not url.endswith('.chlsj'):
        return Result(Result.RC_ERR_FILE_EXT)

    # temp file name
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    datestamp = datetime.now().strftime('%Y%m%d')
    temp_file_name = './{}/temp_{}.json'.format(TEMP_FILE_FOLDER, timestamp)

    # check if temp folder exists
    if not os.path.exists('./{}'.format(TEMP_FILE_FOLDER)):
        os.mkdir('./{}'.format(TEMP_FILE_FOLDER))

    # download file from url
    r = requests.get(url)

    # write to local file
    with open(temp_file_name, 'wb+') as temp_file:
        temp_file.write(r.content)

    # parse file
    try:
        folder, output_file_arr = json_parser.parse(temp_file_name, suffix=timestamp)
    except KeyError:
        return Result(Result.RC_ERR_FILE_TYPE)

    folder_path = './{}/{}'.format(TEMP_FILE_FOLDER, folder)

    # zipfile

    # check download folder exists
    if not os.path.exists('./{}'.format(DOWNLAOD_DIR)):
        os.mkdir('./{}'.format(DOWNLAOD_DIR))

    # create a output file locate at download dir
    zipf_path = './{}/{}.zip'.format(DOWNLAOD_DIR, folder)
    zipdir(folder_path, dest=zipf_path)

    blob_name = 'download/{}/{}.zip'.format(datestamp, folder)
    blob = cloud_storage.upload_public_blob(zipf_path, blob_name)

    # Get public url for this blob
    result = Result(Result.RC_SUCCESS)
    result.url = blob.public_url

    # remvoe temp file
    os.remove(temp_file_name)
    os.remove(zipf_path)

    for child_file in os.listdir(folder_path):
        os.remove('{}/{}'.format(folder_path, child_file))

    os.rmdir(folder_path)

    # TODO: 10/08/2017, @tomaz: remove expired blob

    return result
