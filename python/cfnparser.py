import ruamel.yaml
from data_structs import Resource, DataFlow
import uuid

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
    return [base, input_file]


def get_resources(input_dict: dict ) -> list:
    resource_list = []
    keyw = 'Key'
    valuew = 'Value'
    section_id = 'Resources'
    props_keyword = 'Properties'
    tags_keyword = 'Tags'
    tb_keyword = 'trust-boundary'
    df_keyword = 'data_flow'
    sink_keyword = 'data_flow_sink'
    source_keyword = 'data_flow_source'
    public_kw = 'public'
    dp_kw = 'data_processing'
    datastore_kw = 'datastore'
    
    if check_keyword(input_dict, section_id):
        resources_dict = input_dict[section_id]
        for key in resources_dict:
            tmp_resource = Resource(key,input_dict[section_id].get(key,{}).get('Type'), 'None', [], False, False, False)
            resource_dict = resources_dict[key]
            if check_keyword(resource_dict[props_keyword], tags_keyword):
                tags_list = resource_dict[props_keyword][tags_keyword]
                for tag in tags_list:
                    if tag.get(keyw) == tb_keyword:
                        tmp_resource.trust_boundry = tag.get(valuew)
                    if tag.get(keyw) == df_keyword:
                        df = DataFlow(tmp_resource.name, tag.get(valuew), 'None')
                        tmp_resource.data_flows.append(df)
                    if tag.get(keyw) == sink_keyword:
                        df = DataFlow(tmp_resource.name, tag.get(valuew), 'None')
                        tmp_resource.data_flows.append(df)
                    if tag.get(keyw) == source_keyword:
                        df = DataFlow(tag.get(valuew), tmp_resource.name,  'None')
                        tmp_resource.data_flows.append(df)
                    if tag.get(keyw) == public_kw:
                        tmp_resource.public = toBool(tag.get(valuew))
                    if tag.get(keyw) == dp_kw:
                        tmp_resource.data_processing = toBool(tag.get(valuew))
                    if tag.get(keyw) == datastore_kw:
                        tmp_resource.data_store = toBool(tag.get(valuew))
            resource_list.append(tmp_resource)
    #add resources that are not in the CFN but in the DFs in the tags to the list

    if resource_list:        
        for item in resource_list:
            if item.data_flows:
                for i in range(0,len(item.data_flows)):
                    if item.data_flows[i].source not in get_all_resource_names(resource_list):
                        ext_Resource = Resource(item.data_flows[i].source, 'External', 'External',[DataFlow( item.data_flows[i].source, item.name, 'None')], False, False, False)
                        resource_list.append(ext_Resource)
                        
                    elif item.data_flows[i].destination not in get_all_resource_names(resource_list):
                        ext_Resource = Resource(item.data_flows[i].destination, 'External', 'External',[DataFlow(item.name, item.data_flows[i].destination,  'None')], True, False, False)
                        resource_list.append(ext_Resource)
                        

    if resource_list:
        for item in resource_list:
            set_data_sensitivity(item, resource_list)
    return resource_list

#helper for get_resources
def get_all_resource_names(list: list) -> list:
    return [resource.name for resource in list]


#Sets data sensitivity based on wether the source and destination are in the same trust boundary
def set_data_sensitivity(resource_from: Resource, resource_list: list) -> None:
    if resource_from.data_flows:
        for df in resource_from.data_flows:
            if (get_resource_by_name(df.destination, resource_list).trust_boundry != resource_from.trust_boundry) or (get_resource_by_name(df.source, resource_list).trust_boundry != resource_from.trust_boundry):
                df.data_sensitivity = 'Crosses Trust Boundary'
            elif get_resource_by_name(df.destination, resource_list).trust_boundry == resource_from.trust_boundry or (get_resource_by_name(df.source, resource_list).trust_boundry == resource_from.trust_boundry): 
                df.data_sensitivity = 'In Trust Boundary'
    return None
    
def get_resource_by_name(name: str, resource_list: list) -> Resource:
    for resource in resource_list:
        if resource.name == name:
            return resource
    return None

#Input list of resource objects. Output list of resource objects within trustboundaries
def get_resources_in_trustboundry(resource_list: list) -> list:
    return [resource for resource in resource_list if resource.trust_boundry != 'None']    

#Input list of resource objects. Create and format txt.file
def create_resources_file(input: list) -> None:
    id = uuid.uuid4()
    with open(f'artifacts/{id}_resources.txt', 'w+') as file:
        for resource in input:
            file.write(f'Name: {resource.name}\n\tResource-type: {resource.type}\n\tResource-TrustBoundary: {resource.trust_boundry}\n\tResource exposed public: {resource.public}\n\tResource process data: {resource.data_processing}\n\tResource is a datastore: {resource.data_store}\n\tDataFlows:\n')
            if len(resource.data_flows) > 0:
                for dataflow in resource.data_flows:
                    file.write(f'\t-   Source: {dataflow.source}\n\t\tDestination: {dataflow.destination}\n\t\tDataSensitivity: {dataflow.data_sensitivity}\n')
            else: 
                file.write('\t-   None\n')
            

#Helper to find if a keyword is used as key in a getKeys on a dict
def check_keyword(input_dict: dict, keyword: str) -> bool:
    if keyword in get_all_keys(input_dict):
      return True
    elif keyword not in get_all_keys(input_dict):
        return False
    else:
        raise Exception('No resources found with the keyword: ' + keyword)

def get_all_keys(input_dict: dict) -> list:
    test = input_dict.keys()
    key_list = list(test)
    return key_list 

def toBool(str: str):
    if(str == 'True'):
        return True
    elif(str == 'False'):
        return False

# def get_trustboundry(input_dict: dict ) -> str:
#     for key in input_dict:
#         if key == 'Resources':
#             for sub_key in input_dict[key]:
#                 for sub_sub_key in input_dict[key][sub_key]:
#                     if sub_sub_key == 'Properties':
#                         for sub_sub_sub_key in input_dict[key][sub_key][sub_sub_key]:
#                             if (sub_sub_sub_key == 'Tags') and input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key][0].get('Key') == 'trust-boundary':
#                                 return input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key][0].get('Value')

                    
    # for key in input_dict:
    #     if key == section_id:
    #         for sub_key in input_dict[section_id]:
    #             tmp_resource = Resource(sub_key,input_dict[section_id].get(sub_key,{}).get('Type'), 'None', [])
    #             for sub_sub_key in input_dict[key][sub_key]:
    #                 if sub_sub_key == 'Properties':
    #                     for sub_sub_sub_key in input_dict[key][sub_key][sub_sub_key]:
    #                         if (sub_sub_sub_key == 'Tags') and input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key][0].get('Key') == 'trust-boundary':
    #                             tmp_resource.trust_boundry = input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key][0].get('Value')
    #                         if (sub_sub_sub_key == 'Tags') and len(input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key]) > 1:
    #                             itr = len(input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key])
    #                             if input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key][1].get('Key') == 'data_flow':
    #                                 df = DataFlow(tmp_resource.name, input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key][1].get('Value'), 'None')
    #                                 tmp_resource.data_flows.append(df)
    #                             if input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key][1].get('Key') == 'data_flow_source':
    #                                 df = DataFlow(input_dict[key][sub_key][sub_sub_key][sub_sub_sub_key][1].get('Value'), tmp_resource.name, 'None')
    #                                 tmp_resource.data_flows.append(df)
    #             resource_list.append(tmp_resource)