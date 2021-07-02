from boto3 import NullHandler
from py2neo import Graph,Node
from py2neo.data import Relationship
from py2neo.errors import Neo4jError
from py2neo.matching import NodeMatcher

from libs.aws_services import AWS

from .colors import colors

# - DEBUG
import json

class Neo4j:
    HOSTNAME = "http://localhost"

    def find_node(data,type_of_node, name_of_node):
      matcher = NodeMatcher(data)
      return matcher.match(type_of_node, name=name_of_node).first()

    class DB:
        PORT = "7474"

        def connect():
            return Graph(Neo4j.HOSTNAME+":"+Neo4j.DB.PORT)
    class AWS:
      class Route53:
        def create_all_ressources(data_route53:list):
          responce = 1
          if len(data_route53["Route53"]["HostedZones"]):
            responce = 0
            neo4j_db = Neo4j.DB.connect()
            neo4j_transaction = neo4j_db.begin()

            nodes_of_hosted_zone = Neo4j.AWS.Route53.create_hosted_zone(neo4j_transaction,data_route53["Route53"]["HostedZones"])
            for hosted_zone, node in zip(data_route53["Route53"]["HostedZones"],nodes_of_hosted_zone):
              Neo4j.AWS.Route53.create_record_sets(neo4j_transaction,node,hosted_zone["ResourceRecordSets"])

            neo4j_db.commit(neo4j_transaction)

          return responce
        
        def create_hosted_zone(neo4j_transaction, list_of_hosted_zone:list):
          list_of_node = []
          
          for hosted_zone in list_of_hosted_zone:
              node_hosted_zone = Node(
                "ROUTE53_HOSTED_ZONE",
                name = hosted_zone["Name"]
              )
              neo4j_transaction.create(node_hosted_zone)
              list_of_node.append(node_hosted_zone)
          
          return list_of_node
        
        def create_record_sets(neo4j_transaction, node_hosted_zone,list_of_record_sets:list):
          for record in list_of_record_sets:
            if Neo4j.AWS.Route53.check_alias_or_record(record) == 0:
              # - Alias
              node_record_set = Neo4j.AWS.Route53.create_record_alias(record,neo4j_transaction)
            elif Neo4j.AWS.Route53.check_alias_or_record(record) == 1:
              # - Record
              node_record_set = Neo4j.AWS.Route53.create_record_value(record,neo4j_transaction)
            else:
              print(colors.ERROR,"[!] Neo4j.Route53 : Problem with check if it's an alias or a record",colors.reset)
              raise Exception
            
            relation_hosted_zone_and_record_set = Relationship(node_hosted_zone,"Have",node_record_set)
            neo4j_transaction.create(node_record_set)
            neo4j_transaction.create(relation_hosted_zone_and_record_set)
        
        def create_record_alias(record:dict,neo4j_transaction):
          node_record_set = Node(
            "ROUTE53_RECORD_SET",
            name=record["Name"],
            Type=record["Type"],
          )

          node_record_endpoint = Neo4j.find_node(neo4j_transaction,"ROUTE53_ENDPOINT",record["AliasTarget"]["DNSName"])
          if not node_record_endpoint:
            node_record_endpoint = Node(
              "ROUTE53_ENDPOINT",
              name = record["AliasTarget"]["DNSName"]
            )
          
          relation_record_set_and_alias = Relationship(node_record_set,"Alias",node_record_endpoint)
          neo4j_transaction.create(node_record_endpoint)
          neo4j_transaction.create(relation_record_set_and_alias)
          return node_record_set

        def create_record_value(record:dict,neo4j_transaction):
          node_record_set = Node(
            "ROUTE53_RECORD_SET",
            name=record["Name"],
            Type=record["Type"],
            TTL=record["TTL"]
          )
          for value in record["ResourceRecords"]:
            node_record_endpoint = Neo4j.find_node(neo4j_transaction,"ROUTE53_ENDPOINT",value["Value"])
            if not node_record_endpoint:
              node_record_endpoint = Node(
                "ROUTE53_ENDPOINT",
                name = value["Value"]
              )
            relation_record_set_and_value = Relationship(node_record_set,"Value",node_record_endpoint)
            neo4j_transaction.create(node_record_endpoint)
            neo4j_transaction.create(relation_record_set_and_value)
          return node_record_set

        def check_alias_or_record(record_set:dict):
          # - 0 : Alias
          # - 1 : Record
          # - 2 : Problem
          responce = 2
          if "AliasTarget" in list(record_set.keys()):
            responce = 0
          elif "ResourceRecords" in list(record_set.keys()):
            responce = 1

          return responce

      class Cloudfront:
        def create_all_ressources(data_cloudfront:list):
          responce = 1
          if len(data_cloudfront):
            responce = 0
            neo4j_db = Neo4j.DB.connect()
            neo4j_tx = neo4j_db.begin()
            
            for cloudfront in data_cloudfront:
              cloudfront_node = Node("CLOUDFRONT",
                name=AWS.Cloudfront.check_have_aliases(cloudfront),
                Status=cloudfront["Status"],
                DomainName=cloudfront["DomainName"],
                Aliases=AWS.Cloudfront.get_list_aliases(cloudfront["Aliases"]),
                PriceClass=cloudfront["PriceClass"],
                Enabled=cloudfront["Enabled"],
                IsIPV6Enabled=cloudfront["IsIPV6Enabled"],
                WebACLId=str(cloudfront["WebACLId"])
              )
              # - CLOUDFRONT_ORIGIN
              if cloudfront["Origins"]["Quantity"]:
                for origin in cloudfront["Origins"]["Items"]:
                  origin_node = Neo4j.AWS.Cloudfront.create_origin(neo4j_tx,origin)

                  print(colors.VERBOSE,"OUTPUT.origin : {}".format(origin_node),colors.reset)
                  print(colors.VERBOSE,"OUTPUT.cloudfront : {}".format(cloudfront_node),colors.reset)

                  relation_cloudfront_origin = Relationship(cloudfront_node,"ORIGIN",origin_node)
                  neo4j_tx.create(origin_node)
                  neo4j_tx.create(relation_cloudfront_origin)
              
              # - Relation - DEFAULT_BEHAVIOR
              # default_behavior_node = Neo4j.AWS.Cloudfront.find_node_origin(neo4j_tx,cloudfront["Origins"]["Items"],cloudfront["DefaultCacheBehavior"]["TargetOriginId"])
              # relation_default_behavior = Relationship(cloudfront,"DEFAULT_BEHAVIOR",default_behavior_node)
              # neo4j_tx.create(relation_default_behavior)
              # - CLOUDFRONT_CACHE_BEHAVIOR

              neo4j_tx.create(cloudfront_node)
          
          neo4j_db.commit(neo4j_tx)
          return responce
        
        def create_origin(neo4j_connect,origin:list):
          origin_node = Neo4j.AWS.Cloudfront.find_node_origin(neo4j_connect,origin["DomainName"])
          
          print("Before : {}".format(origin_node))
          if not origin_node:
            if AWS.Cloudfront.check_is_custom_origin(origin):
              # - Custom
              origin_node = Node("CLOUDFRONT_ORIGIN_CUSTOM",
                name=origin["DomainName"],
                Id=origin["Id"]
              )
              print("custom")
            else:
              # - S3
              origin_node = Node("CLOUDFRONT_ORIGIN_S3",
                name=origin["DomainName"],
                Id=origin["Id"]
              )
              print("s3")
            
          print("After : {}".format(origin_node))
          return origin_node

        # def create_behavior(neo4_connect,default_behavior:dict=False,cache_behavior:dict=False,list_of_origins:list)
        #   if not default_behavior:
        #     # - Cache_Behvior
        #     behavior_node = Node("Node",
        #       name=
        #     )
        #   else:
        #     # - Default_Behvior
        #     behavior_node = Node("CLOUDFRONT_DEFAULT_BEHAVIOR",
        #       name=
        #     )
      
        #   return behavior_node
        def find_node_origin(neo4j_connector,domain_name:str):
          matcher = NodeMatcher(neo4j_connector)          
          origin_node = matcher.match("CLOUDFRONT_ORIGIN_CUSTOM",name=domain_name).first()
          if not origin_node:
            origin_node = matcher.match("CLOUDFRONT_ORIGIN_S3",name=domain_name).first()
          else:
            origin_node = False
          
          return origin_node
