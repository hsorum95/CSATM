from cfnparser import *
from dfdgenerator import *
from threatmodeler import generate_threats, generate_mitigations, get_threats_from_json, get_remediations_from_json, parse_threats_to_ADTree

# /home/hsorum95/CSATM/cloudformation/three-tier-web-app.yml
# /home/hsorum95/CSATM/cloudformation/faas.yml
yaml_dumped_to_dct = get_cloudformationfile()
resources_in_list: list = get_resources(yaml_dumped_to_dct[0])
# for item in resources_in_list:
#     print(f'item name: {item.name}')
tb_resources = get_resources_in_trustboundry(resources_in_list)
create_resources_file(tb_resources)
dfd = create_dot_file(resources_in_list,yaml_dumped_to_dct[1])
tl = generate_threats(resources_in_list, get_threats_from_json('../threat-catalog'))
remedations = (generate_mitigations(tl, get_remediations_from_json('../remmit-catalog')))
#print(remedations)
parse_threats_to_ADTree( 'mitigations.json')
print("Dot-file and DFD-png created")