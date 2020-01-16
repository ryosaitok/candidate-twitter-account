# coding=utf-8
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials


SCOPE_URL = 'https://spreadsheets.google.com/feeds'
SHEET_PROJECT_ID = os.environ['SHEET_PROJECT_ID']
SHEET_PRIVATE_KEY_ID = os.environ['SHEET_PRIVATE_KEY_ID']
SHEET_PRIVATE_KEY = os.environ['SHEET_PRIVATE_KEY']
SHEET_CLIENT_EMAIL = os.environ['SHEET_CLIENT_EMAIL']
SHEET_CLIENT_ID = os.environ['SHEET_CLIENT_ID']
SHEET_CLIENT_X509_CERT_URL = os.environ['SHEET_CLIENT_X509_CERT_URL']

CREDENTIAL_FILE_NAME = 'spread_sheet_credential.json'
TEMPLATE_FILE_NAME = 'spread_sheet_credential_template.txt'


def access_sheet(gid):
    """
    access to google spread sheet. and you must call close_sheet() to remove credential file.
    :return: spread sheet
    """
    # 書き込み用ファイル
    credential_file = open(CREDENTIAL_FILE_NAME, 'w')

    # テンプレートファイルを読み込み、書き込みファイルに書き込み
    template_file = open(TEMPLATE_FILE_NAME)
    template_file_lines = template_file.readlines()
    line_num = 0
    for line in template_file_lines:
        line_num += 1
        if line_num == 3:
            line = line.format(SHEET_PROJECT_ID)
        elif line_num == 4:
            line = line.format(SHEET_PRIVATE_KEY_ID)
        elif line_num == 5:
            line = line.format(SHEET_PRIVATE_KEY)
        elif line_num == 6:
            line = line.format(SHEET_CLIENT_EMAIL)
        elif line_num == 7:
            line = line.format(SHEET_CLIENT_ID)
        elif line_num == 11:
            line = line.format(SHEET_CLIENT_X509_CERT_URL)
        credential_file.writelines(line)
    template_file.close()
    credential_file.close()

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIAL_FILE_NAME, SCOPE_URL)
    client = gspread.authorize(credentials)
    return client.open_by_key(gid)


def close_sheet():
    """
    remove credential file for safety
    """
    os.remove(CREDENTIAL_FILE_NAME)
