from py2neo import Graph, Node, Relationship, NodeMatcher

# Connexion à la base de donnée
g = Graph("localhost:7474", auth=('neo4j', 'test'))
matcher = NodeMatcher(g)

# - Savoir récupérer les informations
person = matcher.match("Person")
list(person)

# alice = matcher.match("Person", name="Alice")
# list(alice)
