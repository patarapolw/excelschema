# excelschema

Excel records' parser and schema viewing and validating tools.

## Installation

Method 1:

```
$ pip install excelschema
```

Method 2:
- Clone the project from GitHub
- `poetry install`

## Usage

To read an Excel file, you may also need to install [`pyexcel`](https://github.com/pyexcel/pyexcel) and [`pyexcel-xlsx`](https://github.com/pyexcel/pyexcel-xlsx) as well.

```python
>>> from excelschema import SchemaParser
>>> import pyexcel
>>> sp = SchemaParser(records=pyexcel.get_records(file_name='foo.xlsx', sheet_name='bar'))
>>> sp.schema
{
    'record_id': <class 'int'>,
    'modified': <class 'datetime.datetime'>,
    'data': <class 'str'>
}
```

Validating records and convert it to a usable one.

```python
>>> sp.ensure_one({'record_id': ' 12', 'data': 567})
{'record_id', 12, 'data': '567'}
```

Setting constraints

```python
>>> from excelschema import Constraint
>>> sp.update_schema({
...     'user_id': Constraint(type_=int, unique=True, not_null=True)
... })
```

It is also possible to create an custom schema without an Excel

```python
>>> sp = SchemaParser(schema={
...     'record_id': Constraint(type_=int, unique=True, not_null=True),
...     'modified': datetime
... })
```

## Bonus functions

Cleaning dirty Excel records

```python
>>> from excelschema import parse_record
>>> parse_record({'foo': ' 1', 'bar': ' - ', 'baz': ' '})
{'foo', 1}
```


## Related projects

- https://github.com/patarapolw/tinydb-constraint
