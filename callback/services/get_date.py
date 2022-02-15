from datetime import datetime
import re


def get_date(post: list[str]):
    for line in post:
        for word in line.split(' '):
            date = re.match(r"^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$", word)
            if date:
                return datetime.strptime(word, '%Y-%m-%d')
    return None
