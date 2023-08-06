import datetime
import math
import time

def to_excel_date(number_of_days):
    if type(number_of_days) == str:
        return number_of_days
    else:
        return datetime.datetime(1900, 1, 1) + datetime.timedelta(days=number_of_days - 2)

def to_excel_datetime(number_of_days):
    if type(number_of_days) == str:
        return number_of_days
    else:
        return datetime.datetime.fromordinal(datetime.datetime(1900, 1, 1).toordinal() + int(number_of_days - 2)) + datetime.timedelta(days=number_of_days % 1)

def sqlescape(str):
    return str.translate(
        str.maketrans({
            "\0": "' || CHR(0) || '",
            "\r": "' || CHR(10) || '",
            "\x08": "' || CHR(8) || '",
            "\x09": "' || CHR(9) || '",
            "\n": "' || CHR(13) || '",
            "\r": "' || CHR(10) || '",
            "\"": "' || CHR(22) || '",
            "'": "' || CHR(27) || '",
            "\\": "' || CHR(92) || '",
            "%": "' || CHR(37) || '"
        }))

def split_oracle_string(str, max_size):
    chunks = []
    for i in range(0, len(str), max_size):
        chunks.append(f"'{sqlescape(str[i:i + max_size])}'")
    return chunks

def sanitize(value):
    if type(value) == str:
        return " ||\n".join(split_oracle_string(value, 1000))
    elif isinstance(value, datetime.datetime):
        return f"'{value.strftime('%m/%d/%Y')}'"
    else:
        return value if value != None and not math.isnan(value) else 'null'

def generate_log_filename():
    now = datetime.datetime.now()
    return f"assets-data-{now.strftime('%Y-%m-%d %H:%M:%S.%f')}.sql"

def current_milli_time():
    return int(round(time.time() * 1000))
