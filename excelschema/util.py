import unicodedata
from datetime import datetime, date
import dateutil.parser


def normalize_chars(s):
    return unicodedata.normalize("NFKD", s)


def jsonify(d):
    for k, v in d.items():
        if isinstance(v, datetime):
            yield k, v.isoformat()
        else:
            yield k, v


def parse_record(record, yield_='type',  as_datetime_str=False):
    def _yield_switch(x):
        if yield_ == 'type':
            return type(x)
        elif yield_ == 'record':
            if isinstance(x, (datetime, date)):
                x = x.isoformat()
                if not as_datetime_str:
                    x = dateutil.parser.parse(x)

            return x
        else:
            raise ValueError

    for k, v in record.items():
        if isinstance(v, str):
            v = normalize_chars(v.strip())
            if v.isdigit():
                v = int(v)
            elif '.' in v and v.replace('.', '', 1).isdigit():
                v = float(v)
            elif v in {'', '-'}:
                continue
            else:
                try:
                    v = dateutil.parser.parse(v)
                except ValueError:
                    pass
        elif isinstance(v, date):
            v = datetime.combine(v, datetime.min.time())

        yield k, _yield_switch(v)