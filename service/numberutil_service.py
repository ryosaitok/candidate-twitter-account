# coding=utf-8


def format_comma_decimal(float_num, decimal_point):
    """
    format float number to float with one decimal and comma (ex. float_num=1213213.708, decimal_point=2 -> 1,213,213.70)
    if decimal point is 0, return integer.
    :param float_num: float number
    :param decimal_point: the point of decimal
    :return: float num
    """
    format_text = '{:,.' + str(decimal_point) + 'f}'
    return format_text.format(float_num)
