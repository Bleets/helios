from py2neo import Graph, Node, Relationship

graph = Graph()

hello_world = Node("Message", content="Hello world !")
graph.merge()
