# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class EALayout(Component):
    """An EALayout component.
Layout used by Energy Aspects apps

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Main content.

- id (string; optional):
    Layout wrapper Id.

- className (string; optional):
    Layout wrapper className.

- drawerContent (a list of or a singular dash component, string or number; optional):
    Contents of drawer.

- fixedSecondaryHeader (boolean; optional)

- headerContent (a list of or a singular dash component, string or number; optional):
    Contents of header.

- logoUrl (string; optional):
    `href` passed to on logo click.

- open (boolean; required):
    Signifies if drawer of Layout is open.

- secondaryHeaderContent (a list of or a singular dash component, string or number; optional):
    Contents of secondary header. Won't be present if not specified.

- showLeftHandNav (boolean; optional):
    Toggle off and on the drawer and sidebar.

- sidebarContent (a list of or a singular dash component, string or number; optional):
    Contents of sidebar."""
    _children_props = ['sidebarContent', 'drawerContent', 'headerContent', 'secondaryHeaderContent']
    _base_nodes = ['sidebarContent', 'drawerContent', 'headerContent', 'secondaryHeaderContent', 'children']
    _namespace = 'ea_dash'
    _type = 'EALayout'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, sidebarContent=Component.UNDEFINED, drawerContent=Component.UNDEFINED, headerContent=Component.UNDEFINED, secondaryHeaderContent=Component.UNDEFINED, fixedSecondaryHeader=Component.UNDEFINED, logoUrl=Component.UNDEFINED, open=Component.REQUIRED, showLeftHandNav=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'drawerContent', 'fixedSecondaryHeader', 'headerContent', 'logoUrl', 'open', 'secondaryHeaderContent', 'showLeftHandNav', 'sidebarContent']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'drawerContent', 'fixedSecondaryHeader', 'headerContent', 'logoUrl', 'open', 'secondaryHeaderContent', 'showLeftHandNav', 'sidebarContent']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['open']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(EALayout, self).__init__(children=children, **args)
