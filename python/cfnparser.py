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
    data_flows: list()

@dataclass
class DataFlow:
    source: Resource
    destination: Resource
    data_sensitivity: str

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
    resource_list = []
    section_id = 'Resources'
    for key in input_dict:
        if key == section_id:
            for sub_key in input_dict[section_id]:
                tmp_resource = Resource(sub_key,input_dict[section_id].get(sub_key,{}).get('Type'), 'None', [])
                for sub_sub_key in input_dict[key][sub_key]:
                    if sub_sub_key == 'Properties':
                        for sub_sub_sub_key in input_dict[key][sub_key][sub_sub_key]:
                            if (sub_sub_sub_key == 'Tags') and input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key][0].get('Key') == 'trust-boundary':
                                tmp_resource.trust_boundry = input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key][0].get('Value')
                            if (sub_sub_sub_key == 'Tags') and len(input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key]) > 1:
                                itr = len(input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key])
                                if input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key][1].get('Key') == 'data_flow':
                                    df = DataFlow(tmp_resource.name, input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key][1].get('Value'), 'None')
                                    tmp_resource.data_flows.append(df)
                                if input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key][1].get('Key') == 'data_flow_source':
                                    df = DataFlow(input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key][1].get('Value'), tmp_resource.name, 'None')
                                    tmp_resource.data_flows.append(df)
                resource_list.append(tmp_resource)
    return resource_list


def get_trustboundry(input_dict: dict ) -> str:
    for key in input_dict:
        if key == 'Resources':
            for sub_key in input_dict[key]:
                for sub_sub_key in input_dict[key][sub_key]:
                    if sub_sub_key == 'Properties':
                        for sub_sub_sub_key in input_dict[key][sub_key][sub_sub_key]:
                            if (sub_sub_sub_key == 'Tags') and input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key][0].get('Key') == 'trust-boundary':
                                return input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key][0].get('Value')

def get_all_keys(input_dict: dict) -> list:
    test = input_dict.keys()
    key_list = list(test)
    return key_list 
##TODO: create dataflow objects and add them to the resource objects