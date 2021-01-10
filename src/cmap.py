from py2neo import Graph, Node, Relationship, NodeMatcher
import boto3
import sys
import pprint  # DEGUB : For well display dict

DB = Graph("172.21.0.3:7474", auth=("neo4j", "test"))

# The usage of the script
def usage():
    print("cmap.py : The Cloud Mapper")
    print("usage: cmap.py ENV=<env> DNS=<dns>")
    print("    <env>: The environment where the dns is")
    print("    <dns>: The dns which you want information")


# Setup envirnment
def setup_env(profile="default"):
    if profile != "default":
        print("INFO : Init environment on profile '{}'".format(profile))
        boto3.setup_default_session(profile_name=profile)


# Check if the environment is avaible in the conf file
def check_env(env):
    return True if env in boto3.session.Session().available_profiles else False


# Return a list off all cloudfront use by an url
def cloudfront_find(dns):
    try:
        cloudfront_client = boto3.client("cloudfront")
        result = []

        # Parse all cloudfront
        list_of_distribution = cloudfront_client.list_distributions()
        for cloudfront in list_of_distribution["DistributionList"]["Items"]:
            exist = False
            match = False

            # Check if the distributions have some 'Aliases'
            if not exist and cloudfront["Aliases"]["Quantity"] > 0:
                aliases = cloudfront["Aliases"]["Items"]
                nb_aliases = cloudfront["Aliases"]["Quantity"]
                # Testing each alias
                for i in range(nb_aliases):
                    # If is a wildcard DNS (ex:'*.toto.com')
                    if aliases[i][0] == "*":
                        wildcard_dns = aliases[i].split(".")
                        wildcard_dns = ".".join(wildcard_dns[1 : len(wildcard_dns)])
                        if wildcard_dns in dns:
                            match = True
                    # Else is an basic DNS
                    elif dns in aliases[i]:
                        match = True
                    # Check if match
                    if match:
                        if len(result):
                            for i in range(len(result)):
                                if cloudfront["DomainName"] == result[i]["DomainName"]:
                                    exist = True
                                    break
                        # Check if the CloudFront already exist in 'result'
                        if not exist:
                            result.append(cloudfront)
        return result
    except Exception as error:
        print("ERROR : An error occurred getting list of cloudfront")
        print(str(error))
        raise


def cloudfront_create_node(list_cloudfront):
    try:
        tx = DB.begin()
        matcher = NodeMatcher(tx)
        for cloudfront in list_cloudfront:
            cloudfront_node = Node(
                "CloudFront_DISTRIBUTION",
                name=cloudfront["DomainName"],
                ARN=cloudfront["ARN"],
                Enabled=str(cloudfront["Enabled"]),
                Status=cloudfront["Status"],
            )
            tx.create(cloudfront_node)

            # -- Create "CloudFront_ALIAS"
            if cloudfront["Aliases"]["Quantity"] > 0:
                for aliases in cloudfront["Aliases"]["Items"]:
                    alias_node = matcher.match("CloudFront_ALIAS", name=aliases).first()
                    # If "CloudFront_ALIAS" doesn't exist
                    if not alias_node:
                        alias_node = Node("CloudFront_ALIAS", name=aliases)
                        tx.create(alias_node)
                    cloudfront_to_alias = Relationship(
                        cloudfront_node, "ALIAS", alias_node
                    )
                    tx.create(cloudfront_to_alias)

            # -- Create "CloudFront_ORIGIN"
            default_target_origin = cloudfront["DefaultCacheBehavior"]["TargetOriginId"]
            if cloudfront["Origins"]["Quantity"] > 0:
                for origin in cloudfront["Origins"]["Items"]:
                    origin_node = matcher.match(
                        "CloudFront_ORIGIN", name=origin["DomainName"]
                    ).first()
                    if not origin_node:
                        origin_node = Node(
                            "CloudFront_ORIGIN", name=origin["DomainName"]
                        )
                        tx.create(origin_node)
                    cloudfront_to_origin = Relationship(
                        cloudfront_node, "ORIGIN", origin_node
                    )
                    # -- Create the "CloudFront_DEFAULT_CACHEBEHAVIOR" Relation
                    if origin["Id"] == default_target_origin:
                        default_to_origin = Relationship(
                            cloudfront_node, "DEFAULT_BEHAVIOR", origin_node
                        )
                        tx.create(default_to_origin)
                    tx.create(cloudfront_to_origin)

            # -- Create "CloudFront_CACHEBEHAVIORS"
            if cloudfront["CacheBehaviors"]["Quantity"] > 0:
                for behavior in cloudfront["CacheBehaviors"]["Items"]:
                    # Translate 'behavior["TargetOriginId"]' to origin DomainName and find it
                    for origin in cloudfront["Origins"]["Items"]:
                        if origin["Id"] == behavior["TargetOriginId"]:
                            target_origin_node = matcher.match(
                                "CloudFront_ORIGIN", name=origin["DomainName"]
                            ).first()

                    # Create the Node and Relationship
                    behavior_node = Node(
                        "CloudFront_CACHEBEHAVIORS",
                        name=behavior["PathPattern"],
                        DefaultTTL=behavior["DefaultTTL"],
                        MaxTTL=behavior["MaxTTL"],
                        MinTTL=behavior["MinTTL"],
                    )
                    behavior_to_target = Relationship(
                        behavior_node, "CONNECT", target_origin_node
                    )
                    cloudfront_to_behavior = Relationship(
                        cloudfront_node, "BEHAVIOR", behavior_node
                    )
                    tx.create(behavior_node)
                    tx.create(behavior_to_target)
                    tx.create(cloudfront_to_behavior)

        tx.commit()
    except Exception as error:
        print("ERROR : An error occurred during the creation of node")
        print(str(error))
        raise


def main(argv):
    env = argv[1]
    dns = argv[2]

    # -- Check if the Environment is available and setup it if is good
    if check_env(env):
        print("INFO : '{}' is an environment available".format(env))
        setup_env(env)
    else:
        print(
            "WARNING : '{}' isn't an environment available. Check your configuration file".format(
                env
            )
        )
        return

    print("INFO : Search information in '{}' for '{}' on CloudFront".format(env, dns))
    # Cloudfront
    list_cloudfront = cloudfront_find(dns)
    if len(list_cloudfront):
        print("INFO : Find some information in Cloudfront")
        cloudfront_create_node(list_cloudfront)
    else:
        print("INFO : Nothing find in CloudFront")


if __name__ == "__main__":
    print(len(sys.argv))
    pprint.pprint(sys.argv)
    print("------------------------------------------------------")
    # Check if we have minimum 1 arguments
    if len(sys.argv) >= 2:
        # If we have only 1 argument env = default
        if len(sys.argv) == 2:
            sys.argv.append(sys.argv[1])
            sys.argv[1] = "default"
        main(sys.argv)
    else:
        usage()
