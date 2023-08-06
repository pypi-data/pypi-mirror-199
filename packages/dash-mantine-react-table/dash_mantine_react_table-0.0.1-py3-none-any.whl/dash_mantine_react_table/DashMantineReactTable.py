# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashMantineReactTable(Component):
    """A DashMantineReactTable component.
A simple wrapper over Mantine React Table. For more information have a look at https://www.mantine-react-table.com.

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional):
    class name for styling.

- columns (list of boolean | number | string | dict | lists; required):
    columns.

- data (list of boolean | number | string | dict | lists; required):
    data.

- mantineProviderProps (boolean | number | string | dict | list; optional):
    MantineProvider theme.

- mrtProps (boolean | number | string | dict | list; optional):
    MRT props."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_react_table'
    _type = 'DashMantineReactTable'
    @_explicitize_args
    def __init__(self, data=Component.REQUIRED, columns=Component.REQUIRED, mrtProps=Component.UNDEFINED, mantineProviderProps=Component.UNDEFINED, id=Component.UNDEFINED, className=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'columns', 'data', 'mantineProviderProps', 'mrtProps']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'columns', 'data', 'mantineProviderProps', 'mrtProps']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['columns', 'data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(DashMantineReactTable, self).__init__(**args)
