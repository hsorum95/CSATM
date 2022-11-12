from data_structs import Threat, Mitigation, Resource
import json
import yaml
import os
import pydot

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
def generate_mitigations(threatmodel: dict, mitigations: list) -> list:
    '''takes in a threatmodel as a dict and creates a list of the applicable remediations according to CSAM'''
    mitigations_in_system = {}
    for resource in threatmodel:
        for threat in threatmodel[resource]:
            for mit in mitigations:
                if int(threat[0]) in mit.related_to:
                   add_to_mit_dict(threat, mitigations_in_system, resource, [mit])

    with open('mitigations.json', 'w+') as f:
        json.dump(mitigations_in_system, f, indent=4)
    return mitigations_in_system


'''Parse threats to a DOT-representation of ADTree'''
def parse_threats_to_ADTree(mit_filename: str) -> None:
    '''Parse threats to a DOT-representation of ADTree'''
    with open(mit_filename) as f:
        mitigations = json.load(f)
        for resource in mitigations:
            for threat in mitigations[resource]:
                create_ad_tree(resource,threat)    

    # with open(mit_filename) as f:
    #     mitigations = json.load(f)
    #     print(mitigations)



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


def create_ad_tree(resource_name: str,threat_name: str) -> None:
    lst = threat_name.split(',')
    
    threat = lst[1]
    threat_id = lst[0]
    mit = lst[2]

    if int(threat_id) == 10:
        dot = pydot.Dot(graph_type='digraph', rankdir = 'TB')
        dot.obj_dict['attributes']['label'] = f'ADTree for resource: {resource_name} and threat: {threat}'
        
        dot.obj_dict['attributes']['labelloc'] = 't'
        #Create first node which is what the attacker wants to do
        root = pydot.Node(f'Attacker Goal {threat}', shape='box')
        dot.add_node(root)
        #2 lvl
        attack = pydot.Node(f'Spoofing identity of legit user', shape='box')
        dot.add_node(attack)
        dot.add_edge(pydot.Edge(root,attack))
        attack2 = pydot.Node(f'Elevating priveleges of lowlevel user', shape='box')
        dot.add_node(attack2)
        dot.add_edge(pydot.Edge(root,attack2))
        dot.write_png(f'artifacts/atd/{threat.replace("/","_")}_{resource_name}_atd.png')
    elif int(threat_id) == 9:
        
        dot = pydot.Dot(graph_type='digraph', rankdir = 'TB')
        dot.obj_dict['attributes']['label'] = f'ADTree for resource: {resource_name} and threat: {threat}'
        dot.obj_dict['attributes']['labelloc'] = 't'
        #Create first node which is what the attacker wants to do
        root = pydot.Node(f'{threat}', shape='box')
        dot.add_node(root)
        # 2 lvl
        attack = pydot.Node(f'No IP allowlisting', shape='box')
        dot.add_node(attack)
        dot.add_edge(pydot.Edge(root,attack))
        attack2 = pydot.Node('Container overtake', shape='box')
        dot.add_node(attack2)
        dot.add_edge(pydot.Edge(root,attack2))
        attack3 = pydot.Node('Misunderstood SRM', shape='box')
        dot.add_node(attack3)
        dot.add_edge(pydot.Edge(root,attack3))
        #3 lvl 
        attack4 = pydot.Node('No network isolation', shape='box')
        dot.add_node(attack4)
        dot.add_edge(pydot.Edge(attack,attack4))
        attack5 = pydot.Node('Vulnerable container image', shape='box')
        dot.add_node(attack5)
        dot.add_edge(pydot.Edge(attack2,attack5))
        attack6 = pydot.Node('Container running as root', shape='box')
        dot.add_node(attack6)
        dot.add_edge(pydot.Edge(attack2,attack6))
        attack7 = pydot.Node('Vulnerable Runtime', shape='box')
        dot.add_node(attack7)
        dot.add_edge(pydot.Edge(attack3,attack7))
        attack8 = pydot.Node('Overpriveleged role for resource', shape='box')
        dot.add_node(attack8)
        dot.add_edge(pydot.Edge(attack3,attack8))
        
        dot.write_png(f'artifacts/atd/{threat.replace("/","_")}_{resource_name}_atd.png')
    elif int(threat_id) == 8:
        dot = pydot.Dot(graph_type='digraph', rankdir = 'TB')
        dot.obj_dict['attributes']['label'] = f'ADTree for resource: {resource_name} and threat: {threat}'
        dot.obj_dict['attributes']['labelloc'] = 't'
        #Create first node which is what the attacker wants to do
        root = pydot.Node(f'{threat}', shape='box')
        dot.add_node(root)
         #2 lvl
        attack = pydot.Node(f'Spoofing identity of legit user', shape='box')
        dot.add_node(attack)
        dot.add_edge(pydot.Edge(root,attack))
        attack2 = pydot.Node(f'Elevating priveleges of lowlevel user', shape='box')
        dot.add_node(attack2)
        dot.add_edge(pydot.Edge(root,attack2))
        #3 lvl
        attack3 = pydot.Node(f'Brute force password', shape='box')
        dot.add_node(attack3)
        dot.add_edge(pydot.Edge(attack,attack3))
        attack4 = pydot.Node(f'Phishing', shape='box')
        dot.add_node(attack4)
        dot.add_edge(pydot.Edge(attack,attack4))
        attack5 = pydot.Node(f'Bypass access control', shape='box')
        dot.add_node(attack5)
        dot.add_edge(pydot.Edge(attack2,attack5))
        dot.write_png(f'artifacts/atd/{threat.replace("/","_")}_{resource_name}_atd.png')
    else:
        return

    


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
    info_disc = lstproc(threats, 'Information_Disclosure')
    tamp = lstproc(threats, 'Tampering')
    denial = lstproc(threats, 'DoS')

    if resource.public:
        add_to_TM_dict(tm, resource, info_disc)
    if resource.data_processing:
        if resource.public == False:
           add_to_TM_dict(tm, resource, info_disc)
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
    if resource.data_store == False and resource.data_processing == True:
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
    input: tm_dict: dict, resource: Resource, threatlist: list'''
    for threat in threatlist:
        if resource.name not in tm_dict:
            tm_dict[resource.name] = [(f'{threat.id}, {threat.name}')]
        elif resource.name in tm_dict:
            if (f'{threat.id}, {threat.name}') in tm_dict[resource.name]:
                pass
            else:
                tm_dict[resource.name].append((f'{threat.id}, {threat.name}'))


def add_to_mit_dict(threat, mit_dict: dict, resource: str, mitigations: list):
    '''Add a mitigation to the dict containing the mitigations for the system being modeled
    input: mit_dict: dict, resource: str, mitigations, list'''
    for mitigation in mitigations:
        if resource not in mit_dict:
                mit_dict[resource] = [(f'{threat}, Mitigation id: {mitigation.id} & Mitigation: {mitigation.name}')]
        elif resource in mit_dict:
            if (f'{threat}, Mitigation id: {mitigation.id} & Mitigation: {mitigation.name}') in mit_dict[resource]:
                pass
            else:
                mit_dict[resource].append((f'{threat}, Mitigation id: {mitigation.id} & Mitigation: {mitigation.name}'))

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
