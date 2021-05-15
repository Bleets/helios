from py2neo import *
import traceback, sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from libs.colors import colors
from libs.settings import neo4j_database

# -- This Script test the following element :
# 1   - Connect to the DB
# 2.1 - Create nodes and add to the DB
# 2.2 - Check if all nodes was created
# 3.1 - Create relation between nodes
# 3.2 - Check if the relationship was created

def main():
    # 1 - Connect to the DB
    print(colors.INFO,"[i] Try to connect on the DB '{}:{}'".format(neo4j_database.HOSTNAME, neo4j_database.PORT))
    try:
        DB = Graph(neo4j_database.HOSTNAME + ":" + neo4j_database.PORT, auth=(neo4j_database.USER, neo4j_database.PWD))
        DB.delete_all()
    except Exception:
        print(colors.reset)
        traceback.print_exc()
        print(colors.ERROR,"[!] Can't connect to the DB 'http://{}:{}'".format(neo4j_database.HOSTNAME, neo4j_database.PORT))
        sys.exit(1)
    print(colors.OK,"[+] Can connecte to the DB '{}:{}'".format(neo4j_database.HOSTNAME, neo4j_database.PORT))
    # 2.1 - Create nodes and add to the DB
    print(colors.INFO,"[i] Create nodes and add to the DB")
    try:
        tx = DB.begin()
        for name in ("Alice", "Bob", "Charlie"):
            node = Node("Person", name=name)
            tx.create(node)
        tx.commit()
    except Exception:
        print(colors.reset)
        traceback.print_exc()
        print(colors.ERROR,"[!] Can't create nodes and added to the DB")
        sys.exit(1)
    print(colors.OK,"[+] Can create nodes on the DB")
    # 2.2 - Check if all nodes was created
    print(colors.INFO,"[i] Check if all nodes was created")
    try:
        nodes = NodeMatcher(DB)
        tab_of_nodes = []
        count = 0
        for name in ("Alice", "Bob", "Charlie"):
            result = dict(nodes.match("Person", name=name).first())
            if result["name"] == name:
                count += 1
                tab_of_nodes.append(nodes.match("Person", name=name).first())
        if count != 3:
            raise Exception()
    except Exception:
        print(colors.reset)
        traceback.print_exc()
        print(colors.ERROR,"[!] Can't get all nodes")
        sys.exit(1)
    print(colors.OK,"[+] All nodes was created")
    # 3.1 - Create relation between nodes
    print(colors.INFO,"[i] Try to create relationship between nodes")
    try:
        tx = DB.begin()
        for i in range(len(tab_of_nodes)):
            if i == 2:
                knows = Relationship(tab_of_nodes[0], "KNOWS", tab_of_nodes[i])
            else:
                knows = Relationship(tab_of_nodes[i], "KNOWS", tab_of_nodes[i + 1])
            tx.create(knows)
        tx.commit()
    except Exception:
        print(colors.reset)
        traceback.print_exc()
        print(colors.ERROR,"[!] Can't create relationship")
        sys.exit(1)
    print(colors.OK,"[+] Can create relations between nodes")
    # 3.2 - Check if the relationship was created
    print(colors.INFO,"[i] Check if all relations was created")
    try:
        relations = RelationshipMatcher(DB)
        result = relations.match(None, "KNOWS")
        if result.__len__() != 3:
            raise Exception()
    except Exception:
        print(colors.reset)
        traceback.print_exc()
        print(colors.ERROR,"[!] Can't get all relations")
        sys.exit(1)
    print(colors.OK,"[+] All relations was created")


if __name__ == "__main__":
    main()
