from collections import OrderedDict
import yaml
import pydot
from cfn_tools import load_yaml

def save_dot(dot_file):
    graphs = pydot.graph_from_dot_file(dot_file)
    graph = graphs[0]
    file_save_location = input('Where do you want the file to saved?')
    graph.write_png(file_save_location)


def get_cloudformationfile():
    input_file = input('Where is the cloudformation-template located?')
    with open(input_file, 'r') as stream:
        raw = stream.read()
        data_dict = load_yaml(raw)


def get_resources(input_dict):
    resource_list = {}
    section_id = 'Resources'
    for key in input_dict:
        if key == section_id:
            for sub_key in input_dict[section_id]:
                resource_list[sub_key] = input_dict[section_id].get(sub_key,{}).get('Type')
    return resource_list
    

# test_dict = get_resources(data_dict)
# print(test_dict)

save_dot(input('Where is the dotfile'))