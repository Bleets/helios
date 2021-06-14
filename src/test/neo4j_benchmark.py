import traceback, sys, os
from py2neo import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from libs.colors import colors
from libs.settings import Neo4j as N
    
def main():
    # Cleanup all mess
    try:
        DB = N.DB.connect()
        DB.delete_all()
    except Exception:
        print(colors.reset)
        traceback.print_exc()
        print(colors.ERROR,"[!] Can't connect to the DB '{}:{}'".format(N.HOSTNAME, N.DB.PORT))
        sys.exit(1)
    print(colors.OK,"[+] Can connect to the DB '{}:{}'".format(N.HOSTNAME, N.DB.PORT))

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
        for i in range(NB_NODE):
            node = Node("Node", name=i)
            nino = Relationship(node, "NINO", elpadre)
            tx.create(nino)
        DB.commit(tx)
    except Exception:
        print(colors.reset)
        traceback.print_exc()
        print(colors.ERROR,"[!] Can't create all nodes ")
        sys.exit(1)
    print(colors.OK,"[+] '{}' nodes are created".format(NB_NODE))

if __name__ == "__main__":
    global NB_NODE
    print(sys.argv)
    if len(sys.argv) == 2:
        NB_NODE = int(sys.argv[1])
    else:
        NB_NODE = 300
    main()