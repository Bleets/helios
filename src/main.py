import argparse, os
from py2neo import *

import json

# Our Librairies 
from libs.colors import colors
from libs.settings import General
from libs.aws_services import AWS
from libs.neo4j_services import Neo4j

# -- Setup Parser
def setup_parser():
    parser = argparse.ArgumentParser(
        description="This programs will collect all information about your aws account"
    )
    parser.add_argument(
        "-p",
        "--profile",
        help="Which profile you want to run (DEFAULT: default)"
    )
    parser.add_argument(
        "-r",
        "--region",
        help="Which region you want to run the script (DEFAULT: eu-west-1)"
    )
    parser.add_argument(
        "-v", "--verbose", action="count", help="Increase output verbosity (v, vv, vvv)"
    )
    return parser

def main():
    # - Get all service enabled
    service_enabled = ["ROUTE53","Cloudfront"]
    # - Collect
    services = {
        "Route53":{
            "Collect_function" : AWS.ROUTE53.collect,
            "Node_function" : Neo4j.AWS.ROUTE53.create_all_ressources,
            "Associations" : {
                "Cloudfront":Neo4j.AWS.Associations.route53_cloudfront
            }
        },
        "Cloudfront":{
            "Collect_function" : AWS.Cloudfront.collect,
            "Node_function" : Neo4j.AWS.Cloudfront.create_all_ressources,
        }
    }
    results = []
    
    # - AWS
    for service in services:
        results.append(General.collect(service,services.get(service)["Collect_function"]))
    
    print(colors.OK,"[+] All info have been retrieved successfully")

    # -- debug
    with open("test.json", 'w') as output_file:
        json.dump(results, output_file, sort_keys=False, indent=2,default=str)

    # - Neo4j
    for result in results:
        service = list(result.keys())[0]
        node_function = services.get(service)["Node_function"]
        General.create_all_nodes(service,node_function,result)

    # - Associations
    for service in service_enabled:
        if services["Route53"].get("Associations"):
            all_associations = services["Route53"].get("Associations")
            for associate_service in list(all_associations.keys()):
                function_association = all_associations[associate_service]
                General.association(service,associate_service,function_association)

    print(colors.OK,"[+] All Nodes and Relations have been created go on {} to see the result".format(Neo4j.HOSTNAME+":"+Neo4j.DB.PORT))


if __name__ == "__main__":
    # - Setup Env
    parser = setup_parser()
    args = parser.parse_args()
    VERBOSITY = args.verbose if args.verbose else 0
    PROFILE = args.profile if args.profile else AWS.PROFILE
    # Info : We set the region with the environment variable because
    #       "Session" method or "Config()" doesn't work or overwrite the
    #       Region set in ~/.aws/config
    os.environ["AWS_DEFAULT_REGION"] = args.region if args.region else AWS.REGION
    AWS.setup_profile(PROFILE)
    
    if VERBOSITY:
        General.verbose(VERBOSITY, os.environ["AWS_DEFAULT_REGION"],"Region")
        General.verbose(VERBOSITY, PROFILE,"Profile")

    main()
