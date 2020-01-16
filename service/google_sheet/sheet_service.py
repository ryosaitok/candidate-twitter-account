# coding=utf-8
from service.google_sheet import google_sheet_api_service
from model.evaluated_candidate_model import EvaluatedCandidate
from service import timeutil_service

# ファイル内で利用する定数
ACCESS_WAIT_SHORT_SECOND = 1
ACCESS_WAIT_LONG_SECOND = 60
DECIMAL_ZERO = 0
TIME_DIFFERENCE = 9
USER_ENTERED_OPTION = 'USER_ENTERED'
RAW_OPTION = 'RAW'


def write_users(gid, sheet_name, targets: [EvaluatedCandidate]):
    # 取得できたユーザーデータの辞書を作成しておく。
    user_ids = [str(t.user_id) for t in targets]
    url_prefix = 'https://twitter.com/'
    url_dict = dict(zip(user_ids, [url_prefix + t.screen_name for t in targets]))
    user_name_dict = dict(zip(user_ids, [t.username for t in targets]))
    screen_name_dict = dict(zip(user_ids, [t.screen_name for t in targets]))
    profile_dict = dict(zip(user_ids, [t.profile for t in targets]))
    job_category_possibility_dict = dict(zip(user_ids, [t.job_category_possibility for t in targets]))
    career_type_possibility_dict = dict(zip(user_ids, [t.career_type_possibility for t in targets]))
    job_category_contribute_words_dict = dict(zip(user_ids, [str(t.job_category_contribute_words) for t in targets]))
    career_type_contribute_words_dict = dict(zip(user_ids, [str(t.career_type_contribute_words) for t in targets]))
    now = timeutil_service.slushed_current_datetime()

    sheet = google_sheet_api_service.access_sheet(gid).worksheet(sheet_name)
    u_ids = sheet.col_values(1)
    start_row = len(u_ids) + 1
    end_row = start_row + len(targets) - 1
    _update_cells_with_list(sheet, 'A' + str(start_row), 'A' + str(end_row), user_ids, value_input_option=RAW_OPTION)
    _update_cells(sheet, 'B' + str(start_row), 'B' + str(end_row), user_ids, url_dict, value_input_option=RAW_OPTION)
    _update_cells(sheet, 'C' + str(start_row), 'C' + str(end_row), user_ids, user_name_dict, value_input_option=RAW_OPTION)
    _update_cells(sheet, 'D' + str(start_row), 'D' + str(end_row), user_ids, screen_name_dict, value_input_option=RAW_OPTION)
    _update_cells(sheet, 'E' + str(start_row), 'E' + str(end_row), user_ids, profile_dict, value_input_option=RAW_OPTION)
    _update_cells(sheet, 'F' + str(start_row), 'F' + str(end_row), user_ids, job_category_possibility_dict, value_input_option=USER_ENTERED_OPTION)
    _update_cells(sheet, 'G' + str(start_row), 'G' + str(end_row), user_ids, career_type_possibility_dict, value_input_option=USER_ENTERED_OPTION)
    _update_cells(sheet, 'H' + str(start_row), 'H' + str(end_row), user_ids, job_category_contribute_words_dict, value_input_option=RAW_OPTION)
    _update_cells(sheet, 'I' + str(start_row), 'I' + str(end_row), user_ids, career_type_contribute_words_dict, value_input_option=RAW_OPTION)
    _update_cells_by_value(sheet, 'K' + str(start_row), 'K' + str(end_row), now, value_input_option=USER_ENTERED_OPTION)


def check_searched(gid, sheet_name, row_num, col_num):
    sheet = google_sheet_api_service.access_sheet(gid).worksheet(sheet_name)
    now = timeutil_service.slushed_current_datetime()
    sheet.update_cell(row_num, col_num, now)


################
# privateメソッド
################
def _update_cells_with_list(sheet, from_cell, to_cell, id_list, value_input_option):
    cell_list = sheet.range('{}:{}'.format(from_cell, to_cell))
    count_num = -1
    for cell in cell_list:
        count_num += 1
        try:
            val = id_list[count_num]
        except Exception as e:
            continue
        if val is None:
            continue
        cell.value = val
    print('{}から{}まで書き込むよ'.format(from_cell, to_cell))
    sheet.update_cells(cell_list, value_input_option=value_input_option)


def _update_cells(sheet, from_cell, to_cell, id_list, dict, value_input_option):
    """
    {id: value}の辞書の値をシートに書き込んでいく。id_listの値を持っているdictのvalueをsheetのidの行に書き込んでいく。
    開始セルの位置=id_listの最初のid, 終了セルの位置=id_listの最後のid で対応している必要あり。
    :param sheet:
    :param from_cell:
    :param to_cell:
    :param id_list:
    :param dict:
    :param value_input_option: RAW:文字列(ex.「=1+1」と入力すると「=1+1」になる)。USER_ENTERED:関数や数値など(ex.「=1+1」と入力すると「2」になる)
    :return: 更新したセル数
    """
    cell_list = sheet.range('{}:{}'.format(from_cell, to_cell))
    count_num = -1
    updated_num = 0
    for cell in cell_list:
        count_num += 1
        try:
            val = dict[id_list[count_num]]
        except Exception as e:
            continue
        if val is None:
            continue
        cell.value = val
        updated_num += 1
    print('{}から{}まで書き込むよ'.format(from_cell, to_cell))
    sheet.update_cells(cell_list, value_input_option=value_input_option)
    return updated_num


def _update_cells_by_value(sheet, from_cell, to_cell, value, value_input_option):
    """
    指定した行から指定した行まで、valueで更新する。value_input_optionで文字列にするか、関数やdateやintを入力するか制御できる。
    :param sheet: Spread Sheet
    :param from_cell: 開始セル
    :param to_cell: 終了セル
    :param value: 入力値
    :param value_input_option: RAW:文字列(ex.「=1+1」と入力すると「=1+1」になる)。USER_ENTERED:関数や数値など(ex.「=1+1」と入力すると「2」になる)
    """
    cell_list = sheet.range('{}:{}'.format(from_cell, to_cell))
    for cell in cell_list:
        cell.value = value
    print('{}から{}まで書き込むよ'.format(from_cell, to_cell))
    sheet.update_cells(cell_list, value_input_option=value_input_option)
