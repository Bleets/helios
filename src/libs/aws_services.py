import collections
import boto3
import re
# - DEBUG
import json, sys

from libs.settings import General
from .colors import colors

class AWS:
  PROFILE = "default"
  REGION = "eu-west-1"
  
  def setup_profile(profile:str="default"):
    if profile != "default":
        print(colors.INFO,"[i] Init environment on profile {}".format(profile),colors.reset)
        boto3.setup_default_session(profile_name=profile)
  
  class Route53:
    def collect():
      r53_data = {"Route53":{"HostedZones":[]}}
      r53_client = boto3.client("route53")

      next_marker = ""
      while True:
        if len(next_marker):
          response = r53_client.list_hosted_zones(Marker=next_marker)
        else:
          response = r53_client.list_hosted_zones()
        if not response["IsTruncated"]:
          break
        else:
          next_marker = response["NextMarker"]

      for hosted_zone in response["HostedZones"]:
        r53_data["Route53"]["HostedZones"].append(AWS.Route53.collect_record_set(r53_client,hosted_zone))
      
      return r53_data

    def collect_record_set(r53_client,HostedZone:dict):
      list_of_type = ["A","AAAA","CNAME"]

      data = General.filter_data(HostedZone,[
        "Id",
        "Name",
        ["Config","PrivateZone"],
        "ResourceRecordSetCount"
        ]
      )
      data.update({"ResourceRecordSets":[]})
      
      # -- Get all Record Set for an HostedZoneId
      start_record_name = ""
      start_record_type = ""
      while True:
        if len(start_record_name):
          response = r53_client.list_resource_record_sets(
            HostedZoneId=HostedZone["Id"],
            StartRecordName=start_record_name,
            StartRecordType=start_record_type,
          )
        else:
          response = r53_client.list_resource_record_sets(HostedZoneId=HostedZone["Id"])

        data["ResourceRecordSets"].append(AWS.Route53.filter_record(response["ResourceRecordSets"],list_of_type))
        
        if not response["IsTruncated"]:
          break
        else:
          start_record_name = response["NextRecordName"]
          start_record_type = response["NextRecordType"]
          # -- Uncomment the following "break" if you want to unactivate the pagination
          # break

      # - this following command permit to flatten list 2d to 1d (ex: [[1,2,3],[4,5,6]] -> [1,2,3,4,5,6])
      data["ResourceRecordSets"] = sum(data["ResourceRecordSets"],[])

      return data

    def filter_record(list_of_records_sets:list,list_of_type_wanted:list=["A","AAAA","CAA","CNAME","MX","NAPTR","NS","PTR","SOA","SPF","SRV","TXT","DS"],certificat_filter:bool=True):
      data = []
      regex_certificate = ".*acm-validations\.aws\.$"

      for record_set in list_of_records_sets:
        if record_set["Type"] in list_of_type_wanted:
          if certificat_filter:
            # print(json.dumps(record_set,indent=2,sort_keys=False))
            if record_set["Type"] == "CNAME" and re.search(regex_certificate,record_set["ResourceRecords"][0]["Value"]):
              pass
            else:
              data.append(record_set)
          else:
            data.append(record_set)
      
      return data

    def display_nb_recordset(data:dict):
      cpt = 0
      for hosted_zones in data["Route53"]["HostedZones"]:
          print(colors.DEBUG,"{} for {}".format(len(hosted_zones["ResourceRecordSets"]),hosted_zones["Name"]),colors.reset)
          cpt += len(hosted_zones["ResourceRecordSets"])
      print(colors.DEBUG,"Total of recordset = {}".format(cpt),colors.reset)

  
  class S3:
    def list_buckt(resource):
      for bucket in resource.buckets.all():
        print(bucket.name)