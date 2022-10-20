import sys
import ruamel.yaml
from dataclasses import dataclass


class Generic:
    def __init__(self, tag, value, style=None):
        self._value = value
        self._tag = tag
        self._style = style


class GenericScalar(Generic):
    @classmethod
    def to_yaml(self, representer, node):
        return representer.represent_scalar(node._tag, node._value)

    @staticmethod
    def construct(constructor, node):
        return constructor.construct_scalar(node)


class GenericMapping(Generic):
    @classmethod
    def to_yaml(self, representer, node):
        return representer.represent_mapping(node._tag, node._value)

    @staticmethod
    def construct(constructor, node):
        return constructor.construct_mapping(node, deep=True)


class GenericSequence(Generic):
    @classmethod
    def to_yaml(self, representer, node):
        return representer.represent_sequence(node._tag, node._value)

    @staticmethod
    def construct(constructor, node):
        return constructor.construct_sequence(node, deep=True)


def default_constructor(constructor, tag_suffix, node):
    generic = {
        ruamel.yaml.ScalarNode: GenericScalar,
        ruamel.yaml.MappingNode: GenericMapping,
        ruamel.yaml.SequenceNode: GenericSequence,
    }.get(type(node))
    if generic is None:
        raise NotImplementedError('Node: ' + str(type(node)))
    style = getattr(node, 'style', None)
    instance = generic.__new__(generic)
    yield instance
    state = generic.construct(constructor, node)
    instance.__init__(tag_suffix, state, style=style)

@dataclass
class Resource:
    name: str
    type: str
    trust_boundry: str


ruamel.yaml.add_multi_constructor('', default_constructor, Loader=ruamel.yaml.SafeLoader)
yaml = ruamel.yaml.YAML(typ='safe', pure=True)
yaml.default_flow_style = False
yaml.register_class(GenericScalar)
yaml.register_class(GenericMapping)
yaml.register_class(GenericSequence)

def get_cloudformationfile():
    input_file = input('Where is the cloudformation-template located?')
    with open(input_file, 'r') as stream:
        raw = stream.read()
    base = yaml.load(raw)
    return base


def get_resources(input_dict: dict ) -> list:
    resource_dict = []
    section_id = 'Resources'
    for key in input_dict:
        if key == section_id:
            for sub_key in input_dict[section_id]:
                tmp = Resource(sub_key,input_dict[section_id].get(sub_key,{}).get('Type'), "cloudnetwork")
                resource_dict.append(tmp)
    return resource_dict

yaml_dumped_to_dct: dict = get_cloudformationfile()

recources_in_list: list = get_resources(yaml_dumped_to_dct)

for item in recources_in_list:
    print(item.name)
    print(item.type)
    print(item.trust_boundry)

# lst = base['Resources']['PharmacyVPC']['Properties']['Tags']
# dict = lst[0]
# key = dict.get('Key')
# value = dict.get('Value')
# tuple = (key, value)
#print(tuple)
#print((base['Resources']['PharmacyVPC']['Properties']['Tags']))