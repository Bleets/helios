import traceback, sys, os
from py2neo import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from libs.colors import colors
from libs.settings import neo4j_database

# Cleanup all mess
try:
    DB = Graph(neo4j_database.HOSTNAME + ":" + neo4j_database.PORT, auth=(neo4j_database.USER, neo4j_database.PWD))
    DB.delete_all()
except Exception:
    print(colors.reset)
    traceback.print_exc()
    print(colors.ERROR,"[!] Can't connect to the DB 'http://{}:{}'".format(neo4j_database.HOSTNAME, neo4j_database.PORT))
    sys.exit(1)

tx = DB.begin()
try:
    elpadre = Node("Person", name="El padre")
    tx.create(elpadre)
except Exception:
    print(colors.reset)
    traceback.print_exc()
    print(colors.ERROR,"[!] Can't create node 'El Padre'")
    sys.exit(1)
print(colors.OK,"[+] 'El Padre' is create")

try:
    for i in range(350):
        node = Node("Node", name=i)
        nino = Relationship(node, "NINO", elpadre)
        tx.create(nino)
    tx.commit()
except Exception:
    print(colors.reset)
    traceback.print_exc()
    print(colors.ERROR,"[!] Can't create all nodes ")
    sys.exit(1)
print(colors.OK,"[+] All nodes are created")

