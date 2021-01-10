
from py2neo import Graph

# Connect to the DB
g = Graph("host.docker.internal:7474", auth=('neo4j', 'test'))

# Erase all the DB
g.delete_all()
