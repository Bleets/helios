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
        "-s",
        "--setting-file",
        help="Which file you want to use forr setting (DEFAULT: 'setting.yml')"
    )
    parser.add_argument(
        "-v", "--verbose", action="count", help="Increase output verbosity (v, vv, vvv)"
    )
    return parser

def main(services_enabled:list):
    services = {
        "route53":{
            "Collect_function" : AWS.ROUTE53.collect,
            "Node_function" : Neo4j.AWS.ROUTE53.create_all_ressources,
            "Associations" : {
                "Cloudfront":Neo4j.AWS.Associations.route53_cloudfront
            }
        },
        "cloudfront":{
            "Collect_function" : AWS.Cloudfront.collect,
            "Node_function" : Neo4j.AWS.Cloudfront.create_all_ressources,
        }
    }
    results = []
    
    # - Set default value if no services
    if not len(services_enabled):
        services_enabled = list(services.keys())
    # - Collect
    # -- AWS
    for service in services:
        if service in services_enabled:
            results.append(General.collect(service,services.get(service)["Collect_function"]))
    
    print(colors.OK,"[+] All info have been retrieved successfully")

    # - Neo4j
    for result in results:
        service = list(result.keys())[0]
        node_function = services.get(service)["Node_function"]
        General.create_all_nodes(service,node_function,result)

    # - Associations
    for service in services_enabled:
        if services[service].get("Associations"):
            all_associations = services[service].get("Associations")
            for associate_service in list(all_associations.keys()):
                function_association = all_associations[associate_service]
                General.association(service,associate_service,function_association)

    print(colors.OK,"[+] All Nodes and Relations have been created go on {} to see the result".format(Neo4j.HOSTNAME+":"+Neo4j.DB.PORT))


if __name__ == "__main__":
    # - Setup Env
    parser = setup_parser()
    args = parser.parse_args()
    # - AWS
    PROFILE = args.profile if args.profile else AWS.PROFILE
    # Info : We set the region with the environment variable because
    #       "Session" method or "Config()" doesn't work or overwrite the
    #       Region set in ~/.aws/config
    os.environ["AWS_DEFAULT_REGION"] = args.region if args.region else AWS.REGION
    AWS.setup_profile(PROFILE)

    # -- User Setting
    SETTING_FILE = args.setting_file or 'setting.yml'
    user_setting = General.get_user_settings(SETTING_FILE)

    LEVEL_LOG = General.get_user_level_log(user_setting)
    VERBOSITY = args.verbose or General.get_user_verbose(LEVEL_LOG)
    PAGINATION = General.get_user_pagination(user_setting)
    global SERVICES_ENABLED
    SERVICES_ENABLED = General.get_user_services(user_setting)
    
    if VERBOSITY:
        General.verbose(VERBOSITY, PROFILE,"Profile")
        General.verbose(VERBOSITY, os.environ["AWS_DEFAULT_REGION"],"Region")
        General.verbose(VERBOSITY, LEVEL_LOG,"level_log")
        General.verbose(VERBOSITY, PAGINATION,"Pagination")
        General.verbose(VERBOSITY, SERVICES_ENABLED,"Services_enbaled")

    main(SERVICES_ENABLED)
