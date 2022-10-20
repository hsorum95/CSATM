import pydot

def save_dot(dot_file):
    graphs = pydot.graph_from_dot_file(dot_file)
    graph = graphs[0]
    file_save_location = input('Where do you want the file to saved?')
    graph.write_png(file_save_location)

#dump cloudformation to dotfile
def dump_to_dot(input_dict):
    resource_list = get_resources(input_dict)
    dot = pydot.Dot(graph_type='digraph')
    for key in resource_list:
        dot.add_node(pydot.Node(key))
    for key in resource_list:
        if resource_list[key] == 'AWS::CloudFormation::Stack':
            for sub_key in resource_list:
                if resource_list[sub_key] == 'AWS::CloudFormation::Stack':
                    dot.add_edge(pydot.Edge(key, sub_key))
    dot.write('test.dot')
