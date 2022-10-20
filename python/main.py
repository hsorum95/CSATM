from cfnparser import *
import attacktrees

# /home/hsorum95/CSATM/cloudformation/three-tier-web-app.yml
ordered_dict = get_cloudformationfile()
output = get_resources(ordered_dict)
print(ordered_dict)