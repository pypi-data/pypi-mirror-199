import ipywidgets as _widgets
from traitlets import TraitType as _TraitType, Type as _Type, Any as _Any, Unicode as _Unicode, Bool as _Bool, Int as _Int, validate as _validate, TraitError as _TraitError
from .network_traitlet import Graph

@_widgets.register
class HierarchicalGraph(_widgets.DOMWidget):
    """
        Widget that creates a D3 Hierarchical Graph

        Parameters:
            data - Data to be passed to the graph. It can be a networkx graph or a dictionary in form of ex. {nodes: [], edges:[]}
            graph_type - There are currently two options, "file_directory" format and "generic" format. Defaults to "generic"
            height - Height of graph area. Default to 500.
            width - Width of graph area. Default to 950.

    """

    # Name of the widget view class in front-end
    _view_name = _Unicode('HierarchicalGraphView').tag(sync=True)

    # Name of the widget model class in front-end
    _model_name = _Unicode('HierarchicalGraphModel').tag(sync=True)

    # Name of the front-end module containing widget view
    _view_module = _Unicode('ipyd3').tag(sync=True)

    # Name of the front-end module containing widget model
    _model_module = _Unicode('ipyd3').tag(sync=True)

    # Version of the front-end module containing widget view
    _view_module_version = _Unicode('^3.0.1').tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = _Unicode('^3.0.1').tag(sync=True)

    # Widget specific property.
    # Widget properties are defined as traitlets. Any property tagged with `sync=True`
    # is automatically synced to the frontend *any* time it changes in Python.
    # It is synced back to Python from the frontend *any* time the model is touched.
    data = _Any({}).tag(sync=True)
    graph_type = _Unicode("generic").tag(sync=True)
    depth = _Int(3).tag(sync=True)
    height = _Int(500).tag(sync=True)
    width = _Int(950).tag(sync=True)
    directory_columns = _Any([]).tag(sync=True)

    # Basic validator for the floater value
    @_validate('data')
    def _valid_data(self, proposal):
        if isinstance(proposal['value'], dict):
            return proposal['value']
        raise _TraitError('Invalid data value. Provide a JSON object.')

    # Basic validator for the floater value
    @_validate('graph_type')
    def _valid_filter(self, proposal):
        if isinstance(proposal['value'], str):
            if proposal['value'] == "generic" or proposal['value'] == "file_directory":
                return proposal['value']
            else:
                raise _TraitError('Invalid graph_type value. Approriate values are generic or file_directory')
        raise _TraitError('Invalid graph_type value. Provide a string.')

    # Basic validator for the width value
    @_validate('depth')
    def _valid_width(self, proposal):
        if isinstance(proposal['value'], int):
            return proposal['value']
        raise _TraitError('Invalid width. Provide a number.')

    # Basic validator for the width value
    @_validate('width')
    def _valid_width(self, proposal):
        if isinstance(proposal['value'], int):
            return proposal['value']
        raise _TraitError('Invalid width. Provide a number.')

    # Basic validator for the height value
    @_validate('height')
    def _valid_height(self, proposal):
        if isinstance(proposal['value'], int):
            return proposal['value']
        raise _TraitError('Invalid height provide a number.')

    # Basic validator for the floater value
    @_validate('directory_columns')
    def _valid_data(self, proposal):
        if isinstance(proposal['value'], list):
            return proposal['value']
        raise _TraitError('Invalid data value. Provide a JSON object.')
