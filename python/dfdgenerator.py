import pydot
from graphviz import Source


def save_dot_to_png(dot_file):
    graphs = pydot.graph_from_dot_file(dot_file)
    graph = graphs[0] 
    graph.write_png('dfd_tm.png')

def create_dot_file(input_list: list):
    dot = pydot.Dot(graph_type='digraph')
    dot.obj_dict['attributes']['rankdir'] = 'LR'

    for item in input_list:
        if f'cluster_{item.trust_boundry}' not in get_subgraph_names(dot):
            sg = pydot.Subgraph(f'cluster_{item.trust_boundry}')
            sg.obj_dict['attributes']['shape'] = 'box'
            sg.obj_dict['attributes']['label'] = f'Trust boundary: {item.trust_boundry}'
            dot.add_subgraph(sg)
            resource = pydot.Node(item.name)
            resource.obj_dict['attributes']['label'] = f'{item.name}\nAWS resource type: {item.type}'
            sg.add_node(resource)
        elif f'cluster_{item.trust_boundry}' in get_subgraph_names(dot):
            resource = pydot.Node(item.name)
            resource.obj_dict['attributes']['label'] = f'{item.name}\nAWS resource type: {item.type}'
            sg = dot.get_subgraph(f'cluster_{item.trust_boundry}')
            subGraph = sg[0]
            subGraph.add_node(resource)

    for item in input_list:
        if len(item.data_flows) > 0:
            for df in item.data_flows:
                print(f'item: {item.name}. source: {df.source}, destination: {df.destination}\n')
                edge = pydot.Edge(df.source, df.destination)
                edge.obj_dict['attributes']['label'] = 'Dataflow'
                dot.add_edge(edge)
    dot.del_node('cluster_None')
    dot.write('dfd_tm.dot')
    
    save_dot_to_png('dfd_tm.dot')
    return dot


def get_subgraph_names(dot):
    return [subgraph.get_name() for subgraph in dot.get_subgraph_list()]