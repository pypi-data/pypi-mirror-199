import enum
from typing import Union
from atlas_consortia_commons.string import to_snake_case


def build_enum_class(class_name: str, data: Union[list, dict], key: str = None, val_callback=None,
                     obj_type: str = 'class'):
    _props = {}
    try:
        if type(data) is list:
            for item in data:
                val = item.get(key)
                prop = to_snake_case(val).upper()
                _props[prop] = val if val_callback is None else val_callback(val)
        else:
            if key is not None:
                val = data.get(key)
                prop = to_snake_case(val).upper()
                _props[prop] = val if val_callback is None else val_callback(val)
            else:
                _props = data
        if obj_type == 'enum':
            return enum.Enum(class_name, _props)
        else:
            return type(class_name, (), _props)
    except Exception as e:
        print(e)
