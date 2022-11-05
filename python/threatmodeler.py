from data_structs import Threat, Mitigation, Resource
import json
import os

'''Generate threats by iterating over a list of resources'''
def generate_threats(resources: list, threatlist: list) -> list:
    # ...
    for resource in resources:
        pass

'''Generate mitigations by iterating over a list of resources'''
def generate_mitigations(resources: list, mitigations: list) -> list:
    # ...
    for resource in resources:
        pass

'''Parse threats into threat list as a CSV'''
def parse_threats_to_csv(threats: list) -> None:
    # ...
    pass

'''Parse mitigations and remediations to a CSV file'''
def parse_rem_mit_to_csv(remmit: list) -> None:
    # ...
    pass

'''Parse threats to a DOT-representation of ADTree'''
def parse_threats_to_ADTree(threats: list) -> None:
    # ...
    pass

'''Get all threats from the threat catalog'''
def get_threats_from_json(dir: str) -> list:
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
def get_all_threats_as_list(threats) -> list:
    return [threat.id for threat in threats]

def get_filenames_from_threatdir(dir: str) -> list:
    return [f'../threat-catalog/{filename}' for filename in os.listdir(dir)]

def get_filenames_from_remmitdir(dir: str) -> list:
    return [f'../remmit-catalog/{filename}' for filename in os.listdir(dir)]
        
'''Testing ground below'''

ls = get_filenames_from_threatdir('../threat-catalog')
threats = get_threats_from_json(ls)
for i in threats:
    print(i)
