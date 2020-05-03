from py2neo import *
import boto3
import sys
import pprint  # DEGUB : For well display dict
import cmap as CMAP

DB = Graph("localhost:7474", auth=("neo4j", "test"))

# Setup envirnment
def setup_env(profile="default"):
    if profile != "default":
        print("INFO : Init environment on profile {}".format(profile))
        boto3.setup_default_session(profile_name=profile)


def usage():
    print("This is the usage")


def route53_collect():
    try:
        tx = DB.begin()
        r53_client = boto3.client("route53")

        # - Get ID of all hosted zones
        for hostedzone in r53_client.list_hosted_zones(MaxItems="3")["HostedZones"]:
            id_hostedzone = hostedzone["Id"].split("/")[2]

            # -- Create zone node
            zone = Node(
                "Route53_ZONE",
                name=hostedzone["Name"],
                ID=id_hostedzone,
                PrivateZone=hostedzone["Config"]["PrivateZone"],
                RecordSetCount=hostedzone["ResourceRecordSetCount"],
            )
            tx.create(zone)

            # For each zone dump all records (MaxItems=100) and create node
            list_record_set = r53_client.list_resource_record_sets(
                HostedZoneId=id_hostedzone
            )
            route53_record_create_node(zone, list_record_set, r53_client, tx)

            # -- WARNING :
            ## Don't uncomment the code below this will break the limit of MaxItems and
            ## the visualieation of data in your browser will lag if you don't have a powerfull PC

            # while list_record_set["IsTruncated"]:
            #     list_record_set = r53_client.list_resource_record_sets(
            #         HostedZoneId=id_hostedzone,
            #         StartRecordName=str(list_record_set["NextRecordName"]),
            #         StartRecordType=str(list_record_set["NextRecordType"]),
            #     )
            #     route53_record_create_node(zone, list_record_set, r53_client, tx)

        tx.commit()
    except Exception as error:
        print("An error occurred getting Route53 ressource:")
        print(str(error))
        raise


def route53_record_create_node(zone, list_record_set, r53_client, tx):
    for name in list_record_set["ResourceRecordSets"]:
        # If is an Alias
        matcher = NodeMatcher(tx)
        if "AliasTarget" in name:
            # Create record node
            record = Node("Route53_RECORD", name=name["Name"], Type=name["Type"])

            # Find if an node Route53_RECORD_ALIAS all ready exist
            alias = matcher.match(
                "Route53_RECORD_ALIAS", name=name["AliasTarget"]["DNSName"]
            ).first()
            # If the node doesn't exist create it
            if not alias:
                alias = Node(
                    "Route53_RECORD_ALIAS",
                    name=name["AliasTarget"]["DNSName"],
                    HostedZoneId=name["AliasTarget"]["HostedZoneId"],
                    EvaluateTargetHealth=name["AliasTarget"]["EvaluateTargetHealth"],
                )
                tx.create(alias)

            record_to_alias = Relationship(record, "ALIAS", alias)
            tx.create(record_to_alias)
        # If is not an Alias
        else:
            record = Node(
                "Route53_RECORD", name=name["Name"], Type=name["Type"], TTL=name["TTL"]
            )

            # List all value for a record
            for ressource in name["ResourceRecords"]:
                # Create value node
                value = matcher.match(
                    "Route53_RECORD_VALUE", name=ressource["Value"]
                ).first()
                if not value:
                    value = Node("Route53_RECORD_VALUE", name=ressource["Value"])
                    tx.create(value)
                # Create the relationship between the record and thoses values
                record_to_value = Relationship(record, "VALUE", value)
                tx.create(record_to_value)

        zone_to_record = Relationship(zone, "CONTENT", record)
        tx.create(record)
        tx.create(zone_to_record)


def main():
    # - Collect
    # -- Route 53
    print("INFO : Collect all information on Route53")
    route53_collect()
    # -- CloudFront
    # -- S3
    # -- ALB


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        if len(sys.argv) == 2:
            setup_env(sys.argv[1])
        main()
    else:
        usage()
