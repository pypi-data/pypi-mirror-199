import {ForceDirectedGraphModel, ForceDirectedGraphView} from './forceDirectedGraph';
import {HierarchicalGraphModel, HierarchicalGraphView} from './hierarchicalGraph';
import {version} from '../package.json';
import {IJupyterWidgetRegistry} from '@jupyter-widgets/base';

export const ipyd3Plugin = {
  id: 'ipyd3:plugin',
  requires: [IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'ipyd3',
          version: version,
          exports: { 
            ForceDirectedGraphModel, ForceDirectedGraphView,
            HierarchicalGraphModel, HierarchicalGraphView 
          }
      });
  },
  autoStart: true
};

export default ipyd3Plugin;
