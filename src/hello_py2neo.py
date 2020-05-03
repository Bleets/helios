from py2neo import Graph, Node, Relationship, NodeMatcher
import boto3

print("test")
# Connexion à la base de donnée
g = Graph("localhost:7474", auth=("neo4j", "test"))

# Commencer la transaction
tx = g.begin()

# - Savoir faire des noeuds
# liste = ["Alice", "Bob", "Caroline"]
# for i in liste:
#     print(i)
#     n = Node("Person", name=i)
#     tx.create(n)


liste = ["alice.com", "bob.com", "caroline.com"]
liste_type = ["CNAME", "A", "AAAA"]
for i, t in zip(liste, liste_type):
    print(i)
    n = Node("Route53", name=i, type=t)
    tx.create(n)

liste = ["urhizuer.cloudfront.net", "rzegsvr.cloudfront.net", "azefaz.cloudfront.net"]
for i in liste:
    print(i)
    n = Node("CloudFront", name=i)
    tx.create(n)

# print nombre de nodes
print(len(g.nodes))
# print nombre de relations
print(len(g.relationships)

a = Node("Person", name="Alice", age=33)
b = Node("Person", name="Bob", age=44)
c = Node("Person", name="Patrick", age=33)
ab = Relationship(a, "KNOWS", b)

# créé une relationship
FRIENDS = Relationship.type("FRIENDS")
g.merge(FRIENDS(a, c), "Person", "name")


# push les creations
tx.create(a)
tx.create(b)
tx.create(c)
tx.create(ab)

# test exist retourne true
tx.exists(ab)

# trouver un node en particulier
matcher = NodeMatcher(g)
print(matcher.match("Person", name="Alice").first())

# nombre de Person ayant age = 33
print(len(matcher.match("Person", age=33)))

# lister max 3 personnes personnes dont le nom commence par c
print(
    list(matcher.match("Person").where("_.name =~ 'A.*'").order_by("_.name").limit(3))
)

# - Savoir faire des relations

# - Savoir mettre des arguments sur les noeuds
# - Savoir mettre des arguments sur les relations

#   - Nombre de noeud
#   - Nombre de noeud par rapport aux attributs
#   - Qui est à ce type de relation
#   - Qui est à ce type de relation avec cette attribut

# BONUS = cartographier nmap. Créer les noeuds des IPs avece relations port ouvert
# (192.168.1.87)-[:Ouvert]>(7474)
# (192.168.1.87)-[:Fermer]>(22)

# EC2 (name=toto, tag.name="Vitrines", tag.bloc=lc)


# WARNING ! Commit que à la fin du code
tx.commit()
