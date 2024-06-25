import time
import re


def get_now_timestamp_in_seconds():
    return time.time()

def get_now_timestamp_in_milliseconds():
    return time.time() * 1000


ARRAY_MESSAGE_COMPILED_PATTERN = re.compile(r"\*[+-]?\d+\r\n|\+.+\r\n|\$\d+\r\n.+\r\n|\$-1\r\n|-.+\r\n|:[+-]?\d+\r\n")
ARRAY_DEF_GROUPS_COMPILED_PATTERN = re.compile(r"\*([+-]?\d+)\r\n")
