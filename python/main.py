from cfnparser import *
from dfdgenerator import *

# /home/hsorum95/CSATM/cloudformation/three-tier-web-app.yml
yaml_dumped_to_dct = get_cloudformationfile()
resources_in_list: list = get_resources(yaml_dumped_to_dct[0])
tb_resources = get_resources_in_trustboundry(resources_in_list)
create_resources_file(tb_resources)
dfd = create_dot_file(resources_in_list,yaml_dumped_to_dct[1])
print("Dot-file and DFD-png created")