from asyncio.tasks import sleep
import sys, argparse, os, traceback
from py2neo import *

import json
import asyncio

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

async def liaisons_Route53(data_route53):
    print(colors.INFO,"[i] Neo4j.Route53 : Try create node and relattion",colors.reset)
    try:
        if Neo4j.AWS.Route53.create_all_ressources(data_route53):
            print(colors.INFO,"[i] Neo4j.Route53 : You don't have ressource",colors.reset)
        else:
            pass
    except Exception:
        print(colors.reset)
        traceback.print_exc()
        print(colors.ERROR,"[!] Neo4j.Route53 : An error occurred while created node and relation")
        sys.exit(1)
    print(colors.OK,"[+] Neo4j.Route53 : All information have been created",colors.reset)

async def liaisons_CloudFront(data_cloudfront):
    print(colors.INFO,"[i] Neo4j.Cloudfront : Try create node and relattion",colors.reset)
    try:
        if Neo4j.AWS.Cloudfront.create_all_ressources(data_cloudfront["Cloudfront"]["Items"]):
            print(colors.INFO,"[i] Neo4j.Cloudfront : You don't have ressource",colors.reset)
    except Exception:
        print(colors.reset)
        traceback.print_exc()
        print(colors.ERROR,"[!] Neo4j.Cloudfront : An error occurred while created node and relation")
        sys.exit(1)
    print(colors.OK,"[+] Neo4j.Cloudfront : All information have been created",colors.reset)

    print(colors.OK,"[+] All Nodes and Relations have been created go on {} to see the result".format(Neo4j.HOSTNAME+":"+Neo4j.DB.PORT))

async def test1 ():
    print("Début Test 1")
    await asyncio.sleep(0)
    sleep(5)
    print("Début Test 1")

async def test2 ():
    print("Début Test 2")
    await asyncio.sleep(0)
    sleep(2)
    print("Début Test 2")

async def main():
    services = {
        "Route53":test1,
        "Cloudfront":test2  
    }

    await asyncio.gather(
        General.collect("Route53",services.get("Route53")),
        General.collect("Cloudfront",services.get("Cloudfront"))
    )

#     for next_to_complete in asyncio.as_completed(list_services):
#         answer = await next_to_complete
# #        print('received answer {!r}'.format(answer))
        
#     while (completed != 1):
#         if route_status == 1 :
#             asyncio.as_completed(liaisons_Route53())
#             route_status = 0
#         elif cloudfront_status == 1:
#             asyncio.as_completed(liaisons_CloudFront())
#             cloudfront_status = 0
#         elif route_liaison == 1 & cloudfront_liaison == 1:
#             #création lien entre les 2
#             route_liaison = 0
#             cloudfront_liaison = 0
#             completed = 1
    
    print(colors.OK,"[+] All Nodes and Relations have been created go on {} to see the result".format(Neo4j.HOSTNAME+":"+Neo4j.DB.PORT))



# def main():
#     # - Collect
#     # -- Route 53
#     print(colors.INFO,"[i] AWS.Route53 : Try collect all information",colors.reset)
#     try:
#         data_route53 = AWS.Route53.collect()
#     except Exception:
#         print(colors.reset)
#         traceback.print_exc()
#         print(colors.ERROR,"[!] AWS.Route53 : An error occurred while collect information")
#         sys.exit(1)
#     print(colors.OK,"[+] AWS.Route53 : All information have been collected",colors.reset)

#     # -- CloudFront
#     print(colors.INFO,"[i] AWS.CloudFront : Try collect all information",colors.reset)
#     try:
#         data_cloudfront = AWS.Cloudfront.collect()
#     except Exception:
#         print(colors.reset)
#         traceback.print_exc()
#         print(colors.ERROR,"[!] AWS.CloudFront : An error occurred while collect information")
#         sys.exit(1)
#     print(colors.OK,"[+] AWS.CloudFront : All information have been collected",colors.reset)
    
#     with open("test.json", 'w') as output_file:
#         json.dump(data_cloudfront, output_file, sort_keys=False, indent=2,default=str) 


#     # -- S3
#     # -- ALB
#     print(colors.OK,"[+] All info have been retrieved successfully")

#     # - Neo4j
#     # -- Route53
#     print(colors.INFO,"[i] Neo4j.Route53 : Try create node and relattion",colors.reset)
#     try:
#         if Neo4j.AWS.Route53.create_all_ressources(data_route53):
#             print(colors.INFO,"[i] Neo4j.Route53 : You don't have ressource",colors.reset)
#         else:
#             pass
#     except Exception:
#         print(colors.reset)
#         traceback.print_exc()
#         print(colors.ERROR,"[!] Neo4j.Route53 : An error occurred while created node and relation")
#         sys.exit(1)
#     print(colors.OK,"[+] Neo4j.Route53 : All information have been created",colors.reset)
    
#     # -- Cloudfront
#     print(colors.INFO,"[i] Neo4j.Cloudfront : Try create node and relattion",colors.reset)
#     try:
#         if Neo4j.AWS.Cloudfront.create_all_ressources(data_cloudfront["Cloudfront"]["Items"]):
#             print(colors.INFO,"[i] Neo4j.Cloudfront : You don't have ressource",colors.reset)
#         else:
#             pass
#     except Exception:
#         print(colors.reset)
#         traceback.print_exc()
#         print(colors.ERROR,"[!] Neo4j.Cloudfront : An error occurred while created node and relation")
#         sys.exit(1)
#     print(colors.OK,"[+] Neo4j.Cloudfront : All information have been created",colors.reset)

#     print(colors.OK,"[+] All Nodes and Relations have been created go on {} to see the result".format(Neo4j.HOSTNAME+":"+Neo4j.DB.PORT))


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

    asyncio.run(main())