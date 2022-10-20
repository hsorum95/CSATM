from ruamel.yaml import YAML
import sys

def get_cloudformationfile():
    input_file = input('Where is the cloudformation-template located?')
    with open(input_file, 'r') as stream:
        raw = stream.read()
        yaml = YAML(typ='rt')
        yaml.register_class(Ref)
        data_dict = yaml.load(raw)
    return data_dict

def get_resources(input_dict):
    resource_list = {}
    section_id = 'Resources'
    for key in input_dict:
        if key == section_id:
            for sub_key in input_dict[section_id]:
                resource_list[sub_key] = input_dict[section_id].get(sub_key,{}).get('Type')
    return resource_list

class Ref:
    yaml_tag = u'!Ref:'

    def __init__(self, value, style=None):
        self.value = value
        self.style = style

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(cls.yaml_tag,
                                            u'{.value}'.format(node), node.style)

    @classmethod
    def from_yaml(cls, constructor, node):
        return cls(node.value, node.style)

    def __iadd__(self, v):
        self.value += str(v)
        return self
