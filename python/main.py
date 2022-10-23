from cfnparser import *
from dfdgenerator import *

# /home/hsorum95/CSATM/cloudformation/three-tier-web-app.yml
yaml_dumped_to_dct: dict = get_cloudformationfile()
resources_in_list: list = get_resources(yaml_dumped_to_dct)
#print(resources_in_list)
dfd = create_dot_file(resources_in_list)
#print(dfd)