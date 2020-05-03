
from py2neo import Graph

# Connect to the DB
g = Graph("localhost:7474", auth=('neo4j', 'test'))

# Erase all the DB
g.delete_all()
