import pydot

input_file = input('Where is the cloudformation-template located?')

graphs = pydot.graph_from_dot_file(input_file)

graph = graphs[0]

file_save_location = input('Where do you want the file to saved?')
graph.write_png(file_save_location)