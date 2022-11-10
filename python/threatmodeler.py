from data_structs import Threat, Mitigation, Resource
import json
import yaml
import os

'''We have defined four "types" of threats. They are resource level threat, traffic level threats and application level threats
Resource level threats are threats that are inherent to the resource itself. For example, a database that is not encrypted
Traffic level threats are threats that are inherent to the traffic between resources. For example, a dataflow that is not encrypted
Application level threats are threats that are inherent to the application itself. For example, a web application that has a vulnerability in the code
External threats are threats that are inherent to the external environment due to that we do not have control over'''

def generate_threats(resources: list, threatlist: list) -> dict:
    '''Generate threats by iterating over a list of resources. Takes in a list of resource-objects
    and a list of threat objects. Returns a list of threat instances and saves a json in artifacs-dir'''
    threats_in_system = {} # dict representing the threatmodel of the system
   
    r_threats = get_resource_threats(threatlist)
    print(r_threats)
    t_threats = get_traffic_threats(threatlist)
    a_threats = get_application_threats(threatlist)
    e_threats = get_external_threats(threatlist)
    iaas = 'iaas'
    paas = 'paas'
    saas = 'saas'
    ext = 'external'
    for resource in resources:
        sm = get_resource_type_servicemodel(resource)
        if sm == iaas:
            generate_resource_threats(resource, r_threats, threats_in_system)
            generate_traffic_threats(resource, t_threats, threats_in_system)
            generate_application_threats(resource, a_threats, threats_in_system)
        elif sm == paas:
            generate_resource_threats(resource, r_threats, threats_in_system)
            generate_traffic_threats(resource, t_threats, threats_in_system)
            generate_application_threats(resource, a_threats, threats_in_system)
        elif sm == saas:  
            generate_resource_threats(resource, r_threats, threats_in_system)
        elif sm == ext:
            generate_external_threat(resource, e_threats, threats_in_system)
            generate_traffic_threats(resource, t_threats, threats_in_system)
        #Sm will be none when the resource is not in a trustboundry, and thus we disregard it
        elif sm is None:
            pass
        else:
            raise Exception('Unknown service model')
    with open('threatmodel.json', 'w+') as f:
        json.dump(threats_in_system, f, indent=4)
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


def generate_resource_threats(resource: Resource, threats: list, tm: dict) -> None:
    '''Generate threats on the resource level. Checks attributes of the resource and applies 
    threats that are relevant based on the attributes mapped against STRIDE'''
 

    def lstproc(lst:list,str: str) -> list:
        lst2 = list()
        for threat in lst:
                for t in threat.stride:
                    if t == str:
                        lst2.append(threat)
        return lst2
    info_disc = lstproc(threats, 'Information Disclosure')
    tamp = lstproc(threats, 'Tampering')
    denial = lstproc(threats, 'DoS')

    if resource.public:
        add_to_TM_dict(tm, resource, info_disc)
    if resource.data_processing:
        add_to_TM_dict(tm, resource, tamp)
        add_to_TM_dict(tm, resource, denial)
    if resource.data_store:
        add_to_TM_dict(tm, resource,tamp)
    

def generate_traffic_threats(resource: Resource, threats: list, tm: dict) -> None:
        dfs = resource.data_flows
        if len(dfs) > 0:    
            for df in dfs: 
                if df.encrypted == False and df.data_sensitivity == 'Crosses Trust Boundary':
                    add_to_TM_dict(tm, resource, threats)
    

def generate_application_threats(resource: Resource, threats: list, tm: dict) -> None:
    if resource.data_store == False:
        add_to_TM_dict(tm, resource, threats)


def generate_external_threat(resource: Resource, threats: list, tm: dict) -> None:
    add_to_TM_dict(tm, resource, threats)

def check_dataprocessing(resource: Resource) -> bool:
    return resource.data_processing

def check_datastoreage(resource: Resource) -> bool:
    return resource.data_store

def check_public(resource: Resource) -> bool:
    return resource.public

def get_resource_threats(threatlist: list) -> list:
    return [threat for threat in threatlist if threat.type == 'Resource']

def get_traffic_threats(threatlist: list) -> list:
    return [threat for threat in threatlist if threat.type == 'Traffic']

def get_application_threats(threatlist: list) -> list:
    return [threat for threat in threatlist if threat.type == 'Application']

def get_external_threats(threatlist: list) -> list:
    return [threat for threat in threatlist if threat.type == 'External']

def get_other_threats(threatlist: list) -> list:
    return [threat for threat in threatlist if threat.type == 'Other']

def add_to_TM_dict(tm_dict: dict, resource: Resource, threatlist: list) -> None:
    '''Add a threat to the dict containing the threatmodel for the system being modeled
    input: tm_dict: dict, resource: Resource, threat_instance: Threat_Instance'''
    for threat in threatlist:
        if resource.name not in tm_dict:
            tm_dict[resource.name] = [(f'{threat.id}, {threat.name}')]
        elif resource.name in tm_dict:
            tm_dict[resource.name].append((f'{threat.id}, {threat.name}'))

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
