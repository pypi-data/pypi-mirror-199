import re
from typing import List
class BaseModel():
    def __init__(self):
        pass

    def _pattern_matching(cls, value: str, pattern: str, variable_name: str):
        if re.match(r'{}'.format(pattern), value):
            return value
        else:
            raise ValueError(f'Invalid value for {variable_name}: must match {pattern}')

    def _enum_matching(cls, value: str, enum_values: List[str], variable_name: str):
        if value in enum_values:
            return value
        else:
            raise ValueError(f'Invalid value for {variable_name}: must match one of {enum_values}')

    @classmethod
    def _one_of(cls, required_array, all_array, functions_array, input_data):
        input_array = list(input_data.keys())
        for model, fields in required_array.items():
            matches_required = True
            for param in fields:
                if param not in input_array:
                    matches_required = False
                    break
                input_array.remove(param)
            if matches_required:
                matches_all = True
                for input in input_array:
                    if input not in all_array[model]:
                        matches_all = False
                        break
                if matches_all:
                    return functions_array[model](input_data)

