import sys, argparse, os, traceback
from py2neo import *

# Our Librairies 
from libs.colors import colors
from libs.settings import *
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
    # parser.add_argument(
    #     "-s",
    #     "--services",
    #     help="The list of all services you want or config file"
    # )
    parser.add_argument(
        "-v", "--verbose", action="count", help="Increase output verbosity (v, vv, vvv)"
    )
    return parser

def main():
    # - Collect
    # -- Route 53
    print(colors.INFO,"[i] AWS.Route53 : Try collect all information",colors.reset)
    try:
        data_route53 = AWS.Route53.collect()
    except Exception:
        print(colors.reset)
        traceback.print_exc()
        print(colors.ERROR,"[!] AWS.Route53 : An error occurred while collect information")
        sys.exit(1)
    print(colors.OK,"[+] AWS.Route53 : All information have been collected",colors.reset)

    # -- CloudFront
    # -- S3
    # -- ALB
    print(colors.OK,"[+] All info have been retrieved successfully")

    # - Build all Node and Relation needed
    # -- Route53
    print(colors.INFO,"[i] Neo4j.Route53 : Try create node and relattion",colors.reset)
    try:
        if Neo4j.AWS.Route53.create_all_ressource(data_route53):
            print(colors.INFO,"[i] Neo4j.Route53 : You don't have ressource",colors.reset)
        else:
            pass
    except Exception:
        print(colors.reset)
        traceback.print_exc()
        print(colors.ERROR,"[!] Neo4j.Route53 : An error occurred while created node and relation")
        sys.exit(1)
    print(colors.OK,"[+] Neo4j.Route53 : All information have been created",colors.reset)

    print(colors.OK,"[+] All Nodes and Relations have been created go on {} to see the result".format(Neo4j.HOSTNAME+Neo4j.DB.PORT))


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
