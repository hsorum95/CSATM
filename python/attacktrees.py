import pydot

def save_dot(dot_file):
    graphs = pydot.graph_from_dot_file(dot_file)
    graph = graphs[0]
    file_save_location = input('Where do you want the file to saved?')
    graph.write_png(file_save_location)
