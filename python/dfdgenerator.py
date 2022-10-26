import pydot




def create_dot_file(input_list: list, filename: str):
    dot = pydot.Dot(graph_type='digraph')
    dot.obj_dict['attributes']['labelloc'] = 't'
    dot.obj_dict['attributes']['label'] = f'Data-flow diagram for {filename}'

    for item in input_list:
        if item.trust_boundry == 'None':
            pass
        elif f'cluster_{item.trust_boundry}' not in get_subgraph_names(dot):
            sg = pydot.Subgraph(f'cluster_{item.trust_boundry}')
            sg.obj_dict['attributes']['shape'] = 'box'
            sg.obj_dict['attributes']['label'] = f'Trust boundary: {item.trust_boundry}'
            dot.add_subgraph(sg)
            resource = pydot.Node(item.name)
            resource.obj_dict['attributes']['label'] = f'Name: {item.name}\nAWS resource type: {item.type}'
            resource.obj_dict['attributes']['shape'] = 'box'
            sg.add_node(resource)
        elif f'cluster_{item.trust_boundry}' in get_subgraph_names(dot):
            resource = pydot.Node(item.name)
            resource.obj_dict['attributes']['label'] = f'Name: {item.name}\nAWS resource type: {item.type}'
            resource.obj_dict['attributes']['shape'] = 'box'
            sg = dot.get_subgraph(f'cluster_{item.trust_boundry}')
            subGraph = sg[0]
            subGraph.add_node(resource)

    for item in input_list:
        if len(item.data_flows) > 0:
            for df in item.data_flows:
                edge = pydot.Edge(df.source, df.destination)
                edge.obj_dict['attributes']['label'] = 'Dataflow'
                dot.add_edge(edge)
    
    dot.write('dfd_tm.dot')
    dot.write_png('dfd_tm.png')
    return dot


def get_subgraph_names(dot):
    return [subgraph.get_name() for subgraph in dot.get_subgraph_list()]