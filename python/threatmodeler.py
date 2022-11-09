from data_structs import Threat, Mitigation, Resource, Threat_Instance
import json
import yaml
import os


def generate_threats(resources: list, threatlist: list) -> dict:
    '''Generate threats by iterating over a list of resources. Takes in a list of resource-objects
    and a list of threat objects. Returns a list of threat instances and saves a json in artifacs-dir'''
    threats_in_system = {}
    iaas = 'iaas'
    paas = 'paas'
    saas = 'saas'
    ext = 'external'
    for resource in resources:
        sm = get_resource_type_servicemodel(resource)
        if sm == iaas:
            add_to_TM_dict(threats_in_system,resource,Threat_Instance(threatlist[0], None))
            add_to_TM_dict(threats_in_system,resource,Threat_Instance(threatlist[1], None))
            
        elif sm == paas:
            add_to_TM_dict(threats_in_system,resource,Threat_Instance(threatlist[1], None))
            add_to_TM_dict(threats_in_system,resource,Threat_Instance(threatlist[2], None))
        elif sm == saas:  
            add_to_TM_dict(threats_in_system,resource,Threat_Instance(threatlist[3], None))
        elif sm == ext:
            add_to_TM_dict(threats_in_system,resource,Threat_Instance(threatlist[4], None))
        #Sm will be none when the resource is not in a trustboundry, and thus we disregard it
        elif sm is None:
            pass
        else:
            raise Exception('Unknown service model')
    with open('threatmodel.json', 'w+') as f:
        json.dump(threats_in_system, f)
    return threats_in_system

'''Generate mitigations by iterating over a list of threats'''
def generate_mitigations(resources: list, mitigations: list) -> list:
    # ...
    for resource in resources:
        pass


'''Parse threats to a DOT-representation of ADTree'''
def parse_threats_to_ADTree(threats: list) -> None:
    # ...
    pass


def get_threats_from_json(dir: str) -> list:
    '''Get all threats from the threat catalog'''
    threat_list = []
    filenames = get_filenames_from_threatdir(dir)
    for fn in filenames:
        with open (fn) as f:
            threat = json.load(f, object_hook=lambda d: Threat(**d))
            threat_list.append(threat)
    return threat_list

'''Get all remediations & mitigations from the remmit catalog'''
def get_remediations_from_json(dir: str) -> list:
    rem_list = []
    filenames = get_filenames_from_remmitdir(dir)
    for fn in filenames:
        with open (fn) as f:
            rem = json.load(f, object_hook=lambda d: Mitigation(**d))
            rem_list.append(rem)
    return rem_list

'''Helpers'''

def add_to_TM_dict(tm_dict: dict, resource: Resource, threat_instance: Threat_Instance) -> None:
    '''Add a threat instance to the dict containing the threatmodel for the system being modeled
    input: tm_dict: dict, resource: Resource, threat_instance: Threat_Instance'''
    if resource.name not in tm_dict:
        tm_dict[resource.name] = [(f'{threat_instance.threat.id}, {threat_instance.threat.name}')]
    elif resource.name in tm_dict:
        tm_dict[resource.name].append((f'{threat_instance.threat.id}, {threat_instance.threat.name}'))

def get_filenames_from_threatdir(dir: str) -> list:
    return [f'{dir}/{filename}' for filename in os.listdir(dir)]

def get_filenames_from_remmitdir(dir: str) -> list:
    return [f'{dir}/{filename}' for filename in os.listdir(dir)]

'''return the servicemodel as a string'''
def get_resource_type_servicemodel(resource: Resource) -> str:
    service_model_dict = get_resource_types_from_file()
    for r in service_model_dict:
        if resource.type  in service_model_dict[r]:
            return r


'''dump servicemodels into a dict in memory'''
def get_resource_types_from_file() -> list:
    with open('taxonomy.yml') as t:
        taxonomy = yaml.load(t, Loader=yaml.FullLoader)
    return taxonomy

'''Testing ground below'''

#print(get_resource_type_servicemodel(Resource('test', 'AWS::RDS::DBInstance','myTB', [], True, True, True)))

# threats = get_threats_from_json('../threat-catalog')
# for i in threats:
#     print(i)

# threats = get_remediations_from_json('../remmit-catalog')
# for i in threats:
#     print(i)
