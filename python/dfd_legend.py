import pydot

''' This python code was used to generate the legend for the DFDs as a figure in the thesis'''

dot = pydot.Dot(graph_type='digraph', rankdir = 'LR', strict=True)
node = pydot.Subgraph('cluster0', label='Trust boundary: <Name of trust boundary>')
node.obj_dict['attributes']['shape'] = 'box'
nd = pydot.Node('B', label='Name: <Name of resource>\nAWS resource type: <Type of resource>')
ndd = pydot.Node('c', label='Name: <Name of resource>\nAWS resource type: <Type of resource>')
nd.obj_dict['attributes']['shape'] = 'box'
ndd.obj_dict['attributes']['shape'] = 'box'
node.add_node(nd)
node.add_node(ndd)
edge = pydot.Edge('B','c')
dot.add_edge(edge)
edge.obj_dict['attributes']['label'] = f'Dataflow\n from <Name of Source-resource> to <Name of Sink-resource>\n In Trust Boundary/Crossses Trust Boundary'
dot.add_subgraph(node)
dot.write_png('box.png')