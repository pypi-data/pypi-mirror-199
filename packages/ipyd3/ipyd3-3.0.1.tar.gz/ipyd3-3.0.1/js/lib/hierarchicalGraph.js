// Based of Mike Bostock at https://observablehq.com/@d3/indented-tree?collection=@d3/d3-hierarchy
// and https://observablehq.com/@d3/collapsible-tree 
try{
  if(window._JUPYTERLAB){
    var lab = true;
  }else{
    var lab = false;
  }
}
catch{
  var lab = false;
}

var widgets = require('@jupyter-widgets/base');
const { scaleLog } = require('d3');

var d3 = require("d3");
if(lab){
  require('bootstrap')
  require('bootstrap/dist/css/bootstrap.min.css');
}


var HierarchicalGraphModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name : 'HierarchicalGraphModel',
        _view_name : 'HierarchicalGraphView',
        _model_module : 'ipyd3',
        _view_module : 'ipyd3',
        _model_module_version : '3.0.1',
        _view_module_version : '3.0.1',
        data:{},
        width:500,
        height:500
    })
});

// Custom View. Renders the widget model.
var HierarchicalGraphView = widgets.DOMWidgetView.extend({
    
    render: function() {
        let self = this;
        const graph_type = self.model.get('graph_type');
        if(graph_type == "generic"){
          self.display_collapsable_graph()
        }
        else if (graph_type == "file_directory"){
          self.tbb = document.createElement('p');
          self.tbb.id = "tbb"+self.cid;
          self.tbb.innerHTML = "To be built. Coming in future version.";
          self.el.appendChild(self.tbb);
          // self.display_file_path_graph();
        }
        
        // Python -> JavaScript update
        // self.model.on('change:graph', self.graph_changed, this);
        // self.model.on('change:floater', self.floater_changed, this);
        // self.model.on('change:label', self.update_graph, this);
        // self.model.on('change:icon', self.update_graph, this);

        // self.graph_update_binded = self.graph_update.bind(this);

    },
    generate_input_area : (self) =>{
      // Creting input area for highlihting node.
      self.input_div = document.createElement('div');
      self.input_div.id = "input_div_"+self.cid;

      self.el.appendChild(self.input_div);

      // Create our stylesheet
      self.style_input_div = document.createElement('style');
      self.style_input_div.innerHTML =
      '#input_div_'+self.cid+' {' +
          'left:0;' +
          'top:0;' +
          'position:absolute;'+
          'display:block;' +
          'background-color: #e5e5e5;'
      '};';

      self.el.appendChild(self.style_input_div)
      // End input area

      // Create our stylesheet
      self.input_box = document.createElement('input');
      self.input_box.id = "input_search_"+self.cid;
      self.input_box.setAttribute("type", "text");
      self.input_box.setAttribute("placeholder", "Search by id...");
      self.input_box.setAttribute("style","font-size: 14px; padding-top: 4px; padding-bottom: 4px;")
      self.input_div.appendChild(self.input_box)

      self.button_layer = document.createElement('button');
      self.button_layer.id = "button_search_"+self.cid;
      self.button_layer.className = "btn btn-primary";
      self.button_layer.innerHTML = "search";
      self.button_layer.setAttribute("style","float: right;font-size: 14px;");
      self.button_layer.onclick = self.update


      self.input_div.appendChild(self.button_layer)
      
    },
    generate_paths: (self, name, node) => {      
      let search_value = "";
      try{
        search_value = self.input_box.value;
        if(name.includes(search_value) && search_value != "" ){
          let path = node.path(self.root);
  
          path.forEach((element, index) => {
            if(element.id in self.highlight_links){
              try{
                self.highlight_links[element.id].push(path[index+1].id)
              }
              catch{
                console.log("Hit end")
              }
            }
            else{
              try{
                self.highlight_links[element.id] = [path[index+1].id]
              }
              catch{
                console.log("Hit end")
              }
              
            }
          })
        }
      }
      catch{
        console.log("No input yet")
      }  
    },

    highlight: (self, source, target) => {
      console.log(self.highlight_links)
      if(source in self.highlight_links && self.highlight_links[source].includes(target)){
        return true
      }
      else if (target in self.highlight_links && self.highlight_links[target].includes(source)){
        return true
      }
      return false
    },

    display_collapsable_graph: function() {
      let self = this;
      let tempData = self.model.get('data');
      var width = self.model.get('width');
      var height = self.model.get('height');
      const margin = ({top: 10, right: 120, bottom: 10, left: 40})
      const dy = width / 6
      const dx = 10
      const diagonal = d3.linkHorizontal().x(d => d.y).y(d => d.x)
      const tree = d3.tree().nodeSize([dx, dy])
      const root = d3.hierarchy(tempData);
      self.full_root = d3.hierarchy(tempData);
      self.root = root;
      self.highlight_links = {};

      root.x0 = dy / 2;
      root.y0 = 0;
      
      self.full_root.descendants().forEach((d, i) => {
        d.id = i;
      });
      root.descendants().forEach((d, i) => {
        d.id = i;
        d._children = d.children;
        if (d.depth && d.depth == self.model.get('depth')) d.children = null;
      });

      var zoom = d3.zoom()
        .scaleExtent([.1, 10])
        .on("zoom", function() { container.attr("transform", d3.event.transform); });

      var svg = d3.select(self.el).append("svg").attr("width", width).attr("height", height).call(zoom);

      var container = svg.append("g").attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("transform", `translate(${margin.left},${width / 6})`);


      const gLink = container.append("g")
        .attr("fill", "none")
        .attr("stroke-opacity", 0.4)
        .attr("stroke-width", 1.5);

      const gNode = container.append("g")
        .attr("cursor", "pointer")
        .attr("pointer-events", "all");

      self.update = (source) =>{
        
        if("bubbles" in source){
          self.highlight_links = {}
          source = self.root;
        }
        
        self.full_root.descendants().forEach((d) => {
          self.generate_paths(self,d.data.name,d);
        })
        
        const duration = 250;
        const nodes = self.root.descendants().reverse();
        const links = self.root.links();
    
        // Compute the new tree layout.
        tree(self.root);

        let left = self.root;
        let right = self.root;
        self.root.eachBefore(node => {
          if (node.x < left.x) left = node;
          if (node.x > right.x) right = node;
        });

        const transition = container.transition()
            .duration(duration)

        // Update the nodes…
        const node = gNode.selectAll("g")
          .data(nodes, d => d.id);

        // Enter any new nodes at the parent's previous position.
        const nodeEnter = node.enter().append("g")
            .attr("transform", d => `translate(${source.y0},${source.x0})`)
            .attr("fill-opacity", 0)
            .attr("stroke-opacity", 0)
            .on("click", (d) => {
              
              d.children = d.children ? null : d._children;
              self.update(d);
            });

        nodeEnter.append("circle")
            .attr("r", 2.5)
            .attr("fill", d => d._children ? "#555" : "#999")
            .attr("stroke-width", 10);

        nodeEnter.append("text")
            .attr("dy", "0.31em")
            .attr("x", d => d._children ? -6 : 6)
            .attr("text-anchor", d =>  d._children ? "end" : "start")
            .text(d => {return d.data.name})
            .clone(true).lower()
            .attr("stroke-linejoin", "round")
            .attr("stroke-width", 3)
            .attr("stroke", "white");

        // Transition nodes to their new position.
        const nodeUpdate = node.merge(nodeEnter).transition(transition)
            .attr("transform", d => `translate(${d.y},${d.x})`)
            .attr("fill-opacity", 1)
            .attr("stroke-opacity", 1);

        // Transition exiting nodes to the parent's new position.
        const nodeExit = node.exit().transition(transition).remove()
            .attr("transform", d => `translate(${source.y},${source.x})`)
            .attr("fill-opacity", 0)
            .attr("stroke-opacity", 0);

        // Update the links…
        const link = gLink.selectAll("path")
          .data(links, d => d.target.id);

        // Enter any new links at the parent's previous position.
        const linkEnter = link.enter().append("path")
            .attr("stroke", d => self.highlight(self, d.source.id, d.target.id) ? "red" :"#999")
            .attr("d", d => {
              const o = {x: source.x0, y: source.y0};
              return diagonal({source: o, target: o});
            });

        // Transition links to their new position.
        link.merge(linkEnter).transition(transition)
            .attr("d", diagonal)
            

        // Transition exiting nodes to the parent's new position.
        link.exit().transition(transition).remove()
            .attr("d", d => {
              const o = {x: source.x, y: source.y};
              return diagonal({source: o, target: o});
            });
        
        gLink.selectAll("path")
            .attr("stroke", d => self.highlight(self, d.source.id, d.target.id) ? "red" :"#999")
            
        // Stash the old positions for transition.
        source.eachBefore(d => {
          d.x0 = d.x;
          d.y0 = d.y;
        });
      }
      self.generate_input_area(self)
      self.update(root)
    },

    display_file_path_graph: function() {
      let self = this;

      let tempData = self.model.get('data');
      let nodeSize = 17;      
      var width = self.model.get('width');
      var height = self.model.get('height');
      self.highlight_links = {};
      let i = 0;
      let root = d3.hierarchy(tempData).eachBefore(d => d.id = i++);
      root.id0 = root.id
      self.root = root;
      self.full_root = d3.hierarchy(tempData).eachBefore(d => d.id = i++);

      root.descendants().forEach((d, i) => {
        d._children = d.children;
        if (d.depth && d.depth == self.model.get('depth')) d.children = null;
      });
      var columns = self.model.get('directory_columns');
      
      var zoom = d3.zoom()
                	.scaleExtent([.1, 10])
                	.on("zoom", function() { container.attr("transform", d3.event.transform); });

      var svg = d3.select(this.el).append("svg").attr("width", width).attr("height", height).call(zoom);
      var container = svg.append("g");

      zoom.scaleTo(svg, .6);
      self.generate_input_area(self);

      const gLink = container.append("g")
        .attr("fill", "none")
        .attr("stroke-opacity", 0.4)
        .attr("stroke-width", 1.5);

      const gNode = container.append("g")
        .attr("cursor", "pointer")
        .attr("pointer-events", "all");

      let ids = [0]

      self.update = (source) => {
        if("bubbles" in source){
          self.highlight_links = {}
          source = self.root;
        }

        self.full_root.descendants().forEach((d) => {
          self.generate_paths(self,d.data.name,d);
        })
        const nodes = self.root.descendants().reverse();
        const links = self.root.links();
        console.log("links",links)
        console.log("source links",source.links())
        console.log(source);

        const transition = container.transition()
          .duration(250)

        // Update the nodes…
        const node = gNode.selectAll("g")
          .data(nodes, d => d.id);

        // Enter any new nodes at the parent's previous position.
        const nodeEnter = node.enter().append("g")
            .attr("transform", d => `translate(0,${source.id0-1 * nodeSize})`)
            .on("click", (d) => {
              d.children = d.children ? null : d._children;
              self.update(d);
            });

        nodeEnter.append("circle")
            .attr("cx", d => d.depth * nodeSize)
            .attr("r", 2.5)
            .attr("fill", d => d.children ? null : "#999");

        nodeEnter.append("text")
            .attr("dy", "0.32em")
            .attr("x", d => d.depth * nodeSize + 6)
            .text(d => d.data.name);
        
        // Transition nodes to their new position.
        const nodeUpdate = node.merge(nodeEnter).transition(transition)
            .attr("transform", d => `translate(0,${d.id * nodeSize})`)
            .attr("fill-opacity", 1)
            .attr("stroke-opacity", 1);

        // Transition exiting nodes to the parent's new position.
        const nodeExit = node.exit().transition(transition).remove()
            .attr("transform", d => `translate(0,${source.id-1 * nodeSize})`)
            .attr("fill-opacity", 0)
            .attr("stroke-opacity", 0);
    
        // Columns
        node.append("title")
            .text(d => d.ancestors().reverse().map(d => d.data.name).join("/"));
        for (const {label, value, separation} of columns) {
          container.append("text")
              .attr("dy", "0.32em")
              .attr("y", -nodeSize)
              .attr("x", separation)
              .attr("text-anchor", "end")
              .attr("font-weight", "bold")
              .text(label);

          node.append("text")
              .attr("dy", "0.32em")
              .attr("x", separation)
              .attr("text-anchor", "end")
            .data(nodes)
              .text(d =>{
                return d['data'][value]
              });
              
          // Update the links…
          const link = gLink.selectAll("path")
            .data(links, d => d.target.id);

          // Enter any new links at the parent's previous position.
          const linkEnter = link.enter().append("path")
              .attr("stroke", d => self.highlight(self, d.source.id, d.target.id) ? "red" :"#999")

              .attr("d", d => `
                M${source.depth * nodeSize},${source.id0 * nodeSize}
                V${source.id0+1 * nodeSize}
                h${nodeSize}
              `);

          if(source.id != 0 && ids.includes(source.id)){
            ids = ids.filter(function(item) {
              return item !== source.id
            })
          } else if (source.id != 0 ){
            ids.push(source.id)
          }

          // Transition links to their new position.
          link.merge(linkEnter).transition(transition)
              // .attr("d", diagonal)
              .attr("d", d => {
                let subs = ids.reduce((a,b)=>a+b)
                let source_sub = subs != 0 && d.source.id > subs? d.source.id -subs:0
                let target_sub = subs != 0 && d.target.id > subs? d.target.id -subs:0
                  return `
                    M${d.source.depth * nodeSize},${(d.source.id - source_sub) * nodeSize}
                    V${(d.target.id -target_sub)* nodeSize}
                    h${nodeSize}
                  `
              });
              

          // Transition exiting nodes to the parent's new position.
          link.exit().transition(transition).remove()
          .attr("d", d => `
            M${source.depth * nodeSize},${source.id * nodeSize}
            V${source.id+1 * nodeSize}
            h${nodeSize}
          `);
          
          // gLink.selectAll("path")
          //     .attr("stroke", d => self.highlight(self, d.source.id, d.target.id) ? "red" :"#999")

          // Stash the old positions for transition.
          source.eachBefore(d => {
            d.id0 = d.id
          });
        }
      }
      self.update(root)
    }
    
})

module.exports = {
  HierarchicalGraphModel: HierarchicalGraphModel,
  HierarchicalGraphView: HierarchicalGraphView
};