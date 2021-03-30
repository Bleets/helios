from py2neo import *
import traceback
import sys

# -- This Script test the following element :
# 1   - Connect to the DB
# 2.1 - Create nodes and add to the DB
# 2.2 - Check if all nodes was created
# 3.1 - Create relation between nodes
# 3.2 - Check if the relationship was created

DB_HOSTNAME = "neo4j"
DB_PORT = "7474"
DB_USER = "neo4j"
DB_PWD = "test"


def main():
    # 1 - Connect to the DB
    print("[+] Test connect to the DB 'http://{}:{}'".format(DB_HOSTNAME, DB_PORT))
    try:
        DB = Graph("http://" + DB_HOSTNAME + ":" + DB_PORT, auth=("neo4j", "test"))
        DB.delete_all()
    except Exception:
        traceback.print_exc()
        print("[!] Can't connect to the DB 'http://{}:{}'".format(DB_HOSTNAME, DB_PORT))
        sys.exit(1)
    # 2.1 - Create nodes and add to the DB
    print("[+] Create nodes and add to the DB")
    try:
        tx = DB.begin()
        for name in ("Alice", "Bob", "Charlie"):
            node = Node("Person", name=name)
            tx.create(node)
        tx.commit()
    except Exception:
        traceback.print_exc()
        print("[!] Can't create nodes and added to the DB")
        sys.exit(1)
    # 2.2 - Check if all nodes was created
    print("[+] Check if all nodes was created")
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
        traceback.print_exc()
        print("[!] Can't get all nodes")
        sys.exit(1)
    # 3.1 - Create relation between nodes
    print("[+] Create relationship between nodes")
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
        traceback.print_exc()
        print("[!] Can't create relationship")
        sys.exit(1)
    # 3.2 - Check if the relationship was created
    print("[+] Check if all relations was created")
    try:
        relations = RelationshipMatcher(DB)
        result = relations.match(None, "KNOWS")
        if result.__len__() != 3:
            raise Exception()
    except Exception:
        traceback.print_exc()
        print("[!] Can't get all relations")
        sys.exit(1)


if __name__ == "__main__":
    main()
