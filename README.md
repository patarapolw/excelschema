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
    'record_id': Constraint(type_=int, unique=False, not_null=False),
    'modified': Constraint(type_=datetime.datetime, unique=False, not_null=False)
}
```

Validating records and convert it to a usable one.

```python
>>> sp.ensure_one({'foo': ' 1', 'bar': '-'})
{'foo', 1}
```

Setting constraints

```python
>>> from tinydb_constraint import Constraint
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

## Related projects

- https://github.com/patarapolw/tinydb-constraint
