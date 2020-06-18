from py2neo import Graph, Node, Relationship

# g = Graph("localhost:7474", auth="neo4j/neo4j")
g = Graph("localhost:7474", auth=('neo4j', 'test'))


tx = g.begin()

liste = ["Alice", "Bob", "Caroline"]

for i in liste:
    print(i)
    a = Node("Person", name=i)
    tx.create(a)


# A faire
# - Savoir faire des relations
# - Savoir mettre des arguments sur les noeuds
# - Savoir mettre des arguments sur les relations
# - Savoir récupérer les informations
#   - Nombre de noeud
#   - Nombre de noeud par rapport aux attributs
#   - Qui est à ce type de relation
#   - Qui est à ce type de relation avec cette attribut


# EC2 (name=toto, tag.name="Vitrines", tag.bloc=lc)


# WARNING ! Commit que à la fin du code
tx.commit()
