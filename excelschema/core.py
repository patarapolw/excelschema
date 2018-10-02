from collections import OrderedDict
from copy import deepcopy

from .constraint import ConstraintMapping
from .exception import NotUniqueException, NotNullException, NonUniformTypeException
from .util import parse_record


class SchemaParser:
    constraint_mapping = ConstraintMapping()
    records = list()

    def __init__(self, records=None, as_datetime_str=False, schema=None):
        self.as_datetime_str = as_datetime_str

        if records:
            if isinstance(records[0], (list, tuple)):
                new_records = list()
                header = records[0]
                for row in records[1:]:
                    new_records.append(OrderedDict(zip(header, row)))

                records = new_records

        if schema:
            self.constraint_mapping.update(schema)

        self.records = self.ensure_multiple(records)

    @property
    def schema(self):
        """Get table's latest schema

        Returns:
            dict -- dictionary of constraints
        """

        return self.constraint_mapping.view()

    @schema.setter
    def schema(self, schema_dict):
        """Reset and set a new schema

        Arguments:
            schema_dict {dict} -- dictionary of constraints or types
        """

        self.constraint_mapping = ConstraintMapping()
        self.update_schema(schema_dict)

    def update_schema(self, schema_dict):
        """Update the schema

        Arguments:
            schema_dict {dict} -- dictionary of constraints or types
        """

        self.constraint_mapping.update(schema_dict)
        self.ensure_multiple(self.records)

    def ensure_multiple(self, records, update_schema=False):
        """Sanitizes records, e.g. from Excel spreadsheet

        Arguments:
            records {list, tuple} -- Iterable of records. Can be a 2-D array of list of dictionaries

        Returns:
            list -- List of records
        """

        def _records():
            nonlocal records

            header = None
            if isinstance(records[0], (list, tuple)):
                header = records[0]
                records = records[1:]

            for record_ in records:
                if isinstance(record_, (list, tuple)):
                    record_ = dict(zip(header, record_))

                record_schema = parse_record(record_, yield_='type')
                num_to_str = set()
                for k, v in record_schema.items():
                    expected_type = self.constraint_mapping.type_.get(k, None)
                    if expected_type and v is not expected_type:
                        if expected_type is str and v in (int, float):
                            num_to_str.add(k)
                        else:
                            raise NonUniformTypeException('{} not in table schema {}'
                                                          .format(v, self.schema))
                    self.constraint_mapping.update(schema_dict=record_schema)

                record_ = parse_record(record_, yield_='record',
                                       as_datetime_str=self.as_datetime_str)
                for k, v in record_.items():
                    if k in num_to_str:
                        record_[k] = str(v)

                is_null = self.constraint_mapping.not_null - set(record_.keys())
                if len(is_null) > 0:
                    raise NotNullException('{} is null'.format(list(is_null)))

                yield record_

        temp_mapping = None
        if not update_schema:
            temp_mapping = deepcopy(self.constraint_mapping)

        for c in self.schema.values():
            assert not isinstance(c.type_, list)

        records = list(_records())
        for record in records:
            self._update_uniqueness(record)

        if not update_schema:
            self.constraint_mapping = ConstraintMapping()
            self.constraint_mapping.update(temp_mapping)
        else:
            self.records.extend(records)

        return records

    def ensure_one(self, record, update_schema=False):
        return self.ensure_multiple([record], update_schema=update_schema)[0]

    def _update_uniqueness(self, record_dict):
        for k, v in parse_record(record_dict, yield_='type').items():
            if k in self.constraint_mapping.preexisting.keys():
                if v in self.constraint_mapping.preexisting[k]:
                    raise NotUniqueException('Duplicate {} for {} exists'.format(v, k))

                self.constraint_mapping.preexisting[k].add(v)
