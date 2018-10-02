from typing import NamedTuple, Any, Union


class Constraint(NamedTuple):
    type_: Union[type, list, type(Any)] = Any
    unique: bool = False
    not_null: bool = False


class ConstraintMapping:
    def __init__(self):
        self.type_ = dict()
        self.preexisting = dict()
        self.not_null = set()

    def update(self, schema_dict):
        if schema_dict:
            for k, c in schema_dict.items():
                if isinstance(c, type):
                    self._parse_type(k, c)
                else:
                    assert isinstance(c, Constraint), repr(c)

                    if c.type_:
                        self._parse_type(k, c.type_)
                    if c.unique:
                        self.preexisting.setdefault(k, set())
                    if c.not_null:
                        self.not_null.add(k)

    def _parse_type(self, k, type_):
        if k in self.type_.keys():
            expected_type = self.type_[k]
            if expected_type is not Any:
                if type_ is not expected_type:
                    raise TypeError
        else:
            self.type_[k] = type_

    def _view(self):
        all_keys = set(self.type_.keys()) | set(self.preexisting.keys()) | self.not_null

        for k in all_keys:
            type_ = self.type_.get(k, Any)
            unique = k in self.preexisting.keys()
            not_null = k in self.not_null

            yield k, Constraint(type_, unique, not_null)

    def view(self):
        return dict(self._view())

    def __repr__(self):
        return repr(self.view())
