import pydot


def save_dot_to_png(dot_file):
    graphs = pydot.graph_from_dot_file(dot_file)
    graph = graphs[0]
    graph.write_png('dfd_tm.png')

def create_dot_file(input_list: list):
    dot = pydot.Dot(graph_type='digraph')
    for item in input_list:
        if item.trust_boundry not in get_subgraph_names(dot):
            sg = pydot.Subgraph(item.trust_boundry)
            sg.obj_dict['attributes']['label'] = f'Trust boundary: {item.trust_boundry}'
            dot.add_subgraph(sg)
            resource = pydot.Node(item.name)
            sg.add_node(resource)
        elif item.trust_boundry in get_subgraph_names(dot):
            resource = pydot.Node(item.name)
            sg = dot.get_subgraph(item.trust_boundry)
            subGraph = sg[0]
            subGraph.add_node(resource)     
    dot.write('dfd_tm.dot')
    return dot


def get_subgraph_names(dot):
    return [subgraph.get_name() for subgraph in dot.get_subgraph_list()]